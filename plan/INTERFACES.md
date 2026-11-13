# Interfaces: Tärningskast – en statisk HTML-sida med 3D-tärningar

Locked contracts. Builders implement these exactly. One source of truth per fact. The product has no
server, no database, no HTTP routes, no jobs and no configuration variables; those template sections are
replaced by the DOM contract, the in-page JavaScript contract and the test-harness contract below.

## 1. Repository layout

| Path | Content | Written by |
|---|---|---|
| `index.html` | THE product: one file with all HTML, CSS (one `<style>`) and JavaScript (one inline `<script>`, no `src`) | SW-001 (shell), then SW-002 (3D renderer), then SW-003 (throw) — strictly in that order |
| `README.md` | Operator README in Swedish (deliverable) | SW-004 |
| `pyproject.toml` | Test harness only: Python project `tarning-tests`, no runtime dependencies, `dev` extra | SW-001 |
| `factory.yaml` | Gate contract (section 6) | SW-001; SW-005 may edit `a11y_pages` only |
| `sitecheck/` | Python package: static checks of `index.html` and `README.md` (section 5) | SW-001 |
| `tests/conftest.py` | Shared pytest config (section 6) | SW-001 |
| `tests/unit/test_sitecheck*.py` | Unit tests of `sitecheck` | SW-001 |
| `tests/e2e/conftest.py` | Playwright fixtures (section 6) | SW-001 |
| `tests/e2e/test_page_shell.py` | Shell tests | SW-001 |
| `tests/e2e/test_render.py` | Renderer tests | SW-002 |
| `tests/e2e/test_throw.py`, `tests/e2e/test_fairness.py` | Throw, timing, randomness tests | SW-003 |
| `tests/e2e/test_journey_*.py` | Journey tests | SW-005 |
| `integration/e2e/**` | Cross-browser (Chromium + Firefox) run over `file://` | INT-001 |

`pyproject.toml`, `factory.yaml`, `sitecheck/` and `tests/` are build-time verification only; Delivery
ships `index.html` and `README.md`. `index.html` must never depend on any of them.

## 2. DOM contract of `index.html`

Exactly this structure (classes and extra wrapper `<div>`s for layout are free; ids, roles, attributes and
texts below are fixed). Visual order top to bottom: die, result, die-type choice, button.

```html
<!DOCTYPE html>
<html lang="sv">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Tärning</title>
  <style>…</style>
</head>
<body>
  <main>
    <h1 class="sr-only">Tärning</h1>
    <div id="die" data-sides="6" data-value="" data-state="idle" aria-hidden="true">
      <canvas id="die-canvas"></canvas>
    </div>
    <div id="result" aria-live="polite" aria-atomic="true">
      <span id="result-die" class="sr-only"></span><span id="result-value">Tryck på Kasta</span>
    </div>
    <fieldset id="die-type">
      <legend>Tärning</legend>
      <input type="radio" name="sides" id="sides-4"  value="4"><label for="sides-4">T4</label>
      <input type="radio" name="sides" id="sides-6"  value="6" checked><label for="sides-6">T6</label>
      <input type="radio" name="sides" id="sides-8"  value="8"><label for="sides-8">T8</label>
      <input type="radio" name="sides" id="sides-10" value="10"><label for="sides-10">T10</label>
      <input type="radio" name="sides" id="sides-12" value="12"><label for="sides-12">T12</label>
      <input type="radio" name="sides" id="sides-20" value="20"><label for="sides-20">T20</label>
    </fieldset>
    <button id="roll" type="button">Kasta</button>
  </main>
  <script>…</script>
</body>
</html>
```

| Element | Attribute / text | Values and when they change |
|---|---|---|
| `#die` | `data-sides` | `"4"`…`"20"`; set synchronously in the radio `change` handler, before the handler returns |
| `#die` | `data-value` | `""` before the first throw; the new result (decimal string) set at the same moment as `#result-value` at landing; during a roll it keeps the previous value |
| `#die` | `data-state` | `idle` (page load, after a type change), `rolling` (animation running), `landed` (after a throw finished) |
| `#die` | `aria-hidden` | always `"true"` |
| `#result-value` | text | `Tryck på Kasta` until the first landing; then the result as digits, e.g. `17`. During a roll the previous text stays and the element has class `is-stale` (dimmed by colour, see 3); the class is removed at landing |
| `#result-die` | text | `""` until the first landing; then `T<N>: ` (e.g. `T20: `) so the live region reads "T20: 17". Visually hidden (`.sr-only`) |
| `#result` | `aria-live="polite"`, `aria-atomic="true"` | fixed. At landing both spans' `textContent` are reassigned (even if the value repeats) |
| `#roll` | `disabled` | set synchronously in the click handler when animating; removed at landing. With reduced motion it is never set |
| `#die-type` | `disabled` | set together with `#roll.disabled`, removed together with it |
| `.sr-only` | CSS | the standard visually-hidden pattern (`position:absolute; width:1px; height:1px; overflow:hidden; clip:rect(0 0 0 0); white-space:nowrap`) |

