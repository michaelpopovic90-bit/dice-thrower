---
schema: factory.spec/1
title: Tärningskast – en statisk HTML-sida med 3D-tärningar
build_type: software
size: S
language: sv
---

## Summary

En enda fristående HTML-fil, `index.html`. Användaren väljer en tärningstyp, T4, T6, T8, T10, T12 eller T20, och klickar på knappen "Kasta". En tärning i 3D snurrar i ungefär en sekund och landar sedan med resultatsidan vänd mot betraktaren. Resultatet visas också som en stor siffra. All grafik ritas med egen JavaScript och CSS i filen, utan bibliotek. Filen behöver ingen server och ingen inloggning, och den fungerar när man öppnar den direkt i en webbläsare. Operatören får `index.html` och en kort `README.md` på svenska.

## Goals and non-goals

**Goals**
- Man kan slå en rättvis tärning av vanlig typ med ett klick, utan att installera något.
- Tärningen ser ut som en riktig tärning och rör sig som en.
- Resultatet går att läsa direkt och tydligt, även på avstånd och på en mobil.

**Non-goals**
- Inga spelregler, ingen poängräkning och ingen historik.
- Ingen nätverkskommunikation och ingen datalagring.
- Ingen fysiksimulering. Animationen är en snygg rotation och ingen simulering av ett riktigt kast.

## Users and usage

Operatören och personer i närheten, till exempel vid ett brädspel eller ett rollspel. Sidan används på dator eller mobil när någon behöver en tärning.

- Scenario 1: Användaren öppnar `index.html` genom att dubbelklicka på den. Sidan visar en T6 som stillastående 3D-tärning, ett tärningsval där T6 är vald, knappen "Kasta" och texten "Tryck på Kasta".
- Scenario 2: Användaren väljer T20 och klickar på "Kasta". En ikosaeder snurrar i ungefär en sekund och stannar med en sida mot betraktaren som visar resultatet, till exempel 17. Under tärningen visas 17 med stor text.
- Scenario 3: Användaren använder bara tangentbordet. Hen flyttar mellan tärningstyperna med piltangenterna, tabbar till "Kasta" och trycker Enter eller mellanslag.

## Requirements

### R-001 (must) En enda fristående fil
Produkten är en enda fil, `index.html`, där all HTML, CSS och JavaScript ligger inbäddad. Filen refererar inte till några externa resurser: inga `src`- eller `href`-adresser som börjar med `http:`, `https:` eller `//`, inga externa typsnitt och inga bibliotek. 3D-grafiken görs med CSS 3D-transformer eller med `<canvas>` och egen kod.
**Acceptance:** `index.html` finns i leveransens rot. Ingen annan `.html`-, `.js`- eller `.css`-fil krävs. En sökning efter `http:`, `https:` och `src="//"`/`href="//"` i attribut i `index.html` ger noll träffar. När sidan laddas och ett kast görs i en headless webbläsare görs inga nätverksanrop.

### R-002 (must) Fungerar utan server
Sidan fungerar fullt ut när den öppnas via en `file://`-adress i en aktuell version av Chrome, Firefox, Safari eller Edge.
**Acceptance:** Ett Playwright-test öppnar `file://.../index.html` i Chromium och Firefox, väljer varje tärningstyp i tur och ordning, klickar på knappen, väntar tills animationen är klar och ser ett resultat i rätt intervall. Inga fel loggas i konsolen.

### R-003 (must) Knappen "Kasta"
Sidan har exakt en knapp, ett `<button>`-element med den synliga texten "Kasta". Medan en animation pågår har knappen `disabled`, och den aktiveras igen när tärningen har landat.
**Acceptance:** Ett test hittar exakt ett element med rollen `button` och namnet "Kasta". Direkt efter ett klick är knappen inaktiverad, och efter högst 1 600 ms är den aktiv igen.

### R-004 (must) Val av tärningstyp
Ovanför knappen finns en grupp radioknappar med etiketten "Tärning" och alternativen "T4", "T6", "T8", "T10", "T12" och "T20". "T6" är förvald. Tärningen som visas byter form direkt när man väljer en annan typ.
**Acceptance:** Ett test hittar en `radiogroup` eller `fieldset` med namnet "Tärning" och exakt sex element med rollen `radio`, med namnen ovan. "T6" är vald när sidan laddas. När ett alternativ väljs får tärningselementet attributet `data-sides` med motsvarande tal (4, 6, 8, 10, 12 eller 20).

