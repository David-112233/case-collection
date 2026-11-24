import { clamp, mix, smooth, fract, seededRandom, resolveState, windowLight, sunAppearance, moonAppearance, precipitationAppearance, stormAppearance } from './state.js';
import { GROUND_OFFSET, STREET, LOWER_ROAD, EAST_ROAD, BRIDGE, STREAM, STORM_TREE, curvePoint, curvePath, streetAtX, riverPoint, houses, trees, fences, lamps } from './layout.js';

const TAU = Math.PI * 2;
const TREE_STRIKE_Y = -78;
const rgb = (a, b, t) => a.map((v, i) => Math.round(mix(v, b[i], clamp(t))));
const css = (c, a = 1) => `rgba(${c[0]},${c[1]},${c[2]},${a})`;
const pathCache = new Map();
const village = [
    ...houses.map(args => ({ kind: 'house', args })),
    ...trees.map(args => ({ kind: 'tree', args })),
    { kind: 'church', args: [699, 521, .96] },
].sort((a, b) => a.args[1] - b.args[1]);

/** Canvas village with replaceable weather data. destroy() releases all observers and timers. */
export class Dorfwelt {
    constructor(element, options = {}) {
        this.element = element;
        this.options = options;
        this.input = options.state ?? {};
        this.anchor = performance.now();
        this.epoch = this.input.time ?? Date.now() / 1000;
        this.elapsed = 0;
        this.stormTime = 0;
        this.cloudTravel = 0;
        this.windTravel = 0;
        this.walkTravel = 0;
        this.last = 0;
        this.frame = 0;
        this.visible = true;
        this.paused = options.paused === true;
        this.destroyed = false;
        this.wetUntil = 0;
        this.snowDust = 0;
        this.target = resolveState(this.input, this.epoch);
        this.state = { ...this.target };
        this.random = seededRandom(options.seed ?? 73);
        this.stars = Array.from({ length: 260 }, () => ({ x: this.random() * 1440, y: this.random() * 424, r: .3 + this.random() * 1.0, p: this.random() * TAU }));
        this.particles = Array.from({ length: 140 }, () => ({ x: this.random(), y: this.random(), z: .25 + this.random() * .75, p: this.random() * TAU }));
        this.clouds = Array.from({ length: 15 }, (_, i) => ({ x: this.random() * 1880 - 220, y: 32 + this.random() * 235, s: .5 + this.random() * 1.15, p: i * 9.7 }));
        this.particles.push(...Array.from({ length: 380 }, () => ({ x: this.random(), y: this.random(), z: .25 + this.random() * .75, p: this.random() * TAU })));
        this.abort = new AbortController();
        this.canvas = document.createElement('canvas');
        this.canvas.setAttribute('aria-hidden', 'true');
        this.ctx = this.canvas.getContext('2d', { alpha: false });
        if (!this.ctx) return;
        const paper = document.createElement('canvas');
        paper.width = 128; paper.height = 128;
        const pc = paper.getContext('2d');
        if (pc) {
            const random = seededRandom(1907);
            for (let i = 0; i < 2300; i++) {
                pc.fillStyle = i % 2 ? '#fcf0c814' : '#071d181a';
                pc.fillRect(random() * 128, random() * 128, .6 + random() * 1.2, .6 + random() * 1.2);
            }
            this.paper = this.ctx.createPattern(paper, 'repeat');
        }
        element.classList.add('dorfwelt');
        element.append(this.canvas);
        this.motion = matchMedia('(prefers-reduced-motion: reduce)');
        this.connection = navigator.connection;
        this.pauseButton = document.createElement('button');
        this.pauseButton.type = 'button';
        this.pauseButton.className = 'dorfwelt__pause';
        this.pauseButton.addEventListener('click', () => this.setPaused(!this.paused), { signal: this.abort.signal });
        if (options.controls !== false) element.append(this.pauseButton);
        this.refreshButton();
        const refresh = () => { this.last = 0; this.refreshButton(); this.schedule(); this.render(); };
        document.addEventListener('visibilitychange', refresh, { signal: this.abort.signal });
        this.motion.addEventListener('change', refresh, { signal: this.abort.signal });
        this.connection?.addEventListener('change', refresh, { signal: this.abort.signal });
        this.resizeObserver = new ResizeObserver(() => this.resize());
        this.resizeObserver.observe(element);
        this.intersectionObserver = new IntersectionObserver(entries => {
            this.visible = entries[0]?.isIntersecting ?? true;
            refresh();
        });
        this.intersectionObserver.observe(element);
        this.tick = setInterval(() => {
            if (this.destroyed || document.hidden || !this.visible) return;
            this.target = resolveState(this.input, this.now());
            if (!this.moving()) { this.state = { ...this.target }; this.render(); }
        }, 1000);
        this.resize();
        this.schedule();
    }

    now() { return this.epoch + (performance.now() - this.anchor) / 1000; }
    moving() { return !this.paused && !this.motion?.matches && !this.connection?.saveData && this.visible && !document.hidden && !this.destroyed; }
    refreshButton() {
        if (!this.pauseButton) return;
        const stopped = this.paused || this.motion.matches || this.connection?.saveData;
        this.pauseButton.textContent = stopped ? '▶' : 'Ⅱ';
        this.pauseButton.setAttribute('aria-label', stopped ? 'Resume animation' : 'Pause animation');
        this.pauseButton.setAttribute('aria-pressed', String(this.paused));
        this.pauseButton.hidden = this.motion.matches || !!this.connection?.saveData;
    }
    setPaused(paused) { this.paused = !!paused; this.last = 0; this.refreshButton(); this.schedule(); }

    /** Merge only the supplied data sources. null clears an observed value. */
    setState(patch) {
        if (this.destroyed) return;
        if (typeof patch.time === 'number' && patch.hour === undefined) {
            patch = { ...patch, hour: resolveState(this.input, patch.time).hour };
        }
        for (const key of ['sun', 'moon', 'forecast', 'observation']) {
            if (patch[key]) this.input = { ...this.input, [key]: { ...this.input[key], ...patch[key] } };
        }
        for (const [key, value] of Object.entries(patch)) {
            if (!['sun', 'moon', 'forecast', 'observation'].includes(key)) this.input = { ...this.input, [key]: value };
        }
        if (typeof patch.time === 'number' && Number.isFinite(patch.time)) { this.epoch = patch.time; this.anchor = performance.now(); }
        this.target = resolveState(this.input, this.now());
        if (!this.moving()) this.state = { ...this.target };
        this.render();
        this.schedule();
    }

    resize() {
        const box = this.element.getBoundingClientRect();
        if (!box.width || !box.height) return;
        this.width = box.width;
        this.height = box.height;
        const landscapeHeight = typeof this.options.landscapeHeight === 'function'
            ? this.options.landscapeHeight(box) : this.options.landscapeHeight;
        this.landscapeHeight = Number.isFinite(landscapeHeight) && landscapeHeight > 0
            ? Math.min(box.height, landscapeHeight) : box.height;
        this.dpr = Math.min(devicePixelRatio || 1, 1.5, 1800 / box.width);
        this.canvas.width = Math.round(box.width * this.dpr);
        this.canvas.height = Math.round(box.height * this.dpr);
        this.render();
    }

    schedule() {
        if (!this.moving()) { cancelAnimationFrame(this.frame); this.frame = 0; return; }
        if (this.frame) return;
        this.frame = requestAnimationFrame(time => {
            this.frame = 0;
            if (!this.moving()) return;
            if (!this.last || time - this.last >= 40) {
                const dt = this.last ? Math.min((time - this.last) / 1000, .15) : 0;
                this.last = time;
                this.elapsed += dt;
                this.stormTime = this.target.storm ? this.stormTime + dt : 0;
                this.cloudTravel += dt * (1.1 + this.state.wind * .65);
                this.windTravel += dt * this.state.wind * (Math.sin(this.state.windDirection * Math.PI / 180) > 0 ? -1 : 1);
                this.walkTravel += dt * (this.target.rainRate > 0 ? 8 : 4.5);
                const blend = 1 - Math.exp(-dt / 2.2);
                for (const [key, value] of Object.entries(this.target)) {
                    if (key === 'moonPhase') {
                        const delta = ((value - this.state[key] + 1.5) % 1) - .5;
                        this.state[key] = (this.state[key] + delta * blend + 1) % 1;
                        continue;
                    }
                    this.state[key] = typeof value === 'number' && typeof this.state[key] === 'number'
                        && !['now', 'hour', 'month', 'rainRate'].includes(key) ? mix(this.state[key], value, blend) : value;
                }
                this.state.now = this.now();
                if (this.target.rainRate > 0) this.wetUntil = this.now() + 180;
                // Only snowfall experienced by the scene leaves decorative snow.
                // The season and a missing snow depth must not imply snow cover.
                this.snowDust = clamp(this.snowDust + dt * (this.target.snow && !this.target.sleet ? .0009 : -.00015));
                this.render();
            }
            this.schedule();
        });
    }

    destroy() {
        this.destroyed = true;
        cancelAnimationFrame(this.frame);
        clearInterval(this.tick);
        this.abort.abort();
        this.resizeObserver?.disconnect();
        this.intersectionObserver?.disconnect();
        this.canvas.remove();
        this.pauseButton?.remove();
        this.element.classList.remove('dorfwelt');
    }

