export const clamp = (n, min = 0, max = 1) => Math.max(min, Math.min(max, n));
export const mix = (a, b, t) => a + (b - a) * t;
const number = (value, fallback = null) => typeof value === 'number' && Number.isFinite(value) ? value : fallback;
export const smooth = (a, b, n) => { const t = clamp((n - a) / (b - a)); return t * t * (3 - 2 * t); };
export const CELESTIAL_RADIUS = 49;
const celestialHeight = elevation => 307 - 210 * Math.atan(elevation / 12) / Math.atan(65 / 12);

/** Exaggerated horizon geometry lets the hills cover the sun as it sets. */
export function sunAppearance(elevation) {
    const normal = smooth(-5.5, 19, elevation);
    const warm = 1 - smooth(0, 13, elevation);
    return {
        x: 1140,
        y: celestialHeight(elevation),
        radius: CELESTIAL_RADIUS * mix(1.3, 1, normal),
        color: [255, Math.round(mix(239, 153, warm)), Math.round(mix(188, 91, warm))],
        warmth: warm,
    };
}

/** Separate visual path; daylight reduces contrast without revealing stars behind the moon. */
export function moonAppearance(elevation, sunElevation, cloud = 0) {
    return {
        x: 900,
        y: celestialHeight(elevation),
        radius: CELESTIAL_RADIUS,
        contrast: mix(1, .065, smooth(-8, 12, sunElevation)) * (1 - smooth(.45, .96, cloud)),
        earthshine: 1 - smooth(-8, 5, sunElevation),
    };
}

/** Rain comes only from an observation no more than five minutes old. */
export function observedRain(observation = {}, now) {
    const at = number(observation.at);
    const rate = number(observation.rainRate);
    return at !== null && rate !== null && at > 0 && now >= at && now - at <= 300 && rate >= 0 ? rate : null;
}

/** Sichtbare Niederschlagsstärke; Regen bleibt an die aktuelle Messung gebunden. */
export function precipitationAppearance(rainRate, snow = 0, sleet = false) {
    const rate = Math.max(0, number(rainRate, 0));
    const intensity = clamp(rate / 40) ** .8;
    const snowCount = snow >= .01 ? Math.ceil(clamp(snow) * 320) : 0;
    const rainCount = rate > 0 && (!snowCount || sleet)
        ? Math.min(520 - snowCount, Math.ceil((8 + 440 * intensity) * (snowCount ? .4 : 1))) : 0;
    return { snowCount, rainCount, intensity, length: mix(9, 34, intensity),
        speed: mix(390, 770, intensity), width: mix(.55, 1.25, intensity), alpha: mix(.24, .64, intensity) };
}

/** Ein langsamer Lichtimpuls je Entladung; der seltene Baumtreffer klingt vollständig ab. */
export function stormAppearance(seconds, seed = 73, easterEggs = true) {
    const cycle = Math.floor(Math.max(0, seconds) / 15);
    const random = seededRandom(seed + cycle * 157);
    const phase = Math.max(0, seconds) % 15 - (4 + random() * 3);
    const tree = easterEggs && cycle % 13 === 2;
    const kind = tree ? 'tree' : cycle % 3 === 0 ? 'cloud' : 'bolt';
    const flash = phase >= 0 && phase < 1.1 ? Math.sin(phase / 1.1 * Math.PI) ** 2 : 0;
    return { cycle, phase, kind, flash, x: 640 + random() * 650,
        fire: tree ? smooth(.12, .65, phase) * (1 - smooth(4.8, 6.8, phase)) : 0,
        smoke: tree ? smooth(2, 4, phase) * (1 - smooth(6.8, 7.8, phase)) : 0 };
}

