# Verifieringsrapport: Tärningskast – en statisk HTML-sida med 3D-tärningar

- Bygge: `b87e3aff0`  
- Typ: software  
- Storlek: S  
- Status: DELIVERED

## 1. Utlåtande

Alla krav verifierades av verktyg och inga kända brister kvarstår.

- Krav: 13 (verifierat med verktyg: 13)
- Kort: 6 (DONE: 6)

## 2. Krav och bevis

| Krav | Prioritet | Status | Bevis |
|---|---|---|---|
| R-001 En enda fristående fil | must | verifierat med verktyg | SW-001: verify pass, software.lint pass, software.tests pass, software.e2e pass; SW-002: verify pass, software.lint pass, software.tests pass, software.e2e pass; SW-003: verify pass, software.lint pass, software.tests pass, software.e2e pass; SW-005: verify pass, software.e2e pass; INT-001: verify pass |
| R-002 Fungerar utan server | must | verifierat med verktyg | SW-005: verify pass, software.e2e pass; INT-001: verify pass |
| R-003 Knappen "Kasta" | must | verifierat med verktyg | SW-001: verify pass, software.lint pass, software.tests pass, software.e2e pass; SW-003: verify pass, software.lint pass, software.tests pass, software.e2e pass; SW-005: verify pass, software.e2e pass |
| R-004 Val av tärningstyp | must | verifierat med verktyg | SW-001: verify pass, software.lint pass, software.tests pass, software.e2e pass; SW-005: verify pass, software.e2e pass |
| R-005 Rättvist slag 1–N | must | verifierat med verktyg | SW-003: verify pass, software.lint pass, software.tests pass, software.e2e pass |
| R-006 3D-tärning med animation | must | verifierat med verktyg | SW-002: verify pass, software.lint pass, software.tests pass, software.e2e pass; SW-003: verify pass, software.lint pass, software.tests pass, software.e2e pass; SW-005: verify pass, software.e2e pass |
| R-007 Resultatet visas stort | must | verifierat med verktyg | SW-001: verify pass, software.lint pass, software.tests pass, software.e2e pass; SW-005: verify pass, software.e2e pass |
| R-008 Respekterar reducerad rörelse | must | verifierat med verktyg | SW-003: verify pass, software.lint pass, software.tests pass, software.e2e pass |
| R-009 Svenskt gränssnitt | must | verifierat med verktyg | SW-001: verify pass, software.lint pass, software.tests pass, software.e2e pass; SW-005: verify pass, software.e2e pass |
| R-010 README på svenska | must | verifierat med verktyg | SW-004: verify pass, core.files pass |
| R-011 Tillgänglighet | should | verifierat med verktyg | SW-001: verify pass, software.lint pass, software.tests pass, software.e2e pass; SW-003: verify pass, software.lint pass, software.tests pass, software.e2e pass; SW-005: verify pass, software.e2e pass |
| R-012 Lagom filstorlek | should | verifierat med verktyg | SW-001: verify pass, software.lint pass, software.tests pass, software.e2e pass; SW-002: verify pass, software.lint pass, software.tests pass, software.e2e pass; SW-003: verify pass, software.lint pass, software.tests pass, software.e2e pass |
| R-013 Jämn animation | should | verifierat med verktyg | SW-003: verify pass, software.lint pass, software.tests pass, software.e2e pass |

## 3. Grindresultat (slutkontroll)

