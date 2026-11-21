import { readFile, writeFile } from 'node:fs/promises';

// The checked-in bundle also lets the demo run directly from a local file.
const sources = await Promise.all(['state.js', 'layout.js', 'dorfwelt.js', 'demo.js'].map(async file => {
    const source = await readFile(new URL(file, import.meta.url), 'utf8');
    return source.replace(/^import .*;\r?\n/gm, '').replace(/^export /gm, '');
}));
await writeFile(new URL('demo.bundle.js', import.meta.url), `(function () {\n'use strict';\n${sources.join('\n')}\n})();\n`);
await writeFile(new URL('index.html', import.meta.url), await readFile(new URL('demo.html', import.meta.url)));
