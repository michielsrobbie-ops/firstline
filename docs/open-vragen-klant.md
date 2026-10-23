# First Line – open punten

## Bevestigen bij de klant
- Overnachting AquaLife: firmafeest-offerte zegt 30 €, bruiloftsfolder 35 € — welke geldt waarvoor?
- Voorgerecht firmamenu: "гъбен сос иньоки" — klopt "гъбен сос, иньоки"?
- Openingstijden (staan nergens op de site)
- Live muziek: vaste avonden/programma voor op de site?
- Restaurantmenu (à la carte) voor een menupagina
- Mogen we "4,2 в Google от над 1300 отзива" tonen? (stand 23-10-2026)
- Afstand: "около 25 км северно от Варна" ok?

## Technisch
- Formulieren gaan naar kranevo.firstline@gmail.com via FormSubmit: eerste inzending bevestigen via de activatiemail
- Domein kiezen + deployen (Vercel)
- Na de renovatie: nieuwe foto's (shotlijst in chat), hero van de homepage vervangen

## Foto's
- img/gevel.jpg komt van Google (gast-upload) — wordt niet meer gebruikt, niet live zetten
- Originelen staan in fotos-aangeleverd/, verkleinde versies in img/ en img/galerij/

## Pagina's aanpassen
- Inhoud staat in src/*.html, header/footer in build.py
- Na wijzigen: `python3 build.py`
- Bij wijziging aan css/js: VERSION in build.py ophogen