    path(data, fill, stroke, width = 1) {
        let p = pathCache.get(data);
        if (!p) { p = new Path2D(data); if (pathCache.size < 350) pathCache.set(data, p); }
        if (fill) { this.ctx.fillStyle = fill; this.ctx.fill(p); }
        if (stroke) { this.ctx.strokeStyle = stroke; this.ctx.lineWidth = width; this.ctx.stroke(p); }
    }
    ellipse(x, y, rx, ry, fill) {
        const c = this.ctx;
        c.beginPath(); c.ellipse(x, y, Math.max(.01, rx), Math.max(.01, ry), 0, 0, TAU); c.fillStyle = fill; c.fill();
    }
    rect(x, y, w, h, fill) { this.ctx.fillStyle = fill; this.ctx.fillRect(x, y, w, h); }
    line(x, y, xx, yy, color, width = 1) {
        const c = this.ctx; c.beginPath(); c.moveTo(x, y); c.lineTo(xx, yy); c.strokeStyle = color; c.lineWidth = width; c.stroke();
    }
    glow(x, y, radius, color, alpha) {
        const g = this.ctx.createRadialGradient(x, y, 0, x, y, radius);
        g.addColorStop(0, css(color, alpha)); g.addColorStop(.25, css(color, alpha * .45)); g.addColorStop(1, css(color, 0));
        this.ellipse(x, y, radius, radius, g);
    }
    litColor(day, night) {
        const s = this.state;
        const gold = s.goldenLight * (1 - s.cloud * .85);
        const warm = [Math.min(255, day[0] * 1.16 + 12), day[1] * .97 + 3, day[2] * .68];
        const light = rgb(night, rgb(day, warm, gold * .65), s.daylight);
        return rgb(light, rgb(night, [48, 61, 73], .5), (s.storminess ?? 0) * s.daylight * .52);
    }
    color(day, night = [20, 36, 40]) { return css(this.litColor(day, night)); }
    snowTone(shade = 0) {
        const moon = this.state.moonLight * (1 - this.state.cloud * .7);
        const night = rgb([169, 190, 208], [99, 126, 155], shade).map(v => v + moon * 17);
        return this.litColor(rgb([250, 250, 244], [182, 205, 220], shade), night);
    }
    snowColor(shade = 0, alpha = 1) { return css(this.snowTone(shade), alpha); }
    coveredColor(day, night, shade = .4) {
        // Schnee verändert auch die Nachtfarbe; sonst bleiben verschneite Wiesen dunkelgrün.
        return css(rgb(this.litColor(day, night), this.snowTone(shade), this.cover));
    }
    snowDrift(x, y, width, height) {
        if (this.cover <= .01) return;
        const c = this.ctx;
        c.save(); c.translate(x, y); c.scale(width, height); c.globalAlpha *= this.cover;
        const light = c.createLinearGradient(0, -1, 0, .4);
        light.addColorStop(0, this.snowColor(.05));
        light.addColorStop(.45, this.snowColor(.22, .8));
        light.addColorStop(1, this.snowColor(.55, 0));
        this.path('M-1 0Q-.8-.5-.5-.46Q-.2-1 .12-.68Q.48-.84 .75-.3Q.9-.26 1 0Q.4.5-.15.38Q-.7.4-1 0Z', light);
        c.restore();
    }
    skyY(y) { return this.skyTop + y * (424 - this.skyTop) / 424; }

    render() {
        if (!this.ctx || !this.width || this.destroyed || document.hidden || !this.visible) return;
        const c = this.ctx, s = this.state;
        c.setTransform(this.dpr, 0, 0, this.dpr, 0, 0);
        c.clearRect(0, 0, this.width, this.height);
        // Extra container height extends the sky without enlarging the village.
        const scale = Math.max(this.width / 1440, this.landscapeHeight / 720);
        this.skyTop = Math.min(0, 720 - this.height / scale);
        c.translate((this.width - 1440 * scale) * .66, this.height - 720 * scale);
        c.scale(scale, scale);
        c.lineCap = 'round'; c.lineJoin = 'round';
        this.cover = Math.max(s.snowCover, this.snowDust);
        this.stormEffect = this.target.storm && this.moving()
            ? stormAppearance(this.stormTime, this.options.seed ?? 73, this.options.easterEggs !== false) : null;
        this.wet = Math.max(s.rain > 0 ? .5 + s.rain * .5 : 0, clamp((this.wetUntil - this.now()) / 180));
        this.sky();
        this.celestial();
        this.cloudLayer();
        this.stormSky();
        this.hills();
        this.fogLayer(.45, 394);
        this.farLife();
        c.save(); c.translate(0, GROUND_OFFSET);
        this.land();
        for (const item of village) this[item.kind](...item.args);
        if (this.stormEffect?.kind === 'tree' && this.stormEffect.flash > 0) {
            const [x, y, scale] = STORM_TREE;
            this.lightningBolt(x - 110, this.skyY(120) - GROUND_OFFSET,
                x + this.treeSway(x) * TREE_STRIKE_Y * scale, y + TREE_STRIKE_Y * scale);
        }
        this.people();
        this.details();
        this.animals();
        this.fogLayer(.6, 565);
        this.foreground();
        this.specials();
        c.restore();
        this.precipitation();
        if (this.paper) { c.save(); c.globalAlpha = .12; this.rect(0, this.skyTop, 1440, 720 - this.skyTop, this.paper); c.restore(); }
        const vignette = c.createLinearGradient(0, this.skyTop, 0, 720);
        vignette.addColorStop(0, '#10213112'); vignette.addColorStop(.6, '#00000000'); vignette.addColorStop(1, '#071a293d');
        this.rect(0, this.skyTop, 1440, 720 - this.skyTop, vignette);
        this.options.onRender?.(this.canvas);
    }

    sky() {
        const c = this.ctx, s = this.state;
        let top = rgb([12, 22, 46], [83, 151, 172], s.daylight);
        let middle = rgb([26, 42, 63], [157, 199, 197], s.daylight);
        let horizon = rgb([55, 67, 77], [238, 225, 180], s.daylight);
        top = rgb(top, s.morning ? [78, 105, 137] : [69, 75, 120], s.twilight * .75);
        middle = rgb(middle, s.morning ? [214, 172, 159] : [201, 133, 131], s.twilight * .83);
        horizon = rgb(horizon, [255, 189, 118], s.twilight);
        const cloud = s.cloud * .7;
        top = rgb(top, rgb([24, 31, 48], [122, 148, 154], s.daylight), cloud);
        middle = rgb(middle, rgb([39, 47, 63], [178, 187, 183], s.daylight), cloud);
        horizon = rgb(horizon, rgb([55, 62, 69], [211, 206, 183], s.daylight), cloud);
        const storm = s.storminess;
        top = rgb(top, rgb([10, 17, 31], [24, 33, 50], s.daylight), storm * .95);
        middle = rgb(middle, rgb([21, 29, 43], [53, 65, 80], s.daylight), storm * .93);
        horizon = rgb(horizon, rgb([37, 45, 54], [107, 117, 117], s.daylight), storm * .86);
        this.horizon = horizon;
        const g = c.createLinearGradient(0, this.skyTop, 0, 530);
        g.addColorStop(0, css(top)); g.addColorStop(.55, css(middle)); g.addColorStop(1, css(horizon));
        this.rect(0, this.skyTop, 1440, 720 - this.skyTop, g);
        this.glow(1140, 307, 410, [255, 152, 91], s.twilight * (1 - s.cloud * .8) * .55);
    }

