# Installation

Det finns inget att installera. Produkten är filen `index.html`.

## Öppna lokalt

1. Hitta `index.html` i leveransens rot.
2. Dubbelklicka på filen, eller dra den till ett fönster i Chrome, Firefox, Safari eller Edge.
3. Du ska se en T6, valet "Tärning" med T6 valt, knappen "Kasta" och texten "Tryck på Kasta".

Ingen server, inloggning eller internetanslutning behövs. Filen anropar inga externa adresser.

## Lägga ut på en webbserver (valfritt)

Kopiera bara `index.html` till valfri webbplats som kan visa statiska filer. Det finns
inga inställningar att fylla i och inga hemligheter eller API-nycklar.

## Köra de automatiska kontrollerna (valfritt)

Kontrollerna finns i paketet men kräver Python, Playwright och webbläsare:

    python -m sitecheck html index.html
    python -m sitecheck readme README.md
    bash integration/e2e/run.sh

Det sista kommandot kör Chromium och Firefox över `file://`. Första gången behöver det
nätverk för att hämta Firefox. Jag har inte kört om dem under leveransen; resultatet
från bygget står i `integration/e2e/report.md`.