There is exactly one `<button>` in the document. No other visible text exists besides the legend, the six
labels, the button text and the result.

Forbidden anywhere in `index.html` (checked by `sitecheck`, section 5): the substrings `http:` and
`https:` (so no inline SVG with `xmlns`, no comments with URLs), any `src=`, `href=`, `srcset=`,
`action=` or `poster=` attribute whose value starts with `//`, `http`, or names another file, `@import`,
CSS `url(` other than `url(data:`, `<link`, `<script src`, `fetch(`, `XMLHttpRequest`, `WebSocket`,
`localStorage`, `sessionStorage`, `indexedDB`, `document.cookie`.

## 3. Visual and layout contract

| Item | Value |
|---|---|
| Colours (fixed, no `prefers-color-scheme` switching, no `color-scheme: dark`) | page background `#f6f4ef`; text `#1d1d1f`; stale result text `#5c5c5c` (≥ 6:1 on the background); die face base `#f3efe4`; die labels/pips `#1b1b1b`; edges `rgba(0,0,0,0.35)`; focus ring `#1a4fd6` |
| Font | `system-ui, -apple-system, "Segoe UI", Roboto, sans-serif` (local system fonts only) |
| `#result` font-size | `clamp(72px, calc(12vmin + 24px), 160px)`, `line-height: 1.05`, `text-align: center`, `font-weight: 700`, wraps normally. Gives 120 px at 1280×800 and 72 px at 375×667 |
| `#result-value` | inherits the font-size of `#result` (do not set its own) |
| Die canvas CSS size | square, `width = height = min(55vmin, 34vh, 360px)`; backing store = CSS size × `min(devicePixelRatio, 2)`; redraw on `resize` |
| Die-type choice | the six options in one row at 375 px width; native radio inputs may be visually restyled but must stay in the accessibility tree and keyboard-operable (arrow keys move and select, native behaviour) |
| Button | min height 48 px, min width 160 px, font-size ≥ 20 px |
| Focus | `:focus-visible` on the button and the radios (or the label after a focused radio) shows `outline: 3px solid #1a4fd6; outline-offset: 2px` |
| Fit | at 375×667 and 1280×800, `#die`, `#result`, `#die-type` and `#roll` lie fully inside the viewport with no scrolling, both before the first throw (two-line "Tryck på Kasta") and after |

## 4. In-page JavaScript contract

All code is inside the one inline `<script>`, ES2017+, `"use strict"`, no modules, no globals other than
`window.tarningDebug`.

### 4.1 Constants
`ROLL_MS = 1000` (animation duration), `SAFETY_MS = ROLL_MS + 150` (fallback timer).

### 4.2 Randomness (SW-003)
`randomInt(n)`: uniform integer 1..n by rejection sampling on one `Uint32Array(1)` filled by
`crypto.getRandomValues`: `limit = 4294967296 - (4294967296 % n)`; draw until `x < limit`; return
`(x % n) + 1`. No `Math.random` for results (`Math.random` is allowed only for visual spin signs).

### 4.3 Geometry (SW-002)
Coordinates: right-handed, x to the right, y up, z towards the viewer. Orthographic projection. Every
solid is scaled so its circumradius is 1; on canvas the radius is `0.40 × canvas side`, centred.
`φ = (1 + √5) / 2`.

| Sides | Solid | Vertices before scaling | Face polygon |
|---|---|---|---|
| 4 | tetrahedron | (1,1,1), (1,−1,−1), (−1,1,−1), (−1,−1,1) | triangle |
| 6 | cube | (±1,±1,±1) | square |
| 8 | octahedron | (±1,0,0), (0,±1,0), (0,0,±1) | triangle |
| 10 | pentagonal trapezohedron | apexes (0,0,±1); upper ring Uₖ = (cos 72k°, sin 72k°, +a); lower ring Lₖ = (cos(72k+36)°, sin(72k+36)°, −a), k = 0..4, a = 0.105573 | kite: upper faces (T, Uₖ, Lₖ, Uₖ₊₁), lower faces (B, Lₖ₋₁, Uₖ, Lₖ) |
| 12 | dodecahedron | (±1,±1,±1), (0,±1/φ,±φ), (±1/φ,±φ,0), (±φ,0,±1/φ) | pentagon |
| 20 | icosahedron | (0,±1,±φ), (±1,±φ,0), (±φ,0,±1) | triangle |

Faces are found by brute-force convex hull (planes through vertex triples with all other vertices on one
side, tolerance 1e-6, coplanar vertices merged and ordered counter-clockwise seen from outside), or from
explicit tables; the result must match the polygon kind above. Face count equals the number of sides.