    celestial() {
        const c = this.ctx, s = this.state, t = this.elapsed;
        const moon = moonAppearance(s.moonElevation, s.elevation, s.cloud);
        const moonVisible = s.moonElevation > -12 && s.cloud < .96;
        // The moon masks stars and the Milky Way while preserving the sky
        // gradient, so its unlit side does not become a flat gray patch.
        c.save();
        if (moonVisible) {
            c.beginPath(); c.rect(0, this.skyTop, 1440, 720 - this.skyTop);
            c.moveTo(moon.x + moon.radius, moon.y);
            c.arc(moon.x, moon.y, moon.radius, 0, TAU);
            c.clip('evenodd');
        }
        if (s.milkyWay > .01) {
            c.save(); c.translate(835, this.skyY(180)); c.rotate(-.57);
            for (let i = 0; i < 22; i++) {
                const x = Math.sin(i * 1.7) * 28;
                this.glow(x, i * 30 - 390, 90 + Math.sin(i) * 20, [182, 184, 220], .025 * s.milkyWay);
            }
            c.restore();
        }
        if (s.stars > .01) {
            for (const p of this.stars) {
                const y = this.skyY(p.y);
                const a = (.5 + .2 * Math.sin(t * .6 + p.p)) * s.stars;
                this.ellipse(p.x, y, p.r, p.r, css([238, 234, 207], a));
                if (p.r > 1.2) {
                    this.line(p.x - 2.3, y, p.x + 2.3, y, css([234, 231, 218], a * .25), .5);
                    this.line(p.x, y - 2.3, p.x, y + 2.3, css([234, 231, 218], a * .25), .5);
                }
            }
        }
        const meteor = (t + 19) % 89;
        if (meteor < 1.4 && s.stars > .35) {
            const p = meteor / 1.4, x = 610 + p * 330, y = this.skyY(60) + p * 134;
            const g = c.createLinearGradient(x - 110, y - 44, x, y);
            g.addColorStop(0, '#f6efd500'); g.addColorStop(1, css([247, 241, 210], Math.sin(p * Math.PI) * s.stars));
            this.line(x - 110, y - 44, x, y, g, 1.8);
        }
        const satellite = (t + 7) % 267;
        if (satellite < 43 && s.stars > .5) this.ellipse(360 + satellite * 14, this.skyY(89) + satellite * 1.1, .9, .9, css([225, 231, 228], s.stars * .65));
        c.restore();
        if (s.elevation > -12 && s.cloud < .99) {
            const sun = sunAppearance(s.elevation), { x, y, radius } = sun;
            const visibility = 1 - smooth(.38, .99, s.cloud);
            const corona = rgb([255, 231, 165], [255, 132, 65], sun.warmth);
            this.glow(x, y, radius * 3.5, corona, .26 * visibility);
            const disk = c.createLinearGradient(0, y - radius, 0, y + radius);
            disk.addColorStop(0, css(rgb(sun.color, [255, 226, 142], .24 * sun.warmth), visibility));
            disk.addColorStop(.65, css(sun.color, visibility));
            disk.addColorStop(1, css(rgb(sun.color, [241, 129, 76], sun.warmth * .35), visibility));
            this.ellipse(x, y, radius, radius, disk);
            this.glow(x, y, radius * 1.7, corona, .1 * visibility);
        }
        if (moonVisible) {
            const { x, y, radius } = moon;
            this.glow(x, y, radius * 3.4, [225, 235, 224], s.moonLight * moon.contrast * moon.earthshine * .15);
            c.save(); c.translate(x, y); c.rotate(s.moonRotation * Math.PI / 180);
            c.globalAlpha = moon.contrast;
            const rim = c.createRadialGradient(0, 0, radius * .88, 0, 0, radius);
            rim.addColorStop(0, css([172, 193, 185], 0));
            rim.addColorStop(.8, css([172, 193, 185], .018 * moon.earthshine));
            rim.addColorStop(.96, css([172, 193, 185], .055 * moon.earthshine));
            rim.addColorStop(1, css([172, 193, 185], 0));
            this.ellipse(0, 0, radius, radius, rim);
            this.moonIllustration(radius, s.moonPhase);
            c.restore();
        }
    }

    moonIllustration(r, phase) {
        const c = this.ctx, k = (1 - Math.cos(phase * TAU)) / 2;
        c.save();
        // The outer rim and elliptical terminator clip the same drawing in
        // every phase, keeping craters and surface markings in place.
        const waxing = phase <= .5;
        c.beginPath();
        c.moveTo(0, -r);
        c.arc(0, 0, r, -Math.PI / 2, Math.PI / 2, !waxing);
        c.ellipse(0, 0, Math.max(.001, Math.abs(1 - 2 * k) * r), r, 0, Math.PI / 2, -Math.PI / 2, waxing === (k < .5));
        c.closePath(); c.clip();
        const glow = c.createLinearGradient(-r * .5, -r, r * .5, r);
        glow.addColorStop(0, '#e7dfb5'); glow.addColorStop(.58, '#cdd1ae'); glow.addColorStop(1, '#a6bca5');
        this.ellipse(0, 0, r, r, glow);
        c.scale(r / 50, r / 50);
        this.path('M-28-27Q-17-40-5-30Q7-30 3-18Q-17-1-24-9Q-37-13-28-27Z', '#7d9e893b');
        this.path('M12-22Q27-30 34-17Q44-9 35 0Q24 9 17-1Q7-5 12-22Z', '#6f99863b');
        this.path('M-13 5Q1-4 12 8Q16 21 1 23Q-5 36-19 26Q-30 17-13 5Z', '#85a28c30');
        this.path('M20 13Q35 8 37 24Q25 36 16 26Z', '#b0bfa038');
        for (const [x, y, radius] of [[-16, -19, 6], [24, -10, 5], [-24, 15, 4], [7, 29, 6.5], [29, 20, 3], [-5, -36, 2.3]]) {
            this.ellipse(x, y + .8, radius, radius * .86, '#78968729');
            this.ellipse(x + .5, y - .6, radius * .75, radius * .6, '#a6b79a30');
            c.beginPath(); c.ellipse(x, y, radius, radius * .87, -.2, Math.PI * 1.06, Math.PI * 1.78);
            c.strokeStyle = '#f2e8bf48'; c.lineWidth = 1; c.stroke();
        }
        this.path('M-35-14Q-39 0-33 12M13 36Q24 34 29 30', null, '#ece5bc25', 1.2);
        c.restore();
    }

    cloudLayer() {
        const c = this.ctx, s = this.state, t = this.elapsed;
        const count = Math.ceil(s.cloud * 15);
        for (let i = 0; i < count; i++) {
            const cloud = this.clouds[i];
            const x = ((cloud.x + this.cloudTravel * (i % 2 ? 1 : .7) + 240) % 1920) - 240;
            const opacity = clamp(s.cloud * 15 - i) * (.42 + s.cloud * .24 + s.storminess * .2);
            c.save(); c.translate(x, this.skyY(cloud.y)); c.scale(cloud.s, cloud.s * .75);
            const base = rgb([53, 64, 83], rgb([246, 239, 215], [72, 84, 103], s.storminess), s.daylight);
            const bottom = rgb([33, 45, 65], rgb([154, 178, 180], [40, 50, 68], s.storminess), s.daylight);
            const g = c.createLinearGradient(0, -40, 0, 75);
            g.addColorStop(0, css(rgb(base, [252, 185, 141], s.twilight * .6 * (1 - s.storminess)), opacity));
            g.addColorStop(.65, css(base, opacity)); g.addColorStop(1, css(bottom, opacity * .1));
            this.path('M-165 45 Q-180 13-133 8 Q-138-24-92-20 Q-65-65-22-33 Q20-69 66-33 Q116-50 123-3 Q173-11 179 29 Q209 62 137 66 L-123 68 Q-167 69-165 45Z', g);
            this.path('M-132 8 Q-99-2-75 12 M-22-33 Q0-21 2 3 M66-33 Q73-16 68-6', null, css([255, 239, 211], s.daylight * opacity * .19 * (1 - s.storminess)), 2);
            c.restore();
        }
        if (s.cloud > .83) {
            const g = c.createLinearGradient(0, this.skyTop, 0, 390);
            g.addColorStop(0, this.color([137, 157, 164], [32, 43, 59]));
            g.addColorStop(1, '#87959a00');
            c.save(); c.globalAlpha = smooth(.83, 1, s.cloud) * .8 * (1 - s.storminess);
            this.rect(0, this.skyTop, 1440, 390 - this.skyTop, g); c.restore();
        }
    }

    stormSky() {
        const c = this.ctx, s = this.state, event = this.stormEffect;
        if (s.storminess > .01) {
            c.save(); c.globalAlpha = s.storminess * .92;
            c.translate(Math.sin(this.cloudTravel * .003) * 18, this.skyY(168) - 168);
            const cloud = c.createLinearGradient(0, -40, 0, 250);
            cloud.addColorStop(0, this.color([27, 36, 54], [13, 21, 35]));
            cloud.addColorStop(.7, this.color([66, 77, 98], [30, 39, 56]));
            cloud.addColorStop(1, this.color([91, 101, 116], [45, 54, 70]));
            this.path('M-200-1000H1640V144Q1550 193 1450 157Q1330 225 1210 176Q1100 238 998 193Q879 259 765 202Q625 258 514 209Q408 244 314 193Q187 232 80 175Q-80 215-200 154Z', cloud);
            c.restore();
        }
        if (!event || event.flash <= .001) return;
        const x = event.kind === 'tree' ? STORM_TREE[0] - 110 : event.x;
        c.save(); c.translate(x, this.skyY(150)); c.scale(1, .48);
        this.glow(0, 0, 330, [204, 216, 255], event.flash * .55);
        this.glow(120, -35, 180, [236, 229, 255], event.flash * .35);
        c.restore();
        if (event.kind === 'bolt') this.lightningBolt(x, this.skyY(138), x - 85, 382);
    }

    lightningBolt(x, y, endX, endY) {
        const c = this.ctx, event = this.stormEffect;
        if (!event || event.flash <= .001) return;
        const random = seededRandom((this.options.seed ?? 73) + event.cycle * 991);
        const points = Array.from({ length: 13 }, (_, i) => {
            const t = i / 12;
            return [mix(x, endX, t) + (i && i < 12 ? (random() - .5) * 52 : 0), mix(y, endY, t)];
        });
        c.beginPath(); points.forEach(([px, py], i) => i ? c.lineTo(px, py) : c.moveTo(px, py));
        c.strokeStyle = css([153, 180, 239], event.flash * .5); c.lineWidth = 7; c.stroke();
        c.strokeStyle = css([245, 246, 255], event.flash); c.lineWidth = 2.3; c.stroke();
        for (const index of [4, 7]) {
            const [px, py] = points[index], side = index === 4 ? 1 : -1;
            c.beginPath(); c.moveTo(px, py); c.lineTo(px + side * 27, py + 13);
            c.lineTo(px + side * 20, py + 31); c.lineTo(px + side * 49, py + 51);
            c.strokeStyle = css([220, 230, 255], event.flash * .8); c.lineWidth = 1.2; c.stroke();
        }
    }