| Kort | Kontroll | Status | Sammanfattning | Rapportfil |
|---|---|---|---|---|
| SW-001 | verify | pass | verify: PASS |  |
| SW-001 | software.lint | pass | software.lint: PASS (3 checks) | .factory/gates/final-SW-001-software_lint-10f0210e.json |
| SW-001 | software.tests | pass | software.tests: PASS (4 checks) | .factory/gates/final-SW-001-software_tests-942d08a6.json |
| SW-001 | software.e2e | pass | software.e2e: PASS (6 checks) | .factory/gates/final-SW-001-software_e2e-a855168f.json |
| SW-002 | verify | pass | verify: PASS |  |
| SW-002 | software.lint | pass | software.lint: PASS (3 checks) | .factory/gates/final-SW-002-software_lint-d27ae5fa.json |
| SW-002 | software.tests | pass | software.tests: PASS (4 checks) | .factory/gates/final-SW-002-software_tests-00939920.json |
| SW-002 | software.e2e | pass | software.e2e: PASS (6 checks) | .factory/gates/final-SW-002-software_e2e-f573a5be.json |
| SW-003 | verify | pass | verify: PASS |  |
| SW-003 | software.lint | pass | software.lint: PASS (3 checks) | .factory/gates/final-SW-003-software_lint-40b63ee8.json |
| SW-003 | software.tests | pass | software.tests: PASS (4 checks) | .factory/gates/final-SW-003-software_tests-57cb2a48.json |
| SW-003 | software.e2e | pass | software.e2e: PASS (6 checks) | .factory/gates/final-SW-003-software_e2e-c6258cc6.json |
| SW-004 | verify | pass | verify: PASS |  |
| SW-004 | core.files | pass | core.files: PASS (2 checks) | .factory/gates/final-SW-004-core_files-84e6f7e3.json |
| SW-005 | verify | pass | verify: PASS |  |
| SW-005 | software.e2e | pass | software.e2e: PASS (6 checks) | .factory/gates/final-SW-005-software_e2e-4e62679c.json |
| INT-001 | verify | pass | verify: PASS |  |

## 4. Kort

| Kort | Titel | Avdelning | Status | Försök | Eskaleringar |
|---|---|---|---|---|---|
| SW-001 | Create the page shell, the static checker and the browser test harness | software | DONE | 2 | 0 |
| SW-002 | Render the six dice as shaded 3D polyhedra on the canvas | software | DONE | 1 | 0 |
| SW-003 | Add the fair throw with the multi-axis roll animation and reduced-motion path | software | DONE | 1 | 0 |
| SW-004 | Write the Swedish README for the operator | software | DONE | 1 | 0 |
| SW-005 | Cover the three user journeys and the full file:// run end to end | software | DONE | 1 | 0 |
| INT-001 | Run the page in Chromium and Firefox over file:// and report | integration | DONE | 1 | 0 |

## 5. Kända brister

Inga.

## 6. Kräver fysisk validering

**Från avdelningarna: integration**

- Assemble the real board into the printed enclosure with all cables attached; integration checks used box models of components.

**Rapporterat av agenter**

- INT-001: Safari/WebKit on the operator's Mac or iPhone: page load, throw and result display were not run here.
- INT-001: Real mobile touch behaviour was not tested; only headless desktop Chromium and Firefox ran.

## 7. Antaganden som agenter gjort

