# Architecture: Tärningskast – en statisk HTML-sida med 3D-tärningar

## Deviations from the specification
None in the product. Two deviations from the factory defaults, both forced by the specification:
- The product is a single static `index.html`, not a FastAPI web app. The `web-app` blueprint and the
  `webapp-scaffold`, `data-model` and `deploy-compose` recipes do not apply; there is no server, database
  or container. The software gates still run: a small Python test harness (`pyproject.toml`,
  `factory.yaml`, the `sitecheck` package, Playwright tests) exists only for verification and is not
  delivered.
- SW-004 uses the `user-docs` recipe but writes the one `README.md` that R-010 asks for instead of
  `docs/USER_GUIDE.md` and `docs/ADMIN_GUIDE.md`; its `core.files` gate is pointed at `README.md`.

## Overview
One self-contained HTML file holds the markup, one `<style>` and one inline `<script>`. The script has
three parts that are built in sequence: the page shell (radio group, button, result live region), a
Canvas 2D renderer that draws six convex polyhedra with flat shading and face labels, and a throw
controller that draws a fair value with `crypto.getRandomValues` and animates a multi-axis rotation that
ends exactly in the orientation that turns the result face to the viewer. Verification runs in headless
Chromium over `file://`, plus Firefox in an integration run.

```
index.html
 ├─ DOM: #die(canvas, data-sides/value/state) · #result(aria-live) · fieldset "Tärning" · button "Kasta"
 ├─ Renderer (SW-002): geometry → faces → landing(sides,value) → shaded Canvas 2D drawing
 └─ Controller (SW-003): randomInt(n) → Renderer.roll(…, 1000 ms, onLand) → result text + data-value
verification only (not delivered):
 pyproject.toml · factory.yaml (http.server for axe) · sitecheck/ · tests/unit · tests/e2e · integration/e2e
```

## Decisions
| # | Decision | Reason | Alternatives rejected (and why) |
|---|---|---|---|
| D-1 | Canvas 2D with own orthographic projection, flat Lambert shading and back-face culling | One code path for all six solids; shading per frame is trivial; convex solids need no depth sort; pixels are testable | CSS 3D transforms: non-square faces need `clip-path` per face and shading cannot follow rotation without per-frame JS anyway; WebGL: forbidden as a library route and needless for ≤ 20 polygons |
| D-2 | Geometry from vertex lists + convex hull, numbering by a fixed sort rule, value = index + 1 | Deterministic, short code (R-012), and lets tests assert `frontFaceValue()` for every value | Hand-written face tables per solid: error-prone; opposite-faces-sum rule: not required by the spec, adds risk |
| D-3 | Landing pose = face normal to +z and up-vector to +y, then a fixed tilt of < 16° | The result face is the most viewer-facing face (adjacent normals differ by ≥ 41.8°) and the die still shows depth | Exactly face-on: a cube would look flat, against R-006 "djupet syns" |
| D-4 | `ROLL_MS = 1000` with a cubic ease-out and a slerp combined with decaying x/y spins; rAF plus a safety timeout | Centre of the 600–1500 ms window gives margin for slow machines; spins on two axes meet "flera axlar" | Physics simulation: out of scope; CSS keyframes: cannot end on an arbitrary computed orientation easily |
| D-5 | Reduced-motion path updates the DOM synchronously in the click handler | R-008's 100 ms bound with margin, and lets the fairness test click 20 000 times in one `page.evaluate` | Short animation: still violates "hoppar över rotationen" |
| D-6 | Small debug object `window.tarningDebug` in the product | Makes the landing orientation (the riskiest part) tool-checkable; harmless to users | Pixel-OCR of the front face: fragile |
| D-7 | Python harness: `sitecheck` package (static rules) + pytest-Playwright | The factory gates are Python-based and require a package with ≥ 70 % coverage; the static rules (R-001, R-010, R-012) are real checks worth unit-testing | Node/Playwright-test: gates only partly support Node (no a11y runner) |
| D-8 | `factory.yaml` starts `python -m http.server` only so the e2e gate's axe pass has a URL; product tests use `file://` | R-002 is about `file://`; axe runner needs HTTP | Running axe over `file://` ourselves: duplicates the gate |
| D-9 | Fixed light colours, no dark scheme | Spec: dark text on light background; axe checks both schemes and fixed colours pass both | Dark mode: not requested |
| D-10 | Firefox proof in a separate integration card (INT-001), Chromium in every SW card | Only Chromium is preinstalled; containing the Firefox risk in a leaf card keeps the rest of the build green | Firefox in `tests/e2e`: would fail every later e2e gate run if Firefox is unavailable |