    hills() {
        const s = this.state;
        const snow = this.cover;
        const distant = rgb(this.horizon, this.litColor([114, 151, 162], [43, 65, 83]), .57);
        this.path('M0 365L82 337L148 276L184 290L231 253L291 308L348 327L418 288L467 303L529 240L558 256L611 303L670 339L746 287L779 302L823 267L880 315L945 339L1014 299L1040 314L1092 268L1156 317L1212 341L1286 279L1317 296L1360 256L1440 333V720H0Z', css(distant));
        const ridge = this.litColor([109, 140, 147], [36, 58, 73]);
        this.path('M0 397L91 360L168 331L237 350L318 293L344 301L426 367L478 350L549 301L579 312L654 371L712 356L770 319L841 359L905 345L971 366L1034 331L1109 351L1179 300L1209 314L1296 360L1359 319L1440 374V720H0Z', css(rgb(this.horizon, ridge, .72)));
        for (const path of ['M318 293L344 301L426 367L349 341Z', 'M549 301L579 312L654 371L574 345Z', 'M1179 300L1209 314L1296 360L1210 345Z']) {
            this.path(path, css(rgb(this.horizon, ridge, .9)));
        }
        const peakSnow = .18 + snow * .7 + (s.season === 'winter' ? .18 : 0);
        for (const path of ['M202 281L231 253L263 283L242 276L231 270L220 282L214 278Z', 'M502 270L529 240L558 256L582 280L551 268L534 258L522 270L515 264Z', 'M1332 284L1360 256L1390 285L1365 273L1354 278L1347 273Z']) {
            this.path(path, this.colorAlpha([224, 229, 214], [112, 136, 150], peakSnow));
        }
        this.path('M0 448Q171 391 347 427Q478 443 614 417Q790 394 968 434Q1196 389 1440 435V720H0Z', this.coveredColor([119, 148, 111], [36, 59, 61], .65));
        this.path('M83 435Q184 414 272 430M499 433Q582 422 632 423M1064 427Q1186 409 1314 425', null, this.colorAlpha([210, 211, 154], [102, 128, 120], .18 * (1 - snow)), 1);
        const forest = this.color([73, 111, 91], [28, 47, 53]);
        for (let i = 0; i < 95; i++) {
            const x = i * 15.4, y = 453 + Math.sin(i / 9) * 19, h = 10 + fract(Math.sin(i * 19) * 847) * 20;
            this.path(`M${x - 5} ${y}L${x} ${y - h}L${x + 7} ${y}Z`, forest);
        }
        const glow = this.ctx.createLinearGradient(0, 390, 0, 477);
        glow.addColorStop(0, css(this.horizon, .03)); glow.addColorStop(1, css(this.horizon, .15));
        this.rect(0, 390, 1440, 100, glow);
    }

    farLife() {
        const s = this.state, t = this.elapsed;
        if (s.activity < .3) return;
        const x = ((t * 2.2 + 207) % 950) + 50, y = 456;
        this.ctx.save(); this.ctx.translate(x, y); this.ctx.scale(.55, .55);
        this.rect(-16, -16, 26, 13, this.color([167, 82, 57]));
        this.rect(-12, -31, 17, 17, this.color([59, 79, 67]));
        this.rect(-9, -28, 11, 10, this.color([194, 211, 181]));
        this.ellipse(-11, -3, 9, 9, '#283d37'); this.ellipse(14, 0, 5, 5, '#283d37');
        this.ellipse(-11, -3, 3.5, 3.5, '#aaa48b'); this.ctx.restore();
    }

    land() {
        const s = this.state;
        let grass = rgb([134, 159, 90], [149, 136, 75], s.autumn);
        grass = rgb([139, 145, 121], grass, s.leaf);
        this.path('M0 509 Q170 450 350 503 Q490 530 627 486 Q810 464 985 503 Q1230 452 1440 520V720H0Z', this.coveredColor(grass, [30, 49, 44], .35));
        this.path('M0 515 Q116 474 248 492L173 563Q63 550 0 571Z', this.coveredColor([192, 171, 99], [48, 61, 44], .27));
        this.path('M28 521 Q110 497 211 501 M20 531Q107 506 200 509M6 544Q96 513 186 519 M0 555Q88 526 177 530', null, this.colorAlpha([150, 134, 77], [45, 57, 42], 1 - this.cover), 2);
        this.path('M1440 522Q1297 480 1144 507L1260 553Q1350 539 1440 568Z', this.coveredColor([175, 159, 100], [41, 56, 44], .3));
        this.path('M0 613Q168 554 316 575Q487 621 654 574Q833 546 1008 588Q1223 556 1440 619V720H0Z', this.coveredColor(rgb(grass, [79, 112, 70], .35), [23, 44, 39], .46));
        const seed = seededRandom(151);
        for (let i = 0; i < 165; i++) {
            const x = seed() * 1440, y = 511 + seed() * 175;
            const patch = css(rgb(this.litColor(i % 2 ? [217, 206, 140] : [63, 94, 57], i % 2 ? [90, 118, 85] : [10, 29, 27]), this.snowTone(i % 2 ? .05 : .8), this.cover), .09);
            this.ellipse(x, y, 2 + seed() * 8, .5 + seed() * 1.2, patch);
        }
        for (const [x, y, w, h] of [[130, 531, 125, 13], [442, 551, 87, 10], [795, 537, 137, 12], [1290, 539, 145, 17], [285, 641, 205, 24], [643, 624, 153, 17], [1325, 669, 160, 24]]) this.snowDrift(x, y, w, h);
        if (this.cover > .01) {
            for (const [curve, width] of [[STREET, 20], [LOWER_ROAD, 39], [EAST_ROAD, 32]]) {
                this.path(curvePath(curve), null, this.snowColor(.12, this.cover), width);
            }
        }
        const road = this.coveredColor([180, 164, 126], [59, 71, 55], .78);
        for (const [x, y, scale] of houses.filter(h => h[0] < 950)) {
            const doorX = x + 10 * scale, street = streetAtX(doorX);
            this.path(`M${doorX} ${y}Q${doorX + 4} ${(y + street.y) / 2} ${street.x} ${street.y}`, null, road, 3.5 * scale);
        }
        this.path('M699 521Q690 551 699 587M1034 534Q1067 564 1116 584L1156 590M1255 542Q1273 571 1233 605Q1196 618 1156 632', null, road, 4);
        this.path(curvePath(STREET), null, road, 13);
        this.path('M920 578Q947 580 963 610L985 646', null, road, 15);
        this.path(curvePath(LOWER_ROAD), null, road, 30);
        this.path(curvePath(EAST_ROAD), null, road, 23);
        this.path('M699 585L704 563Q741 559 779 563L784 585Z', this.coveredColor([168, 163, 137], [59, 72, 62], .7));
        this.path(STREAM, this.color([91, 146, 149], [37, 67, 76]));
        if (this.cover > .01) for (const side of [-1, 1]) {
            const bank = Array.from({ length: 49 }, (_, i) => riverPoint(i / 48, side));
            this.path(bank.map((p, i) => `${i ? 'L' : 'M'}${p.x.toFixed(2)} ${p.y.toFixed(2)}`).join(''), null, this.snowColor(.08, this.cover), 4);
        }
        this.ctx.save(); this.ctx.clip(new Path2D(STREAM));
        for (let i = 0; i < 31; i++) {
            const { x, y } = riverPoint(.12 + i * .027, Math.sin(i * 2.3) * .55);
            const w = 7 + Math.sin(this.elapsed * .7 + i) * 4;
            this.line(x - w, y, x + w, y, this.color([182, 197, 165], [81, 105, 107]), .7);
        }
        if (!s.storm) for (let i = 0; i < 2; i++) {
            const { x, y } = riverPoint(.57 + i * .07 + Math.sin(this.elapsed * .04) * .09, i ? .25 : -.2);
            this.ellipse(x, y, 4, 2, this.color([192, 175, 127], [98, 119, 107]));
            this.ellipse(x + 3, y - 2.6, 1.7, 1.7, this.color([65, 105, 72], [55, 86, 72]));
            this.line(x + 4, y - 2.5, x + 6, y - 2.5, this.color([207, 161, 87], [120, 131, 83]), 1);
            this.line(x - 9, y + 2, x - 4, y + 2, this.colorAlpha([219, 222, 186], [86, 119, 119], .4), .6);
        }
        this.ctx.restore();
        const b = BRIDGE;
        // The arch spans the stream, with both abutments on its banks.
        // Draw water and ducks first so they pass beneath the bridge.
        this.path(`M${b.left} ${b.front}H${b.right}V${b.base}H${b.archRight}Q1050 638 ${b.archLeft} ${b.base}H${b.left}Z`, this.color([154, 146, 122], [64, 80, 74]));
        this.path(`M${b.left} ${b.front}L${b.left + 5} ${b.back}H${b.right - 5}L${b.right} ${b.front}Z`, this.coveredColor([196, 183, 151], [97, 105, 89], .65));
        this.path(`M${b.archLeft} ${b.base}Q1050 638 ${b.archRight} ${b.base}`, null, this.color([187, 174, 140], [91, 102, 85]), 2.5);
        for (let x = b.left + 10; x < b.right; x += 15) {
            this.line(x, b.back + 1, x, b.front, this.colorAlpha([126, 123, 96], [38, 59, 52], .28), .7);
        }
        for (const y of [b.back, b.front]) {
            this.line(b.left + 4, y - 13, b.right - 4, y - 13, this.color([199, 188, 151], [108, 112, 94]), 2.3);
            for (let x = b.left + 4; x < b.right; x += 17) this.line(x, y, x, y - 13, this.color([116, 112, 91], [69, 77, 68]), 1.6);
            if (this.cover > .01) this.line(b.left + 4, y - 15, b.right - 4, y - 15, this.snowColor(.1, this.cover), 3);
        }
        if (this.wet > .01) {
            for (const { x, y } of [.15, .34, .52, .69, .85].map(t => curvePoint(LOWER_ROAD, t)).concat([.22, .48, .73].map(t => curvePoint(EAST_ROAD, t)))) {
                this.ellipse(x, y, 9 + x % 7, 1.5, css(this.horizon, this.wet * .3));
            }
        }
        const fox = (this.elapsed + 91) % 283;
        if (fox < 18 && s.daylight < .5 && !s.storm) {
            const x = 170 + fox * 11, y = 492;
            this.cat(x, y, .8, true);
            this.path(`M${x - 3} ${y - 4}Q${x - 14} ${y - 9} ${x - 16} ${y - 3}L${x - 7} ${y - 1}Z`, this.color([174, 112, 61], [107, 104, 65]));
        }
    }

