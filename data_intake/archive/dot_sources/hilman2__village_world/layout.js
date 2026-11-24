export const GROUND_OFFSET = 28;
export const STREET = [[0, 574], [300, 562], [580, 606], [920, 578]];
export const LOWER_ROAD = [[644, 740], [756, 699], [915, 697], [985, 646]];
export const EAST_ROAD = [[1120, 646], [1157, 644], [1173, 608], [1156, 580]];
export const BRIDGE = { left: 979, right: 1122, back: 638, front: 652, base: 674, archLeft: 1016, archRight: 1084 };

/** Point on the drawn path, offset along its unit normal in scene pixels. */
export function curvePoint(points, t, offset = 0) {
    const [a, b, c, d] = points, u = 1 - t;
    const x = u ** 3 * a[0] + 3 * u * u * t * b[0] + 3 * u * t * t * c[0] + t ** 3 * d[0];
    const y = u ** 3 * a[1] + 3 * u * u * t * b[1] + 3 * u * t * t * c[1] + t ** 3 * d[1];
    const dx = 3 * u * u * (b[0] - a[0]) + 6 * u * t * (c[0] - b[0]) + 3 * t * t * (d[0] - c[0]);
    const dy = 3 * u * u * (b[1] - a[1]) + 6 * u * t * (c[1] - b[1]) + 3 * t * t * (d[1] - c[1]);
    const length = Math.hypot(dx, dy);
    return { x: x - dy / length * offset, y: y + dx / length * offset };
}

export const curvePath = points => `M${points[0].join(' ')}C${points.slice(1).map(p => p.join(' ')).join(' ')}`;

export function streetAtX(x) {
    let lo = 0, hi = 1;
    for (let i = 0; i < 18; i++) {
        const t = (lo + hi) / 2;
        if (curvePoint(STREET, t).x < x) lo = t; else hi = t;
    }
    return curvePoint(STREET, (lo + hi) / 2);
}

const riverCurves = [
    [[968, 436], [981, 513], [956, 563], [1005, 589]],
    [[1005, 589], [1054, 615], [1049, 638], [1049, 667]],
    [[1049, 667], [1049, 696], [1119, 710], [1124, 746]],
];
const riverWidths = [0, 24, 64, 88];

/** Banks, flowing water and ducks share the same stream centerline. */
export function riverPoint(progress, across = 0) {
    const section = Math.min(2, Math.floor(progress * 3)), t = progress * 3 - section;
    const width = riverWidths[section] * (1 - t) + riverWidths[section + 1] * t;
    return curvePoint(riverCurves[section], t, across * width / 2);
}

const bank = side => Array.from({ length: 97 }, (_, i) => riverPoint(i / 96, side));
const banks = [...bank(1), ...bank(-1).reverse()];
export const STREAM = banks.map((p, i) => `${i ? 'L' : 'M'}${p.x.toFixed(2)} ${p.y.toFixed(2)}`).join('') + 'Z';

export const houses = [
    [210, 534, .72, 0], [326, 535, .92, 1], [458, 548, .65, 2],
    [792, 536, .72, 2], [887, 560, 1.03, 0], [1026, 534, .79, 1],
    [1144, 577, 1.13, 3], [1249, 542, .63, 0], [606, 561, .68, 3],
];
export const STORM_TREE = [1080, 523, .65];
export const trees = [
    [74, 523, 1.15], [145, 520, .72, true], [395, 519, .68], [527, 518, .72],
    [662, 526, .62, true], STORM_TREE, [1330, 558, 1, true], [1403, 615, 1.55],
];
export const fences = [[250, 314, 556], [346, 419, 556], [553, 599, 569], [628, 655, 569], [1191, 1218, 604], [1248, 1300, 604]];
export const lamps = [
    ...[.17, .44, .72, .97].map(t => ({ ...curvePoint(STREET, t, 10), scale: .76 })),
    { ...curvePoint(LOWER_ROAD, .88, 22), scale: .9 },
    { ...curvePoint(EAST_ROAD, .47, 19), scale: .9 },
];