- SW-001: Cache directories are removed and not committed; .gitignore is not owned by this card so it was left alone.
- SW-004: Described the die groups using the fieldset legend 'Tärning'.
- SW-004: The card's core.files command uses YAML-style params that the gate cannot parse; I ran it with JSON params instead.
- SW-002: T4 at rest shows only one full face plus a thin sliver of a second face, because the tilt is under 16 degrees and adjacent normals are 109 degrees apart. The shading test therefore requires the second brightness to cover at least 0.5% of the die pixels (about 1.2% for T4), not 2%. The brightness difference is about 16 of 255, which is at least 10.
- SW-002: Interface section 4.4 says to lay T6 pips along the axes u and n x u. I used u and u x n instead, which is the viewer's right, so the layout is not mirrored when seen from outside.
- SW-002: T10 uses explicit kite index tables instead of the hull. With a = 0.105573 the kites are not planar within the 1e-6 hull tolerance, so the hull gave 20 triangles.
- SW-002: Face labels are centred on the mean of the face vertices, which for the T10 kites is not the visual centre.
- SW-002: Shadow is an ellipse of radius 0.30 x 0.035 of the canvas side at 0.46 side below the centre, drawn at alpha 0.18.
- SW-002: showFinal draws immediately rather than waiting for the next frame.
- SW-003: Tests select die types with get_by_role('radio').check(force=True), as the shell tests do, because the restyled radio intercepts label clicks.
- SW-003: The frame-interval test measures the mean requestAnimationFrame interval over 900 ms after the click.
- SW-003: Fairness tests click #roll in a loop inside one page.evaluate under reduced motion.
- SW-005: The keyboard journey assumes the first Tab lands on the checked T6 radio and that four ArrowRight presses reach T20.
- SW-005: The keyboard test also asserts that focus stays on Kasta after landing, so Space works without another Tab.
- SW-005: Firefox is not covered here because INT-001 owns the cross-browser run.
- INT-001: The venv is created with `uv venv` plus `uv pip install` of pytest, playwright and ruff, instead of `uv pip install -r pyproject.toml --extra dev`; the dev extra also pulls in pytest-cov, which this run does not need.
- INT-001: A missing INDEX_HTML file exits 2 from run.sh before any browser starts.
- INT-001: The reduced-motion check clicks once per die type and measures click to landed state in-page, because the page sets the result synchronously in that mode.
- INT-001: Chromium is run with --no-sandbox when the process runs as root.

## 8. Användning

| Roll | Modell | Anrop | Tokens in | Tokens ut |
|---|---|---|---|---|
| architect | opus | 1 | 1291178 | 44656 |
| builder | sonnet | 7 | 1873132 | 56746 |
| delivery | sonnet | 1 | 91854 | 2657 |
| plan_reviewer | opus | 1 | 249950 | 10240 |
| red_team | sonnet | 1 | 120408 | 2046 |
| reviewer | sonnet | 3 | 316819 | 6499 |

- Modellanrop totalt: 14
- Aktiv tid: 0 h 47 min
- Tid i paus: 1 h 57 min
- Pauser på grund av användningsgräns: 1
- Uppskattat listpris (USD): 5.0601

Kostnadssiffror är uppskattningar till listpris. På ett abonnemang debiteras ingenting per anrop.

## 9. Köra kontrollerna igen

Kör varje kommando från paketets rotmapp. Grindar körs från en utcheckning av The Factory.

**Verifieringskommandon**

```sh
python -m pytest tests/unit -q && RUN_E2E=1 python -m pytest tests/e2e/test_page_shell.py -q   # SW-001
RUN_E2E=1 python -m pytest tests/e2e/test_render.py tests/e2e/test_page_shell.py -q   # SW-002
python -m sitecheck html index.html && RUN_E2E=1 python -m pytest tests/e2e/test_throw.py tests/e2e/test_fairness.py tests/e2e/test_render.py -q   # SW-003
python -m sitecheck readme README.md   # SW-004
python -m sitecheck html index.html && RUN_E2E=1 python -m pytest tests/e2e -q   # SW-005
bash integration/e2e/run.sh   # INT-001
```

**Grindar**

```sh
python departments/software/gates/lint.py --workdir .   # SW-001
python departments/software/gates/tests.py --workdir .   # SW-001
python departments/software/gates/e2e.py --workdir .   # SW-001
python departments/software/gates/lint.py --workdir .   # SW-002
python departments/software/gates/tests.py --workdir .   # SW-002
python departments/software/gates/e2e.py --workdir .   # SW-002
python departments/software/gates/lint.py --workdir .   # SW-003
python departments/software/gates/tests.py --workdir .   # SW-003
python departments/software/gates/e2e.py --workdir .   # SW-003
python factory/gates/files.py --workdir . --params '{"files": ["README.md"], "min_bytes": 800, "forbid": ["lorem ipsum", "TODO", "TBD"]}'   # SW-004
python departments/software/gates/e2e.py --workdir .   # SW-005
```