**Face numbering**: sort faces by outward normal `n` descending on `n.z`, ties (|Δ| < 1e-6) by
`atan2(n.y, n.x)` ascending; face at index i carries value i + 1.
**Face up-vector** `u`: first rotate each face's counter-clockwise vertex list so that its first vertex
v0 is: for T10 the apex (the vertex with |z| = 1); for all other solids the vertex with the largest y
(ties: largest x, then largest z). Then: for T6 (square faces) `u` = unit vector from the centroid to the
midpoint of edge v0→v1, so the square lands upright with pips aligned to its edges; for every other solid
`u` = unit vector from the centroid to v0 (a corner, or the T10 apex, points up). `u` lies in the face
plane, so `u ⟂ n`.

**Landing orientation** `landing(sides, value)`: the rotation R such that R·n = (0,0,1) and R·u = (0,1,0)
for that face, followed by the fixed tilt `TILT = Ry(−10°) · Rx(12°)` (applied after, i.e.
`TILT · R`). The tilt shows depth while the result face remains the most viewer-facing face (the angle
between adjacent face normals is ≥ 41.8° for every solid; the tilt is < 16°).
**Rest pose** shown at load and after a type change: `landing(sides, 1)`.

### 4.4 Drawing (SW-002)
Flat shading per visible face (`R·n` has z > 0): brightness `0.35 + 0.65 × max(0, n′·L)` with
`L = normalize(−0.4, 0.6, 0.7)` applied to the base colour; edge stroke as in section 3; a soft elliptical
shadow below the die. Labels are drawn in face-local coordinates through `ctx.setTransform` built from
the projected face axes, so they foreshorten with the face. T6: pips in the standard 1–6 layout
(3×3 grid at 0 and ±0.5 of the half-edge along the face axes `u` and `n × u`, pip radius 0.11 × edge). Other dice: the value as digits, bold system font,
height ≈ 0.45 × the face's inscribed-circle diameter; on T10, T12 and T20 the values 6 and 9 get a short
underline.

### 4.5 Renderer object (SW-002 implements, SW-003 calls)
```js
const Renderer = {
  init(canvas),                 // size canvas, attach resize redraw
  setShape(sides),              // switch solid, draw rest pose
  showFinal(sides, value),      // draw landing(sides, value) now (may coalesce to the next frame)
  roll(sides, value, durationMs, onDone) // SW-003: animate to landing(sides, value); call onDone() exactly once
};
```
SW-002 delivers `roll` as a function that draws `showFinal` immediately and calls `onDone()` on the next
animation frame; SW-003 replaces its body with the animation.

### 4.6 Roll animation (SW-003)
From the current orientation `Q0` to `Q1 = landing(sides, value)` with eased progress
`e(t) = 1 − (1 − t)³`, `t = elapsed / durationMs` clamped to [0, 1]:
`Q(t) = Rx(sx · 4π · (1 − e)) · Ry(sy · 3π · (1 − e)) · slerp(Q0, Q1, e)`, with `sx, sy ∈ {−1, +1}`
chosen per throw. Driven by `requestAnimationFrame`; at `t = 1` the pose is exactly `Q1`. A `setTimeout`
at `SAFETY_MS` finishes the roll (draw `Q1`, `onDone`) if no frame has done so (background tabs).

### 4.7 Throw controller (SW-003)
Click on `#roll` (Enter/Space are native for a `<button>`):
1. `n = Number(#die.dataset.sides)`, `v = randomInt(n)`.
2. If `matchMedia('(prefers-reduced-motion: reduce)').matches` (evaluated on every click): in the same
   task, before the handler returns, set `#die.dataset.value = v`, `data-state = landed`,
   `#result-die = "T<n>: "`, `#result-value = v`, call `Renderer.showFinal(n, v)`. Never disable anything.
3. Otherwise: set `#roll.disabled = true`, `#die-type.disabled = true`, `data-state = rolling`, add
   `is-stale` to `#result-value`, call `Renderer.roll(n, v, ROLL_MS, onLand)`. `onLand` performs the
   updates of step 2, removes `is-stale`, re-enables both controls and, if the button had focus when
   clicked, calls `#roll.focus()`.

### 4.8 Test hook (SW-002 creates; SW-003 keeps it working)
```js
window.tarningDebug = {
  faceCount(),        // number of faces of the current solid
  faceSizes(),        // array of vertex counts per face, in numbering order
  frontFaceValue(),   // value of the face whose current rotated normal has the largest z
  show(sides, value)  // Renderer.setShape(sides) then Renderer.showFinal(sides, value); no DOM text changes
};
```

## 5. `sitecheck` package (SW-001)

`python -m sitecheck html index.html` and `python -m sitecheck readme README.md`: print one line per
problem, exit 1 if any, else print `OK` and exit 0. Functions in `sitecheck/checks.py`:

| Function | Returns | Rules |
|---|---|---|
| `html_problems(text: str, size_bytes: int) -> list[str]` | problems | every forbidden item of section 2; `<html lang="sv">`; `<title>Tärning</title>`; contains `crypto.getRandomValues` and `requestAnimationFrame`; `size_bytes < 61440` |
| `readme_problems(text: str) -> list[str]` | problems | ≤ 60 lines; contains `index.html`, `Kasta`, `T20`; matches `(ingen\|inte\|utan)[^\n]{0,40}server` case-insensitively; contains at least one of `å ä ö` and the words `och` and `att` (Swedish heuristic) |

The `crypto.getRandomValues` and `requestAnimationFrame` rules fail on the SW-001 shell by design (that
code arrives with SW-002/SW-003); `python -m sitecheck html index.html` is first required to pass by
SW-003's verify. Do not weaken the rules to make an earlier card pass.

## 6. Test-harness contract (SW-001)

- `pyproject.toml`: `[project] name = "tarning-tests"`, `requires-python = ">=3.11"`, `dependencies = []`;
  `[project.optional-dependencies] dev = ["pytest>=8,<10", "pytest-cov>=5", "ruff>=0.6", "playwright>=1.47,<2"]`;
  pytest `testpaths = ["tests"]`, `pythonpath = ["."]`; coverage `source = ["sitecheck"]`; ruff
  `line-length = 120`, `target-version = "py311"`, `extend-exclude = [".factory", ".venv"]`, lint select
  `["E","F","W","I","B","UP","S","SIM"]`, per-file-ignores `"tests/**" = ["S101"]`, `"integration/**" = ["S101", "S603", "S607"]`.
- `factory.yaml`:
  ```yaml
  kind: python-web
  package: sitecheck
  start: "python -m http.server {port} --bind 127.0.0.1"
  port: 8000
  health: /index.html
  e2e: "pytest tests/e2e -q"
  a11y_pages: ["/index.html"]
  public: false
  ```
  The HTTP server exists only so the gate can run axe; all product tests open `file://`.
- `tests/conftest.py`: `collect_ignore = ["e2e"]` when both `E2E_BASE_URL` and `RUN_E2E` are unset, so the
  `software.tests` gate runs only unit tests; the e2e gate (sets `E2E_BASE_URL`) and card verify commands
  (set `RUN_E2E=1`) run the browser tests. Browser tests never use `E2E_BASE_URL`; they open `index_url`.
- `tests/e2e/conftest.py` fixtures (the only place for them):
  - `index_url` (session): `Path("index.html").resolve().as_uri()`.
  - `browser` (session): Chromium headless; `executable_path` from `PLAYWRIGHT_CHROMIUM_EXECUTABLE`
    when set; `--no-sandbox` when running as root.
  - `make_page(viewport=(1280, 800), reduced_motion="no-preference")` → new context + page at `index_url`,
    with `page.console_errors` (console `error` + `pageerror`) and `page.requests` (every request URL)
    collected; failure screenshot to `E2E_ARTIFACT_DIR`; contexts closed at teardown.
  - `page`: `make_page()` with defaults.
- Every e2e test asserts `page.console_errors == []` and that no request URL starts with `http:`,
  `https:`, `ws:` or `wss:`.
- Timed assertions use `performance.now()` inside one `page.evaluate` (click and observe in-page), not
  Python sleeps.

## 7. Cross-browser run (INT-001)

`bash integration/e2e/run.sh`: creates or reuses the venv `.factory/scratch/int-venv` with
`uv pip install -r pyproject.toml --extra dev`; Chromium from `PLAYWRIGHT_CHROMIUM_EXECUTABLE` or
`$PLAYWRIGHT_BROWSERS_PATH/chromium-*/chrome-linux*/chrome`; Firefox from Playwright's own browser,
installed if missing with `PLAYWRIGHT_BROWSERS_PATH=.factory/scratch/ms-playwright python -m playwright install firefox`;
then `pytest integration/e2e -q` against the page named by `INDEX_HTML` (default `index.html`, resolved to a `file://` URI). If Firefox cannot be obtained the script prints
`FIREFOX NOT VERIFIED: <reason>` and exits 3. It never reports Firefox as passed without running it.

## Generated contracts
| File | Produced by | Consumed by | Schema |
|---|---|---|---|
| `index.html` | SW-001 → SW-002 → SW-003 | SW-004 (labels), SW-005, INT-001, Delivery | sections 2–4 |
| `$E2E_ARTIFACT_DIR/render-T<N>.png` | `tests/e2e/test_render.py` (SW-002) | plan reviewer, red team (visual review of R-006) | PNG of `#die`, one per die type, landing pose of value N |
| `integration/e2e/report.md` | INT-001 | Delivery | what ran in which browser, versions, results |
