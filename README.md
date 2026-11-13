# Tärning

## Vad det här är

`index.html` är en enda fristående sida med en 3D-tärning (T4, T6, T8, T10, T12, T20).
Du väljer tärning, trycker på "Kasta" och får ett rättvist slumpat resultat.
Ingen server och inget internet behövs; sidan öppnas direkt i webbläsaren.

## Status

Alla 10 `must`-krav och alla 3 `should`-krav är verifierade av verktyg. Inga krav
saknas och inga kända problem finns. Safari/WebKit är inte provat; det behöver du
prova själv på en Mac eller iPhone (se `docs/LAUNCH_CHECKLIST.md`). Se
[VERIFICATION_REPORT.md](VERIFICATION_REPORT.md).

## Innehåll

| Fil eller katalog | Vad det är |
|---|---|
| `index.html` | Hela produkten: HTML, CSS och JavaScript i en fil |
| `README.md` | Den här filen |
| `docs/INSTALL.md` | Så öppnar du sidan eller lägger ut den |
| `docs/LAUNCH_CHECKLIST.md` | Kontrollera före användning |
| `tests/`, `sitecheck/` | Automatiska tester och kontroller |
| `integration/e2e/` | Körning i Chromium och Firefox över `file://` |
| `BUILD_SPEC.md`, `plan/` | Specifikation och plan från bygget |

## Nästa steg

1. Öppna `index.html` med dubbelklick, se [docs/INSTALL.md](docs/INSTALL.md).
2. Välj tärning och tryck på "Kasta". Med tangentbord: piltangenter, Tab, Enter.
3. Prova i Safari om du ska använda den där, se [docs/LAUNCH_CHECKLIST.md](docs/LAUNCH_CHECKLIST.md).

## Bra att veta

- Med inställningen minskad rörelse hoppar sidan över animationen och visar resultatet direkt.
- Ingenting sparas och ingenting skickas någonstans.

## Kända problem

Inga. Enda öppna punkten är att Safari/WebKit inte har provats.
