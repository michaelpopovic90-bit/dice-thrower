# Risk register: Tärningskast – en statisk HTML-sida med 3D-tärningar

Likelihood and impact: low / med / high.

| ID | Risk | Likelihood | Impact | Mitigation in the plan | Residual / how it will be validated |
|---|---|---|---|---|---|
| K-01 | The die lands with a wrong face towards the viewer (geometry, numbering or orientation maths wrong), so the picture contradicts the big number | med | high | INTERFACES 4.3 fixes vertices, numbering, up-vectors and the landing rotation; `tarningDebug.frontFaceValue()` is asserted for every value of every die in SW-002 and after real throws in SW-003; both cards are reviewed | Readability of the label on the front face (upright, not mirrored) is checked only on the six `render-T<N>.png` screenshots by review |
| K-02 | Shapes look wrong (e.g. T10 kites not planar, T12 drawn as something else) although the counts pass | low | med | Exact coordinates incl. a = 0.105573 for the trapezohedron; `faceSizes()` asserted per solid; screenshots per type | Visual review of the screenshots (reviewed, not tool-verified) |
| K-03 | Firefox cannot be obtained in the build environment (only Chromium is preinstalled), so R-002's Firefox half is unproven | med | med | INT-001 installs Playwright's Firefox into scratch; on failure it exits 3 with "FIREFOX NOT VERIFIED", it never passes silently; INT-001 is a leaf card, so its failure blocks nothing else | If it fails, the delivery report lists Firefox as not verified; Safari (and mobile browsers) are always operator validation |
| K-04 | Timing assertions (disabled ≤ 1600 ms, update 600–1500 ms, frame interval < 20 ms) are flaky on a loaded CI machine | med | med | Fixed ROLL_MS = 1000 leaves ≥ 400 ms margin both sides; SAFETY_MS fallback; measurements in-page with `performance.now()`; no Python sleeps | A flaky run shows up as an intermittent gate failure; the red team re-runs the suite |
| K-05 | Fairness test (26 000+ throws through the button) is too slow or flaky | low | med | Reduced-motion path is synchronous and drawing may coalesce to the next frame (INTERFACES 4.7, 4.5); bounds 850–1150 are > 4.7σ for 1000 expected, false-failure chance per run < 1e-4 | Statistical, not a proof: rejection sampling is also reviewed in SW-003 |
| K-06 | Layout overflows at 375×667 (two-line "Tryck på Kasta" at 72 px + die + six options + button) | med | med | Locked sizes in INTERFACES 3 (canvas min(55vmin, 34vh, 360px), one-row options, line-height 1.05); bounding boxes asserted in SW-001 and SW-005 at both sizes | Other phone sizes (e.g. 320 px wide, landscape) are not tested; operator check on a real phone |
| K-07 | An accidental external reference or storage use (a URL in a comment, SVG xmlns, a font) breaks R-001 / non-goals | low | high | `sitecheck` forbids the substrings and APIs (INTERFACES 2); every e2e test asserts zero http/https/ws requests | None known |
| K-08 | `index.html` grows over 60 kB with geometry tables and labels | low | low | Geometry computed from a few vertices; size checked by `sitecheck` in SW-003 and SW-005 | — |
| K-09 | The verification harness (pyproject, sitecheck, tests) is mistaken for part of the product, or `index.html` depends on it | low | med | INTERFACES 1 states only `index.html` and `README.md` are delivered; the page is tested from `file://` with no server | Delivery packages the two files only |
| K-10 | Smoothness on a real mid-range phone (R-013) and correct appearance in Safari cannot be measured here | high | low | Canvas 2D with ≤ 20 polygons per frame is cheap; frame interval measured in desktop Chromium | Needs physical validation on the operator's phone |

## Needs physical validation
- Open `index.html` from the file system in Safari (macOS and iOS) and in Edge, throw each die once, and
  check the result face is readable and matches the big number (README describes how to open the file).
- Check on a real mobile phone that the animation runs smoothly and the layout fits without scrolling.
- Read the result from a few metres away (goal "läsbart även på avstånd").