## Subsystems
### Page shell and harness — SW-001
DOM contract, CSS and layout, radio handling, `sitecheck`, pytest/Playwright fixtures, `factory.yaml`.
### 3D renderer — SW-002
Geometry, numbering, landing orientation, shading, labels and pips, `Renderer`, `tarningDebug`.
### Throw — SW-003
`randomInt`, controller state machine, roll animation, reduced motion, focus return.
### Documentation — SW-004
Swedish `README.md` (independent branch after SW-001).
### Journeys and cross-browser proof — SW-005, INT-001
Journey tests in Chromium; the Chromium + Firefox matrix over `file://` with a report.

## Requirement coverage
| Requirement | Cards | Proven by |
|---|---|---|
| R-001 (must) single self-contained file | SW-001, SW-002, SW-003, SW-005, INT-001 | `python -m sitecheck html index.html` in verify of SW-003/SW-005 (forbidden substrings and APIs); request recording in every e2e test (`software.e2e`); INT-001 in Firefox |
| R-002 (must) works from file:// | SW-005, INT-001 | `tests/e2e/test_journey_all_types.py` (Chromium, verify of SW-005); `bash integration/e2e/run.sh` (Chromium + Firefox, verify of INT-001) |
| R-003 (must) one button "Kasta", disabled while rolling | SW-001, SW-003 | `test_page_shell.py` (one button); `test_throw.py` timing (disabled at once, enabled ≤ 1600 ms) |
| R-004 (must) die type radio group | SW-001, SW-005 | `test_page_shell.py` (six radios, T6 checked, data-sides) |
| R-005 (must) fair 1–N | SW-003 | `test_fairness.py` (6 000 T6 / 20 000 T20 counts in 850–1150; all values for the others); `sitecheck` requires `crypto.getRandomValues`; review of rejection sampling |
| R-006 (must) 3D die with animation | SW-002, SW-003 | `test_render.py` (face counts/sizes, `frontFaceValue` for every value, shading); `test_throw.py` (snapshots at 150/300 ms differ, update in 600–1500 ms, data-value = result = front face); screenshots reviewed |
| R-007 (must) big result, fits on mobile | SW-001, SW-005 | `test_page_shell.py` and `test_journey_all_types.py` (font-size ≥ 96/72 px, bounding boxes in 375×667) |
| R-008 (must) reduced motion | SW-003, INT-001 | `test_throw.py`/`test_fairness.py` with `reducedMotion: 'reduce'` (update ≤ 100 ms, never disabled) |
| R-009 (must) Swedish UI | SW-001 | `test_page_shell.py` (lang, title, "Tryck på Kasta"); `sitecheck` lang/title rules |
| R-010 (must) Swedish README | SW-004 | `python -m sitecheck readme README.md` (verify); `core.files` gate |
| R-011 (should) accessibility | SW-001, SW-003, SW-005 | `test_page_shell.py` (aria-live, aria-hidden, arrow keys, focus outline); `test_throw.py` (Enter/Space); axe in `software.e2e` |
| R-012 (should) < 60 kB | SW-002, SW-003 | `sitecheck` size rule in verify of SW-003 and SW-005 |
| R-013 (should) smooth animation | SW-003 | `test_throw.py` mean rAF interval < 20 ms; `sitecheck` requires `requestAnimationFrame` |

## Budgets
File size: target ≤ 25 kB after SW-002 and < 61 440 bytes hard limit. Timing: ROLL_MS 1000 ms in a
600–1500 ms window, re-enable ≤ 1150 ms worst case (safety timer) against a 1600 ms limit.

## Plan size
Software 5 cards (SW-001…SW-005), integration 1 (INT-001): 6 of 12 for size S. Longest chain:
SW-001 → SW-002 → SW-003 → SW-005 (INT-001 parallel to SW-005, SW-004 parallel to SW-002…SW-005). The
chain is sequential because all three product cards edit the one file `index.html`, which the
specification requires.

## What is not done
- Safari (macOS/iOS) and Edge are not run by any tool; Edge shares Chromium's engine. Operator check.
- Smoothness on a real phone and readability at a distance are not measured.
- That the label on the front face is upright and legible is reviewed on screenshots, not tool-verified.
- No history, sounds, multiple dice, storage or network, as the specification excludes them.