### R-005 (must) Rättvist slag 1–N
Varje kast ger ett heltal från 1 till N, där N är antalet sidor på den valda tärningen. Talet slumpas med `crypto.getRandomValues`, och metoden har ingen skevhet mellan utfallen, till exempel för att skeva värden förkastas.
**Acceptance:** Med `prefers-reduced-motion: reduce` emulerad (se R-008) gör ett test N × 1 000 kast för T6 och T20. Varje resultat är ett heltal i 1–N, och varje värde förekommer mellan 850 och 1 150 gånger. För T4, T8, T10 och T12 görs N × 200 kast. Alla resultat ligger i 1–N och alla värden förekommer. Koden innehåller `crypto.getRandomValues`.

### R-006 (must) 3D-tärning med animation
Tärningen visas som en tredimensionell kropp med ljussättning eller skuggning så att djupet syns: T4 som tetraeder, T6 som kub, T8 som oktaeder, T10 som femsidig trapetsoeder, T12 som dodekaeder och T20 som ikosaeder. Vid ett kast roterar tärningen kring flera axlar i 600–1 500 ms. Sedan stannar den med den sida som visar resultatet vänd mot betraktaren. Sidorna är märkta: T6 med prickar och övriga med siffror.
**Acceptance:** Ett test klickar på "Kasta" och tar två skärmbilder av tärningselementet 150 ms och 300 ms efter klicket. Bilderna skiljer sig åt. Resultatytan uppdateras mellan 600 och 1 500 ms efter klicket. När tärningen har landat har tärningselementet `data-value` lika med det visade resultatet. Att formerna är rätt och att resultatsidan vetter framåt granskas visuellt på skärmbilder av alla sex typer.

### R-007 (must) Resultatet visas stort
Resultatet visas som en siffra under tärningen, centrerat, med en teckenstorlek på minst 96 px i ett fönster som är 1280×800. I ett fönster som är 375×667 är teckenstorleken minst 72 px. Tärningen, tärningsvalet, knappen och resultatet syns då utan att man behöver scrolla. Medan tärningen snurrar visas det förra resultatet nedtonat, eller "…".
**Acceptance:** Ett test läser resultatelementets beräknade `font-size` i båda fönsterstorlekarna och kontrollerar gränsvärdena. Tärningselementet, radiogruppen, knappen och resultatelementet ligger helt inom den synliga ytan i 375×667.

### R-008 (must) Respekterar reducerad rörelse
Om webbläsaren rapporterar `prefers-reduced-motion: reduce` hoppar sidan över rotationen. Tärningen visas då direkt i sitt slutläge och resultatet visas omedelbart.
**Acceptance:** Med `reducedMotion: 'reduce'` emulerad i Playwright uppdateras resultatet inom 100 ms efter klicket, och knappen är aldrig inaktiverad längre än 100 ms.

### R-009 (must) Svenskt gränssnitt
All synlig text är på svenska och `<html>` har `lang="sv"`. Sidans titel är "Tärning". Innan första kastet visar resultatytan texten "Tryck på Kasta".
**Acceptance:** Ett test kontrollerar `lang="sv"`, att `document.title` är "Tärning" och att resultatytan visar "Tryck på Kasta" innan något klick har gjorts.

### R-010 (must) README på svenska
Leveransen innehåller `README.md` på svenska. Den beskriver vad sidan gör, hur man öppnar den (dubbelklicka på filen eller dra den till webbläsaren), vilka tärningar som finns och att den inte behöver server eller internet.
**Acceptance:** `README.md` finns, är på svenska och har högst 60 rader. Den innehåller orden "index.html", "Kasta" och "T20" och nämner att ingen server behövs.