    house(x, y, scale, type) {
        const c = this.ctx, s = this.state;
        c.save(); c.translate(x, y); c.scale(scale, scale);
        if (s.elevation > 0 && s.cloud < .8) {
            const length = 8 + (1 - smooth(1, 45, s.elevation)) * 105;
            const dx = (x < 1140 ? -1 : 1) * length;
            this.path(`M-43 0H55L${55 + dx} ${5 + length * .14}H${-43 + dx}Z`, css([31, 59, 45], s.daylight * (1 - s.cloud) * .12));
        }
        this.ellipse(7, 1, 68, 6, this.coveredColor([65, 92, 63], [14, 33, 31], .95));
        const plaster = [[232, 211, 164], [212, 204, 167], [209, 178, 139], [222, 216, 182]][type];
        this.path('M-43-62H30V0H-43Z', this.color(plaster, [76, 81, 69]));
        this.path('M30-62L55-52V0H30Z', this.color(rgb(plaster, [99, 105, 87], .35), [53, 66, 57]));
        this.path('M-51-60L-7-99L39-60Z', this.color([139, 88, 65], [51, 59, 54]));
        this.path('M-7-99L21-92L64-53L39-60Z', this.color([109, 82, 65], [40, 51, 47]));
        this.line(-51, -60, 39, -60, this.color([225, 194, 146], [90, 94, 75]), 2);
        for (let row = 0; row < 4; row++) {
            const yRoof = -65 - row * 7;
            this.line(-42 + row * 8, yRoof, 30 - row * 8, yRoof, this.color([113, 78, 61], [47, 57, 52]), .65);
        }
        this.rect(20, -95, 8, 20, this.color([157, 127, 91], [59, 69, 57]));
        this.rect(18, -96, 12, 3, this.color([184, 157, 120], [74, 82, 63]));
        if (s.temperature !== null && s.temperature < 15 && (s.hour < 10 || s.hour > 16)) this.smoke(24, -99, x);
        if (type === 1) {
            this.line(-42, -29, 29, -29, this.color([112, 92, 65], [46, 57, 48]), 3);
            this.line(-6, -59, -6, -1, this.color([112, 92, 65], [46, 57, 48]), 3);
            this.line(-41, -57, -7, -30, this.color([112, 92, 65], [46, 57, 48]), 2);
        }
        this.rect(3, -28, 14, 28, this.color([68, 100, 84], [31, 48, 44]));
        this.rect(5, -25, 9, 11, this.color([84, 115, 93], [40, 57, 46]));
        this.ellipse(13, -12, 1, 1, '#d4b87d');
        this.rect(-1, 0, 23, 3, this.color([193, 184, 151], [77, 83, 68]));
        const positions = [[-30, -49], [5, -49], [-29, -23], [38, -39]];
        positions.forEach(([wx, wy], i) => this.window(wx, wy, x + i, i === 3 ? 8 : 12));
        for (const wx of [-30, 5]) {
            this.rect(wx - 5, -49, 3, 13, this.color([95, 125, 95], [47, 66, 47]));
            this.rect(wx + 14, -49, 3, 13, this.color([95, 125, 95], [47, 66, 47]));
        }
        if (s.leaf > .2 && this.cover < .3) {
            for (const wx of [-30, 5]) {
                this.rect(wx - 3, -31, 19, 4, this.color([121, 79, 55], [38, 52, 41]));
                for (let k = 0; k < 6; k++) this.ellipse(wx + k * 2.7, -33 - k % 2, 2.1, 2.2, this.color(s.blossom > .4 ? [239, 185, 179] : [189, 109, 102], [66, 67, 59]));
            }
        }
        if (type === 3) {
            this.path('M-44-29H-4L-1-22H-48Z', this.color([150, 98, 72], [58, 66, 55]));
            this.rect(-45, -22, 40, 3, this.color([234, 209, 151], [100, 105, 77]));
        }
        if (this.cover > .01) {
            c.globalAlpha = this.cover;
            this.path('M-7-102Q8-100 22-95L65-57Q69-51 62-51L38-57Z', this.snowColor(.4));
            this.path('M-52-62Q-34-80-10-101Q-7-105-3-101L40-64Q44-58 38-57Q30-54 23-57Q15-54 8-57Q0-53-9-56Q-17-53-25-56Q-33-53-40-56Q-52-53-52-62Z', this.snowColor(.05));
            this.line(18, -98, 30, -98, this.snowColor(), 4);
            for (const [wx, wy] of positions) this.line(wx - 2, wy + 14, wx + 13, wy + 14, this.snowColor(.15), 2.5);
            if (type === 3) this.path('M-47-30Q-28-34-5-30L-1-23Q-15-20-26-22Q-40-19-49-23Z', this.snowColor(.1));
            if (s.temperature !== null && s.temperature < 0) for (let i = 0; i < 5; i++) this.line(-31 + i * 13, -55, -31 + i * 13, -50 + i % 3, this.snowColor(.35), 1);
            c.globalAlpha = 1;
        }
        c.restore();
    }

    window(x, y, index, width = 12) {
        const dark = 1 - smooth(-5, 9, this.state.elevation);
        const light = windowLight(index, this.state.hour, dark, this.elapsed);
        this.rect(x - 2, y - 2, width + 4, 17, this.color([185, 168, 127], [67, 77, 61]));
        this.rect(x, y, width, 13, this.color([92, 133, 136], [26, 46, 45]));
        if (light > .02) {
            this.glow(x + width / 2, y + 7, 30, [255, 198, 103], light * .14);
            this.rect(x, y, width, 13, css([255, 215, 139], light));
            this.rect(x + 1, y + 1, 2, 11, css([255, 238, 192], light * .6));
            const shadow = Math.sin(this.elapsed / 11 + index);
            if (shadow > .98) this.ellipse(x + width / 2, y + 9, 2, 4, css([73, 74, 52], light * .6));
        }
        this.line(x + width / 2, y, x + width / 2, y + 13, this.color([179, 160, 119], [83, 88, 64]), 1.3);
        this.line(x, y + 5, x + width, y + 5, this.color([179, 160, 119], [83, 88, 64]), 1);
    }

    church(x, y, scale) {
        const c = this.ctx;
        c.save(); c.translate(x, y); c.scale(scale, scale);
        this.path('M-17-116H18V0H-17Z', this.color([224, 216, 178], [94, 99, 77]));
        this.path('M18-116L27-107V0H18Z', this.color([181, 180, 145], [67, 83, 65]));
        this.path('M-25-116L0-159L26-116Z', this.color([80, 103, 87], [33, 53, 49]));
        this.path('M0-159L10-148L32-111L26-116Z', this.color([64, 85, 77], [27, 45, 46]));
        this.line(0, -174, 0, -156, this.color([204, 185, 134], [160, 161, 117]), 1.5);
        this.line(-5, -168, 5, -168, this.color([204, 185, 134], [160, 161, 117]), 1.5);
        this.path('M27-55H84V0H27Z', this.color([214, 205, 167], [78, 90, 70]));
        this.path('M19-54L53-84L94-54Z', this.color([113, 101, 74], [45, 63, 49]));
        this.path('M-6 0V-23Q0-31 6-23V0Z', this.color([86, 95, 71], [32, 48, 36]));
        this.window(-5, -66, 711, 10); this.window(40, -35, 715, 9); this.window(63, -35, 719, 9);
        this.ellipse(0, -94, 9, 9, this.color([239, 226, 173], [195, 185, 117]));
        this.ellipse(0, -94, 7.3, 7.3, this.color([218, 209, 158], [167, 163, 107]));
        const hour = this.state.hour, hand = hour % 12 / 12 * TAU, minute = hour % 1 * TAU;
        this.line(0, -94, Math.sin(hand) * 4.8, -94 - Math.cos(hand) * 4.8, '#495b48', 1.1);
        this.line(0, -94, Math.sin(minute) * 6.5, -94 - Math.cos(minute) * 6.5, '#495b48', .9);
        if (this.cover > .01) {
            c.globalAlpha = this.cover;
            this.path('M-26-117L-2-160Q0-164 3-159L27-118Q30-113 23-114Q14-111 5-114Q-5-111-13-114Q-27-110-26-117Z', this.snowColor(.24));
            this.path('M18-56L51-86Q54-89 57-85L95-57Q99-52 91-51Q80-48 70-52Q58-48 47-51Q35-48 25-51Q15-49 18-56Z', this.snowColor(.08));
            c.globalAlpha = 1;
        }
        c.restore();
    }

