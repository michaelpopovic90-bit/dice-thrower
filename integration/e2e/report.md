# INT-001 — index.html over file:// in Chromium and Firefox

Contract: plan/INTERFACES.md section 7 (R-001, R-002). Side A: the delivered `index.html` opened as a
`file://` URI. Side B: Playwright 1.65.1 driving real headless browsers. Nothing is mocked or faked.

## Browsers used
| Engine | Version | Build |
|---|---|---|
| Chromium | 158.0.8127.18 | Playwright chromium-1254 (shared cache / `PLAYWRIGHT_CHROMIUM_EXECUTABLE`) |
| Firefox | 159.0 | Playwright firefox-1572, installed by `run.sh` into `.factory/scratch/ms-playwright` when missing |

## What ran (per browser; `test_cross_browser.py`)
1. `test_all_dice_throw`: for T4, T6, T8, T10, T12, T20 in turn: select the type, click "Kasta", wait for
   `#roll` to be enabled; assert `#result-value` is an integer in 1..N and equals `#die` `data-value`. After
   all six throws: zero console errors / page errors and zero `http:`/`https:`/`ws:`/`wss:` requests.
2. `test_reduced_motion_is_immediate`: context with `reducedMotion: 'reduce'`; for each die type the
   click-to-result time, measured in-page with `performance.now()`, is at most 100 ms, the die state is
   `landed`, and value equals `data-value`; same console/network assertions.

## Results
Two consecutive runs of `bash integration/e2e/run.sh`: 4 passed each (2 tests x 2 browsers), exit 0, about
23 s. `INDEX_HTML=.factory/scratch/missing.html` exits 2 (the check can fail). `ruff check` and
`ruff format --check` on `integration` are clean. No browser process is left running.

## Not run
- **Safari/WebKit: not run. Needs operator validation** on a Mac or iPhone (see plan/RISKS.md).
- Edge: not run; it is Chromium-based, so Chromium results are the proxy.

## Re-run
`bash integration/e2e/run.sh` (optional `INDEX_HTML=<path>`). Exit 3 with `FIREFOX NOT VERIFIED: <reason>`
if Firefox cannot be installed (needs network the first time only). Browser versions are written by the
test to `.factory/scratch/int-browsers.json`.