/** Reiner Bildzustand. Alle Zeitstempel sind Unix-Sekunden, Wind ist m/s. */
export function resolveState(input = {}, now = input.time ?? Date.now() / 1000) {
    const f = input.forecast ?? {}, o = input.observation ?? {};
    const sun = input.sun ?? {}, moon = input.moon ?? {};
    const month = clamp(number(input.month, 9), 1, 12.999);
    const hour = ((number(input.hour, 12) + (now - number(input.time, now)) / 3600) % 24 + 24) % 24;
    const elevation = clamp(number(sun.elevation, 25), -90, 90);
    const morning = number(sun.azimuth, 180) < 180;
    const daylight = smooth(-9, 12, elevation);
    const night = 1 - smooth(-16, -3, elevation);
    const twilight = smooth(-14, -2, elevation) * (1 - smooth(2, 16, elevation));
    const goldenLight = smooth(-5, 1, elevation) * (1 - smooth(2, 14, elevation));
    const phase = elevation < -12 ? 'night' : elevation < -1 ? (morning ? 'dawn' : 'dusk')
        : elevation < 8 ? (morning ? 'sunrise' : 'sunset') : hour < 11 ? 'morning' : hour < 15 ? 'midday' : 'afternoon';
    const season = month < 3 || month >= 12 ? 'winter' : month < 6 ? 'spring' : month < 9 ? 'summer' : 'autumn';
    const leaf = smooth(3.1, 5.3, month) * (1 - smooth(10.0, 12, month));
    const autumn = smooth(8.8, 11, month) * (1 - smooth(11.4, 12.9, month));
    const blossom = smooth(3.3, 4.2, month) * (1 - smooth(4.6, 5.6, month));
    const rainRate = observedRain(o, now);
    const snow = f.snow === true;
    const temperature = number(f.temperature, number(o.temperature));
    const freshLightning = number(o.lightningAt, 0) > 0 && now >= o.lightningAt && now - o.lightningAt <= 1800;
    const storm = f.storm === true || freshLightning;
    const wind = clamp(number(f.wind, 1), 0, 40);
    const cloud = clamp(Math.max(number(f.cloud, .35), storm ? .88 : snow ? .6 : 0));
    const fog = clamp(number(f.fog, 0));
    const moonPhase = ((number(moon.phase, .5) % 1) + 1) % 1;
    const moonLight = smooth(-4, 6, number(moon.elevation, -90)) * number(moon.illumination, (1 - Math.cos(moonPhase * Math.PI * 2)) / 2);
    const snowCover = clamp(number(o.snowDepth, 0) / 3);
    return {
        now, hour, month, elevation, morning, phase, season, daylight, night, twilight, goldenLight, leaf, autumn, blossom,
        rainRate, rain: !snow && rainRate !== null ? clamp(rainRate / 8) : 0,
        snow: snow ? (temperature !== null && temperature > 2 ? .45 : 1) : 0,
        sleet: snow && temperature !== null && temperature > 2 && rainRate > 0, snowCover,
        storm, storminess: storm ? 1 : 0, cloud, fog, wind, windDirection: number(f.windDirection, 240), temperature,
        moonPhase, moonLight: clamp(moonLight), moonElevation: number(moon.elevation, -90),
        moonRotation: number(moon.rotation, 0), moonAzimuth: number(moon.azimuth, 150),
        sunAzimuth: number(sun.azimuth, 180),
        stars: night * (1 - smooth(.25, .95, cloud)) * (1 - fog),
        milkyWay: night * (1 - cloud) ** 3 * (1 - clamp(moonLight) * .94) * (1 - fog),
        activity: daylight * (1 - fog * .6) * (storm ? .12 : 1) * (1 - clamp(wind / 24)) * (rainRate > 0 ? .35 : 1),
        fireflies: month >= 6 && month < 8.7 && night > .5 && !storm && !snow && !(rainRate > 0) && wind < 4,
    };
}

/** Daily routines vary by window without being randomized at every observation. */
export function windowLight(index, hour, darkness, seconds) {
    const seed = fract(Math.sin(index * 127.1 + 13) * 43758.5453);
    const morning = smooth(4.8 + seed * 2, 5.0 + seed * 2, hour) * (1 - smooth(8.0 + seed, 8.3 + seed, hour));
    const evening = smooth(16 + seed * 3, 16.2 + seed * 3, hour) * (1 - smooth(21.4 + seed * 2.5, 21.7 + seed * 2.5, hour));
    const late = seed > .91 ? .55 : 0;
    const cycle = (seconds + seed * 197) % (61 + seed * 97);
    const room = 1 - smooth(12, 15, cycle) * (1 - smooth(22, 25, cycle));
    const passing = .75 + .25 * smooth(-.45, .45, Math.sin(seconds / (23 + seed * 38) + index * 4));
    return clamp(Math.max(morning, evening, late) * darkness * passing * room);
}

export const fract = n => n - Math.floor(n);
export function seededRandom(seed = 17) {
    let value = seed >>> 0;
    return () => { value = (Math.imul(1664525, value) + 1013904223) >>> 0; return value / 4294967296; };
}
