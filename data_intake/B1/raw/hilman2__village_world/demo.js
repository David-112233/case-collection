import { Dorfwelt } from './dorfwelt.js';

const $ = id => document.getElementById(id);
const fields = ['season', 'weather', 'time', 'moon', 'wind', 'rain', 'snow'];
const world = new Dorfwelt($('scene'), { state: {}, seed: 73 });
const presets = {
    'autumn-evening': ['10.2', 'fair', 18.75, .35, 2, 0, 0],
    'summer-night': ['7.1', 'clear', 0.5, .87, .6, 0, 0],
    'autumn-fog': ['10.2', 'fog', 7.3, .7, .5, 0, 0],
    'winter-snow': ['1.5', 'snow', 16.5, .48, 2, 0, 5],
    'spring-morning': ['4.3', 'fair', 8.5, .15, 2.5, 0, 0],
    'summer-storm': ['7.1', 'storm', 20.5, .65, 8, 9, 0],
};
const formatHour = h => { const minutes = Math.round(h * 60) % 1440; return `${String(Math.floor(minutes / 60)).padStart(2, '0')}:${String(minutes % 60).padStart(2, '0')}`; };

function update() {
    const month = +$('season').value, hour = +$('time').value, weather = $('weather').value;
    const now = Date.now() / 1000;
    const winter = month < 3 || month >= 12;
    const phase = +$('moon').value, illumination = (1 - Math.cos(phase * Math.PI * 2)) / 2;
    const moonTransit = (12 + phase * 24) % 24;
    const moonElevation = Math.cos((hour - moonTransit) / 24 * Math.PI * 2) * (winter ? 60 : 50) - 5;
    // The demo approximates the annual solar path with a daily curve.
    // Dashboard integrations supply the calculated solar position instead.
    const elevation = Math.sin((hour - 6) / 24 * Math.PI * 2) * (winter ? 38 : 58) - (winter ? 13 : 0);
    const cloud = { clear: .02, fair: .23, cloudy: .57, overcast: 1, fog: .4, 'rain-forecast': .82, rain: .84, storm: .95, snow: .8, sleet: .95 }[weather];
    world.setState({
        time: now, month, hour,
        sun: { elevation, azimuth: hour < 12 ? 120 : 240 },
        moon: { phase, illumination, elevation: moonElevation, azimuth: 180, rotation: -14 },
        forecast: { cloud, wind: +$('wind').value, windDirection: 250, fog: weather === 'fog' ? .9 : 0,
            snow: ['snow', 'sleet'].includes(weather), storm: weather === 'storm',
            temperature: weather === 'sleet' ? 3 : weather === 'snow' ? -2 : winter ? 2 : month > 8 ? 12 : 21 },
        observation: { at: now, rainRate: +$('rain').value, snowDepth: +$('snow').value },
    });
    $('time-label').value = formatHour(hour); $('clock').textContent = formatHour(hour);
    $('moon-label').value = `${Math.round(illumination * 100)} %`;
    $('wind-label').value = `${$('wind').value} m/s`;
    $('rain-label').value = `${$('rain').value} mm/h`;
    $('snow-label').value = `${$('snow').value} cm`;
}
function preset(name) {
    const values = presets[name];
    if (!values) return;
    fields.forEach((field, i) => $(field).value = String(values[i]));
    const button = document.querySelector(`[data-preset="${name}"]`);
    $('caption').textContent = button.textContent;
    document.querySelectorAll('[data-preset]').forEach(el => el.setAttribute('aria-pressed', String(el === button)));
    update();
}
document.querySelectorAll('[data-preset]').forEach(button => button.addEventListener('click', () => preset(button.dataset.preset)));
$('controls').addEventListener('input', event => {
    if (event.target.id === 'weather') $('rain').value = ['rain', 'storm'].includes($('weather').value) ? 5 : 0;
    if (event.target.id === 'tour') return;
    document.querySelectorAll('[data-preset]').forEach(el => el.setAttribute('aria-pressed', 'false'));
    $('caption').textContent = `${$('season').selectedOptions[0].textContent} · ${$('weather').selectedOptions[0].textContent}`;
    update();
});
setInterval(() => {
    if (!$('tour').checked || document.hidden || world.paused || world.motion.matches) return;
    $('time').value = String((+$('time').value + .05) % 24);
    update();
}, 180);
preset(new URL(location.href).searchParams.get('scene') ?? 'autumn-evening');

// Expose the demo instance for browser checks.
window.dorfweltPreview = world;