    smoke(x, y, phase) {
        const s = this.state;
        for (let i = 0; i < 5; i++) {
            const p = ((this.elapsed * .13 + i / 5 + phase) % 1);
            this.ellipse(x + p * (s.wind * 4 + 8), y - p * 57, 3 + p * 11, 3 + p * 8, this.colorAlpha([214, 214, 192], [133, 144, 135], (1 - p) * .16));
        }
    }
    colorAlpha(day, night, opacity) { return css(this.litColor(day, night), opacity); }

    treeSway(x) {
        return Math.sin(this.elapsed * .8 + x) * this.state.wind * .0017
            + Math.sin(this.elapsed * 1.9 + x * .1) * this.state.wind * .0008;
    }

    treeFire() {
        const c = this.ctx, event = this.stormEffect;
        if (!event || event.kind !== 'tree' || event.fire + event.smoke <= .001) return;
        c.save(); c.translate(0, TREE_STRIKE_Y);
        this.glow(0, 3, 43, [255, 160, 64], event.fire * .55);
        for (let i = 0; i < 5; i++) {
            const x = (i - 2) * 4, height = 12 + 7 * Math.sin(this.elapsed * 9 + i * 2);
            this.path(`M${x - 4} 13Q${x - 9} 1 ${x + 3} ${-height}Q${x + 1} -2 ${x + 7} 3Q${x + 10} 12 ${x - 4} 13Z`, css([250, 116 + i * 16, 39], event.fire * .9));
            this.ellipse(x + 1, 8, 2.3, 6, css([255, 228, 137], event.fire * .9));
        }
        for (let i = 0; i < 4; i++) {
            const p = fract(this.elapsed * .65 + i * .26);
            this.ellipse(Math.sin(i * 9 + this.elapsed) * 10, -8 - p * 30, .8, 1.3, css([255, 211, 119], event.fire * (1 - p)));
            this.ellipse(p * 16, -12 - p * 54, 4 + p * 9, 4 + p * 7, css([135, 141, 144], event.smoke * (1 - p) * .38));
        }
        c.restore();
    }

    tree(x, y, scale, evergreen = false) {
        const c = this.ctx, s = this.state;
        c.save(); c.translate(x, y); c.scale(scale, scale);
        this.ellipse(0, 2, 28, 5, this.colorAlpha([64, 87, 53], [15, 34, 31], .38));
        const sway = this.treeSway(x);
        c.transform(1, 0, sway, 1, 0, 0);
        this.path('M-3 0L-2-64L-18-83M-1-43L21-68M-2-60L3-99M1-74L20-91M-1-29L-22-54', null, this.color([102, 89, 60], [40, 58, 43]), 3.4);
        this.path('M-18-82L-28-84M-18-81L-20-94M21-68L30-79M20-69L29-70M-21-53L-31-57', null, this.color([119, 102, 69], [43, 62, 46]), 1.3);
        if (evergreen) {
            this.path('M0-115L-18-73L-10-75L-28-45L-18-49L-33-17H33L18-49L28-45L10-75L18-73Z', this.color([59, 98, 75], [21, 49, 42]));
            this.path('M0-109L-9-75L0-78L-16-47L-3-53L-20-23H-6L0-50Z', this.color([90, 125, 88], [33, 65, 49]));
            if (this.cover > .01) {
                c.globalAlpha = this.cover;
                this.path('M-18-75L-2-116Q0-120 3-114L19-76Q22-71 14-71Q7-67 1-72Q-8-68-14-71Q-22-70-18-75Z', this.snowColor(.1));
                this.path('M-28-48L-10-77Q0-84 10-76L29-48Q34-41 24-41Q16-36 7-41Q-4-36-13-41Q-24-37-30-42Z', this.snowColor(.17));
                this.path('M-33-20L-21-43Q-12-48 0-47Q13-49 23-39L34-20Q38-14 28-14Q18-9 7-15Q-5-9-17-14Q-31-9-36-15Z', this.snowColor(.25));
                c.globalAlpha = 1;
            }
        } else if (s.leaf > .02) {
            const random = seededRandom(Math.round(x));
            for (let i = 0; i < 23; i++) {
                const a = random() * TAU, r = Math.sqrt(random()) * 26;
                const leaf = rgb([93 + random() * 37, 130 + random() * 25, 65 + random() * 20], [172 + random() * 45, 101 + random() * 49, 48 + random() * 26], s.autumn);
                const col = rgb(leaf, [230, 178, 166], s.blossom * (i % 3 ? .35 : .85));
                c.globalAlpha = s.leaf;
                this.ellipse(Math.cos(a) * r, -76 + Math.sin(a) * r * .85, 11 + random() * 9, 12 + random() * 8, this.color(col, rgb([33, 57, 44], [55, 62, 40], s.autumn)));
                if (i % 3 === 0) this.ellipse(Math.cos(a) * r - 3, -81 + Math.sin(a) * r * .85, 7, 4, this.colorAlpha([206, 193, 118], [100, 115, 71], .15));
            }
            c.globalAlpha = 1;
        }
        if (!evergreen && this.cover > .01) {
            c.globalAlpha = this.cover;
            this.path('M-2-65L-18-85L-28-86M-1-45L21-70L30-81M1-76L20-93M-1-31L-22-56L-31-59', null, this.snowColor(.18), 3);
            c.globalAlpha = 1;
        }
        if (x === STORM_TREE[0] && y === STORM_TREE[1]) this.treeFire();
        this.snowDrift(1, 2, 24, 5);
        c.restore();
    }

    details() {
        const c = this.ctx, s = this.state, t = this.elapsed;
        const wood = this.color([158, 131, 89], [60, 77, 57]);
        for (const [start, end, y] of fences) {
            for (let x = start; x <= end; x += 11) this.line(x, y, x, y - 14, wood, 2);
            this.line(start, y - 5, end, y - 5, wood, 1.8); this.line(start, y - 11, end, y - 11, wood, 1.8);
            if (this.cover > .01) {
                this.line(start, y - 12.5, end, y - 12.5, this.snowColor(.15, this.cover), 2.5);
                for (let x = start; x <= end; x += 11) this.line(x - 1, y - 15, x + 1, y - 15, this.snowColor(.05, this.cover), 3);
            }
        }
        // Seed beds, a trellis and the small weather garden sit in front of the farm.
        for (let row = 0; row < 3; row++) {
            this.path(`M${374 + row * 2} ${539 + row * 6}l33 1-3 4-33-1Z`, this.coveredColor([126, 99, 61], [39, 53, 36], .42));
            for (let i = 0; i < 6; i++) if (s.leaf > .4 && this.cover < .2) this.ellipse(377 + i * 5 + row * 2, 540 + row * 6, 2.1, 1.4, this.color([113, 150, 66], [47, 75, 42]));
        }
        this.line(418, 554, 418, 522, wood, 2);
        this.rect(412, 527, 13, 7, this.color([234, 229, 206], [138, 153, 141]));
        this.line(418, 522, 418, 516, wood, 1);
        for (let i = 0; i < 3; i++) {
            const a = t * s.wind * 2 + i * TAU / 3;
            this.line(418, 516, 418 + Math.cos(a) * 8, 516 + Math.sin(a) * 2.5, wood, 1);
            this.ellipse(418 + Math.cos(a) * 8, 516 + Math.sin(a) * 2.5, 2, 1.2, wood);
        }
        this.line(502, 559, 502, 529, wood, 2); this.line(548, 559, 548, 531, wood, 2);
        this.path('M502 531Q525 537 548 533', null, wood, 1);
        if (s.daylight > .4 && !(s.rainRate > 0) && !s.storm && s.temperature > 10) {
            for (let i = 0; i < 4; i++) {
                c.save(); c.translate(510 + i * 10, 534); c.rotate(Math.sin(t * 1.8 + i) * s.wind * .017);
                this.path('M-4 0H4L6 12Q0 15-5 12Z', this.color(i % 2 ? [208, 166, 140] : [230, 225, 197], [72, 81, 70])); c.restore();
            }
        }
        this.rect(714, 573, 37, 3, wood);
        for (const x of [718, 747]) { this.line(x, 574, x, 582, wood, 2); this.line(x, 563, x, 574, wood, 1.5); }
        this.line(713, 563, 752, 563, wood, 3); this.line(713, 568, 752, 568, wood, 2.5);
        if (this.cover > .01) {
            this.line(712, 561, 753, 561, this.snowColor(.1, this.cover), 4);
            this.line(713, 571, 752, 571, this.snowColor(.15, this.cover), 4);
        }
        this.line(767, 582, 767, 548, wood, 1.8); this.ellipse(767, 546, 5.5, 5.5, this.color([210, 194, 125], [114, 125, 77]));
        this.line(765, 543, 765, 549, this.color([87, 116, 67]), 1); this.line(769, 543, 769, 549, this.color([87, 116, 67]), 1); this.line(765, 546, 769, 546, this.color([87, 116, 67]), 1);
        for (const { x, y, scale } of lamps) this.lamp(x, y, scale);
        // A parked bicycle remains visible even when nobody is out riding.
        this.bike(851, 563, .65, false);
    }