### R-011 (should) Tillgänglighet
Knappen och tärningsvalet går att använda med tangentbordet och har synlig fokusmarkering. Resultatytan har `aria-live="polite"` så att skärmläsare läser upp varje nytt resultat, till exempel "T20: 17", först när tärningen har landat. Tärningsgrafiken är dold för skärmläsare (`aria-hidden="true"`). Kontrasten mellan text och bakgrund är minst 4.5:1.
**Acceptance:** Ett test fokuserar knappen, trycker Enter och ser ett nytt resultat. Det väljer "T12" med piltangenterna och ser `data-sides="12"`. Resultatelementet har `aria-live="polite"` och tärningselementet har `aria-hidden="true"`. En kontroll med axe-core rapporterar inga överträdelser av graderna "serious" eller "critical".

### R-012 (should) Lagom filstorlek
`index.html` är mindre än 60 kB.
**Acceptance:** Filstorleken är under 61 440 byte.

### R-013 (should) Jämn animation
Animationen använder `requestAnimationFrame` eller CSS-transitioner och går mjukt på en vanlig mobil.
**Acceptance:** Koden använder `requestAnimationFrame` eller CSS `transition`/`animation` för rotationen. Under en animation i Chromium på dator är medeltiden mellan bildrutorna under 20 ms, mätt med `requestAnimationFrame`-tidsstämplar i testet.

## Constraints

- Ren HTML, CSS och JavaScript (ES2017 eller nyare) utan ramverk, bibliotek eller byggsteg. Ingen WebGL-bibliotek; egen kod i canvas eller CSS 3D.
- Ingen server, ingen inloggning, ingen nätverkstrafik och ingen datalagring.
- Fungerar i aktuella versioner av Chrome, Firefox, Safari och Edge, både på dator och mobil.

## Interfaces and environment

- Körs lokalt i operatörens webbläsare via `file://`. Ingen hosting.
- Inga externa system, inga konton och inga API-nycklar.

## Deliverables

- `index.html` – den fristående tärningssidan med 3D-tärningar.
- `README.md` – kort bruksanvisning på svenska.

## Assumptions and defaults

- Tärningstyperna är standardsetet för rollspel, T4, T6, T8, T10, T12 och T20, och T6 är förvald. (Öppen fråga 1.)
- Man kastar en tärning åt gången, inte flera samtidigt. (Öppen fråga 2.)
- T6 har prickar och övriga tärningar har siffror på sidorna. (Öppen fråga 3.)
- T10 är numrerad 1–10, inte 0–9.
- Animationen varar ungefär 1 sekund och består av en rotation som bromsas in. Det finns ingen fysiksimulering och inget ljud.
- Knappen är inaktiverad medan tärningen snurrar, så att man inte kan starta ett nytt kast mitt i ett.
- Resultatet visas både på tärningen och som en stor siffra under den. Den stora siffran är det som gäller.
- Slumpen kommer från `crypto.getRandomValues`, och skeva värden förkastas så att alla utfall är exakt lika sannolika.
- `prefers-reduced-motion` respekteras genom att animationen hoppas över.
- Det valda tärningsvalet sparas inte mellan besök.
- Innan första kastet visar resultatytan texten "Tryck på Kasta". Sidans titel är "Tärning".
- Layouten är centrerad och responsiv, med neutrala färger (mörk text på ljus bakgrund) och en tärning i en ljus färg med tydliga markeringar.

## Out of scope

- Ljud och fysiksimulering (studsar och kollisioner).
- Flera tärningar i samma kast, summering och modifierare (t.ex. "2T6+3").
- Egna tärningar med valfritt antal sidor och procenttärning (T100).
- Historik över kast och sparad data.
- Webbserver, hosting, PWA och offlineinstallation som app.
- Andra språk än svenska.

## Risks and open points

- Öppen fråga 1: vilka tärningstyper som ska finnas. Standardvalet är T4, T6, T8, T10, T12 och T20.
- Öppen fråga 2: om "ett par" betyder två tärningar per kast. Standardtolkningen är olika typer och en tärning per kast.
- Öppen fråga 3: prickar eller siffror på T6. Standardvalet är prickar.
- Att varje polyeder landar med exakt rätt sida framåt är det svåraste momentet. Det kontrolleras med `data-value` och granskas visuellt, men skärmbilderna kan inte bevisa det helt automatiskt.
- Mycket gamla webbläsare saknar `crypto.getRandomValues` eller stöd för 3D. Alla webbläsare som stöds har båda, så sidan använder ingen reservlösning.
- Bygget ligger i den övre delen av storlek S.
