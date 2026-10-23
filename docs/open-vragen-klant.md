# First Line – open punten

## Bevestigen bij de klant
- Voorgerecht firmamenu: "гъбен сос иньоки" — klopt "гъбен сос, иньоки"?
- Openingstijden (staan nergens op de site)
- Live muziek: vaste avonden/programma voor op de site?
- Restaurantmenu (à la carte) voor een menupagina
- Mogen we "4,2 в Google от над 1300 отзива" tonen? (stand 23-10-2026)
- Afstand: "около 25 км северно от Варна" ok?

## Talen
- Site in BG (root), EN (/en/) en RU (/ru/). Laat EN en RU door een moedertaalspreker nalezen voor livegang.
- Er staan bewust geen prijzen op de site; prijzen en voorwaarden gaan mee in de offerte.

## Technisch
- Formulieren gaan naar kranevo.firstline@gmail.com via FormSubmit: eerste inzending bevestigen via de activatiemail
- Domein kiezen + deployen (Vercel)
- Na de renovatie: nieuwe foto's (shotlijst in chat), hero van de homepage vervangen

## Foto's
- img/gevel.jpg komt van Google (gast-upload) — wordt niet meer gebruikt, niet live zetten
- Originelen staan in fotos-aangeleverd/, verkleinde versies in img/ en img/galerij/

## Pagina's aanpassen
- Inhoud staat in src/bg, src/en, src/ru (één bestand per pagina), header/footer/galerij in build.py
- Na wijzigen: `python3 build.py`
- Bij wijziging aan css/js: VERSION in build.py ophogen