    lamp(x, y, scale) {
        const c = this.ctx, s = this.state;
        const light = 1 - smooth(-5 + (x % 7) * .15, 3 + (x % 7) * .15, s.elevation);
        c.save(); c.translate(x, y); c.scale(scale, scale);
        if (light > .01) {
            const g = c.createLinearGradient(0, -45, 0, 0);
            g.addColorStop(0, css([255, 220, 137], light * .16)); g.addColorStop(1, css([255, 207, 118], light * .015));
            this.path('M-3-45L-24 1Q0 9 24 1L3-45Z', g);
            this.ellipse(0, 1, 24, 5, css([237, 200, 107], light * .1));
            this.glow(0, -45, 37 + s.fog * 40, [255, 204, 113], light * (.18 + s.fog * .09));
            if (this.wet > 0) this.ellipse(0, 9, 3, 13, css([241, 197, 105], light * this.wet * .13));
        }
        this.line(0, 0, 0, -42, this.color([86, 98, 78], [64, 84, 72]), 2.2);
        this.path('M-4-49H4L3-41H-3Z', this.color([209, 194, 141], [159, 158, 109]));
        this.rect(-2.5, -48, 5, 6, css([255, 225, 153], light));
        this.path('M-6-49L0-53L6-49Z', this.color([84, 99, 79], [56, 78, 68]));
        if (this.cover > .01) this.path('M-7-50Q-4-57 1-56Q5-55 7-50Q2-48-2-49Q-5-47-7-50Z', this.snowColor(.08, this.cover));
        c.restore();
    }

    person(x, y, scale, index, umbrella = false, standing = false) {
        const c = this.ctx, s = this.state, t = this.elapsed;
        c.save(); c.translate(x, y); c.scale(scale, scale);
        const walk = standing ? 0 : Math.sin(t * 5 + index) * 3.4;
        this.ellipse(0, 0, 4.5, 1.1, '#162e3433');
        this.line(0, -8, -walk, 0, this.color([73, 80, 68], [33, 46, 44]), 1.8);
        this.line(0, -8, walk, 0, this.color([63, 73, 64], [28, 44, 41]), 1.8);
        this.path('M-2-17Q0-19 3-16L4-8H-3Z', this.color(index % 2 ? [165, 91, 63] : [64, 115, 118], [68, 81, 70]));
        this.ellipse(0, -20, 2.4, 2.7, this.color([221, 182, 137], [148, 149, 115]));
        this.line(1, -15, 5 + walk * .4, -10, this.color([187, 150, 113], [89, 104, 84]), 1.3);
        if (s.season === 'winter') { this.rect(-3, -23, 6, 2, this.color([153, 91, 66], [97, 91, 62])); this.ellipse(0, -25, 1.2, 1.2, this.color([214, 189, 140], [137, 140, 99])); }
        if (umbrella) {
            this.line(5, -10, 5, -31, this.color([199, 184, 138], [143, 149, 116]), .9);
            this.path('M-6-29Q4-43 16-29Q11-31 7-28Q2-31-1-28Z', this.color(index % 2 ? [197, 140, 76] : [115, 133, 154], [101, 108, 104]));
        }
        c.restore();
    }

    bike(x, y, scale, rider, direction = 1) {
        const c = this.ctx, t = this.elapsed;
        c.save(); c.translate(x, y); c.scale(scale * direction, scale);
        const metal = this.color([67, 89, 78], [57, 83, 75]);
        for (const xw of [-9, 10]) { this.ellipse(xw, -4, 5.4, 5.4, metal); this.ellipse(xw, -4, 4.3, 4.3, this.color([151, 163, 125], [53, 75, 60])); }
        this.path('M-9-4L-3-13L3-4L-9-4M-3-13H6L3-4L10-4L6-16L10-17M-5-14H0', null, this.color([158, 112, 69], [119, 113, 76]), 1.2);
        if (rider) {
            this.ellipse(1, -28, 2.4, 2.5, this.color([220, 184, 137], [156, 152, 118]));
            this.line(-4, -15, 0, -24, this.color([109, 124, 169], [69, 92, 109]), 4);
            this.line(0, -23, 8, -17, this.color([220, 184, 137], [132, 144, 111]), 1.5);
            this.line(-4, -14, 1 + Math.sin(t * 5) * 3, -7, metal, 2);
        }
        c.restore();
    }

    people() {
        const s = this.state, t = this.elapsed;
        if (s.daylight < .15 && (s.hour > 23 || s.hour < 5)) return;
        if (s.activity > .035 || s.hour > 17 && s.hour < 22) {
            const rain = s.rainRate > 0;
            const trip = (this.walkTravel + 162) % 820, direction = trip < 410 ? 1 : -1;
            const progress = .44 + (trip < 410 ? trip : 820 - trip) / 410 * .46;
            const { x, y } = curvePoint(STREET, progress, -1);
            this.person(x, y, .9, 1, rain);
            if (!rain && !s.storm) {
                const dog = curvePoint(STREET, progress + direction * .025, -1);
                this.line(x + 4, y - 9, dog.x, dog.y - 4, this.color([157, 143, 103], [86, 104, 80]), .6);
                this.cat(dog.x, dog.y, .8, true);
            }
        }
        if (s.activity > .5) {
            const trip = (t * 10 + 187) % 1320, direction = trip < 660 ? 1 : -1;
            const cyclist = curvePoint(STREET, .18 + (trip < 660 ? trip : 1320 - trip) / 660 * .74, 2);
            this.bike(cyclist.x, cyclist.y - 1, .8, true, direction);
            this.person(365, 552, .7, 4, false, true);
            if (!(s.rainRate > 0) && this.cover < .1) {
                this.line(369, 543, 381, 548 + Math.sin(t), this.color([138, 162, 171]), 1.3);
                for (let i = 0; i < 4; i++) this.ellipse(381 + i, 549 + (t * 7 + i) % 4, .4, .8, this.colorAlpha([205, 219, 207], [73, 98, 92], .6));
            }
        }
        if (s.stars > .55 && s.hour >= 20 && s.hour <= 23) {
            this.person(1260, 628, .83, 0, false, true);
            this.line(1272, 627, 1277, 610, this.color([156, 155, 123]), 1); this.line(1282, 627, 1277, 610, this.color([156, 155, 123]), 1);
            this.line(1272, 612, 1287, 604, this.color([180, 190, 170], [130, 158, 153]), 4);
        }
    }

    cat(x, y, scale, dog = false) {
        const c = this.ctx, t = this.elapsed;
        c.save(); c.translate(x, y); c.scale(scale, scale);
        const col = this.color(dog ? [153, 115, 74] : [77, 82, 68], dog ? [101, 106, 74] : [46, 66, 53]);
        this.ellipse(0, -4, 5, 2.6, col); this.ellipse(5, -6, 2.6, 2.4, col);
        this.path('M3-8L3-11L5-9L7-11L8-7Z', col);
        this.line(-4, -4, -3 + Math.sin(t * 5), 0, col, 1.2); this.line(3, -4, 4 - Math.sin(t * 5), 0, col, 1.2);
        this.path(dog ? 'M-5-5Q-10-6-8-9' : 'M-5-5Q-12-11-8-12', null, col, 1.4);
        c.restore();
    }

