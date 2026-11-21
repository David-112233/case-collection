# SVG interactive Diagram

- Author: Kent Chang, CodePen handle kentchangdesign.
- Public original: https://codepen.io/kentchangdesign/pen/VrgoWY
- Public Pen code is MIT per https://blog.codepen.io/docs/pens/licensing/.
- Author HTML/SVG, Sass and TypeScript captured from the original editor; compiled CSS and JS captured using CodePen's View Compiled options.
- External JS requested by the running original: jQuery 3.2.1 and Snap.svg 0.5.1, exact ordered URLs in rendered-dependencies.json. No CDN code redistributed. Do not include CodePen editor runtime assets/URLs in portable copy. Original code expects Snap global and uses jQuery $.
- Cloud preview verified: in compact view chart viewport has 400px height, top/bottom fades and subsequent chart nodes are clipped. Click left circular control at diagram header (#svg-expand); after transitions the chart area expands to 1100px with fades removed. For a 2-frame comparison use a viewport tall enough for the chart, or capture full page. Expanded preview confirms additional stages, branch arrows, segment nodes and panel relationship; this is viewport masking/reveal, not physical 3D geometry.