    animals() {
        const c = this.ctx, s = this.state, t = this.elapsed;
        if (s.daylight > .3 && !s.storm && s.rain < .15) {
            for (let i = 0; i < (s.season === 'winter' ? 2 : 7); i++) {
                const x = ((t * (14 + i * 1.3) + i * 193) % 1680) - 120;
                const y = 246 + Math.sin(t * .17 + i) * 22 + i % 3 * 24;
                const flap = Math.sin(t * 6 + i) * 3;
                this.path(`M${x - 5} ${y + flap}Q${x - 2} ${y - 2} ${x} ${y}Q${x + 2} ${y - 2} ${x + 5} ${y + flap}`, null, this.color([65, 86, 77], [49, 64, 59]), 1.2);
            }
            // Butterflies stay in the gardens to avoid crossing dashboard readings.
            if (s.month > 4.5 && s.month < 9.6 && s.wind < 6 && s.temperature > 12) for (let i = 0; i < 4; i++) {
                const x = 381 + i * 67 + Math.sin(t * .47 + i) * 19, y = 555 + Math.sin(t * 1.2 + i) * 8;
                this.ellipse(x, y, 1 + Math.abs(Math.sin(t * 10)) * 2.3, 1.8, this.color(i % 2 ? [225, 190, 109] : [222, 221, 193]));
            }
        }
        this.cat(827 + Math.sin(t * .025) * 15, 546, .8);
        if (s.night > .6) {
            const owl = (t + 50) % 171;
            if (owl < 150) {
                this.ellipse(1045, 454, 3.2, 4.3, '#697764');
                this.ellipse(1044, 453, .7, .8, '#d4c688'); this.ellipse(1047, 453, .7, .8, '#d4c688');
            } else {
                const x = 1045 + (owl - 150) * 16, y = 454 - (owl - 150) * 6;
                this.path(`M${x - 8} ${y + Math.sin(t * 7) * 6}Q${x} ${y - 5} ${x + 8} ${y + Math.sin(t * 7) * 6}`, null, '#6c7a69', 2);
            }
        }
        if (s.fireflies) for (let i = 0; i < 14; i++) {
            const x = 1070 + Math.sin(t * .24 + i * 12) * 110, y = 600 + Math.cos(t * .34 + i * 6) * 30;
            const a = smooth(.1, .95, Math.sin(t * .7 + i));
            this.glow(x, y, 6, [216, 229, 134], a * .2);
            this.ellipse(x, y, .9, .9, css([230, 237, 154], a * .8));
        }
    }

    fogLayer(alpha, y) {
        const s = this.state;
        if (s.fog < .01) return;
        for (let i = 0; i < 5; i++) {
            const x = 100 + i * 315 + Math.sin(this.elapsed * .025 + i) * 100;
            const c = this.ctx, g = c.createRadialGradient(x, y + i % 2 * 20, 0, x, y + i % 2 * 20, 230);
            g.addColorStop(0, this.colorAlpha([219, 224, 205], [141, 158, 157], s.fog * alpha));
            g.addColorStop(1, '#dbe0cd00');
            c.save(); c.translate(0, y); c.scale(1, .22); c.translate(0, -y);
            this.ellipse(x, y, 300, 230, g); c.restore();
        }
    }

    precipitation() {
        const c = this.ctx, s = this.state, t = this.elapsed;
        const rain = s.rain, snow = s.snow;
        const weather = precipitationAppearance(s.rainRate, snow, s.sleet);
        const fallHeight = 770 - this.skyTop;
        const count = weather.snowCount + weather.rainCount;
        for (let i = 0; i < count; i++) {
            const p = this.particles[i], flake = i < weather.snowCount;
            const speed = flake ? 22 + p.z * 34 : weather.speed * (.7 + p.z * .6);
            const y = (p.y * fallHeight + t * speed) % fallHeight + this.skyTop - 25;
            const drift = s.wind * (flake ? 3 : 8) * (Math.sin(s.windDirection * Math.PI / 180) > 0 ? -1 : 1);
            const x = ((p.x * 1640 + this.windTravel * (flake ? 3 : 8) + (flake ? Math.sin(t + p.p) * 14 : 0)) % 1640 + 1640) % 1640 - 100;
            const quiet = x < 600 && this.options.quietLeft ? .65 : 1;
            if (flake) {
                const radius = .7 + p.z * 2.3;
                this.ellipse(x, y, radius, radius, css([243, 247, 244], quiet * (.3 + p.z * .48) * snow));
            } else {
                const length = weather.length * (.65 + p.z * .65);
                this.line(x, y, x - drift / speed * length, y - length,
                    css([199, 222, 231], quiet * weather.alpha * (.6 + p.z * .55)), weather.width * (.65 + p.z * .6));
            }
        }
        if (weather.rainCount > 0) {
            for (let i = 0; i < Math.ceil(4 + weather.intensity * 44); i++) {
                const p = fract(t * .9 + i * .172), point = curvePoint(i % 2 ? LOWER_ROAD : EAST_ROAD, .2 + (i % 7) * .1, (i % 3 - 1) * 5);
                const x = point.x, y = point.y + GROUND_OFFSET;
                c.beginPath(); c.ellipse(x, y, 1 + p * 7, .5 + p * 1.4, 0, 0, TAU);
                c.strokeStyle = css([210, 225, 231], (1 - p) * (.08 + weather.intensity * .45)); c.lineWidth = .6 + weather.intensity * .5; c.stroke();
            }
        }
        const rainbow = this.wet > .1 && s.elevation > 2 && s.elevation < 35 && s.cloud < .5 && rain < .2 && !snow;
        if (rainbow) {
            const colors = [[216, 119, 115], [221, 167, 109], [217, 199, 120], [144, 178, 139], [122, 161, 182], [153, 144, 183]];
            colors.forEach((color, i) => {
                c.beginPath(); c.arc(840, 483, 223 - i * 3, Math.PI * 1.08, Math.PI * 1.92);
                c.strokeStyle = css(color, this.wet * .13); c.lineWidth = 4; c.stroke();
            });
        }
    }

    foreground() {
        const s = this.state, t = this.elapsed;
        const col = this.color(rgb([76, 111, 62], [143, 118, 65], s.autumn), [23, 48, 36]);
        this.ctx.save(); this.ctx.translate(0, -GROUND_OFFSET);
        for (let i = 0; i < 90; i++) {
            if (this.cover > .5 && i % 9 !== 0) continue;
            const x = i * 16.3, y = 705 + Math.sin(i * 1.7) * 8, h = 7 + fract(Math.sin(i * 44) * 89) * 12;
            if (x > 660 && x < 1195) continue;
            const sway = Math.sin(t * 1.6 + i * .13) * s.wind * .8;
            this.path(`M${x} 727Q${x - 2} ${y + h} ${x + sway} ${y}`, null, col, 1.3);
            if (s.month > 4 && s.month < 10 && i % 5 === 0 && this.cover < .2) {
                this.ellipse(x + sway, y, 2.4, 1.7, this.color(s.month < 6 ? [228, 196, 184] : [222, 199, 112], [81, 91, 58]));
                this.ellipse(x + sway, y, .8, .8, this.color([195, 158, 68], [98, 107, 65]));
            }
        }
        this.snowDrift(153, 718, 175, 14);
        this.snowDrift(453, 721, 189, 18);
        this.snowDrift(1362, 720, 155, 19);
        this.ctx.restore();
        if (s.autumn > .1 || s.blossom > .3) for (let i = 0; i < 18; i++) {
            const x = 350 + ((i * 97 + t * (6 + s.wind * 2)) % 1080), y = 474 + ((i * 43 + t * 8) % 241);
            const size = s.blossom > .3 ? 1.8 : 3.2;
            this.ctx.save(); this.ctx.translate(x + Math.sin(t + i) * 12, y); this.ctx.rotate(t * .6 + i);
            this.ellipse(0, 0, size, size * .45, this.color(s.blossom > .3 ? [234, 194, 185] : [182, 122, 56], [91, 85, 47])); this.ctx.restore();
        }
        if (this.cover > .4) {
            this.ellipse(1237, 640, 10, 10, this.color([231, 234, 218], [136, 162, 165]));
            this.ellipse(1237, 626, 7, 7, this.color([242, 240, 218], [157, 179, 178]));
            this.rect(1230, 619, 15, 2, '#58685c'); this.rect(1233, 614, 9, 6, '#58685c');
            this.line(1240, 626, 1247, 627, this.color([199, 137, 67]), 2);
            this.line(1228, 634, 1217, 629, this.color([104, 108, 78]), 1.5);
            this.rect(1230, 631, 14, 3, this.color([170, 95, 67], [112, 111, 81]));
        }
        if (s.temperature !== null && s.temperature < 1 && s.elevation < 8 && this.cover < .2 && s.rainRate === 0) for (let i = 0; i < 40; i++) {
            const x = 40 + i * 35, y = 669 + Math.sin(i * 8) * 23;
            this.line(x, y, x + 2, y - 3, this.colorAlpha([227, 231, 210], [138, 161, 150], .45), .7);
        }
    }

    specials() {
        const s = this.state, t = this.elapsed;
        // Rare events use elapsed visible time, so switching tabs neither
        // skips a sequence nor triggers a burst of events on return.
        const hat = (t + 40) % 193;
        if (hat < 12 && s.wind > 4 && s.activity > .15) {
            const { x, y } = curvePoint(STREET, .73 + hat / 12 * .16);
            this.person(x, y, .8, 2);
            this.ctx.save(); this.ctx.translate(x + 18, y - 21 + Math.sin(hat * 2) * 7); this.ctx.rotate(hat * 3);
            this.rect(-5, 0, 10, 1.5, '#ad9767'); this.rect(-3, -3, 6, 4, '#baa574'); this.ctx.restore();
        }
        const ufo = (t + (this.options.seed ?? 73) * 7) % 1801;
        if (ufo < 9 && s.stars > .7 && this.options.easterEggs !== false) {
            const x = 650 + ufo * 32, y = 108 + Math.sin(ufo) * 7;
            this.ellipse(x, y, 5, 1.5, '#b6cdc344');
            if (ufo < 5 || ufo > 6) this.ellipse(x + 2, y + 1, .8, .8, '#b8e6b9aa');
        }
    }
}
