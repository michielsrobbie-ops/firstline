"""Bouwt de pagina's van First Line in drie talen (BG, EN, RU).

Structuur:
  src/<taal>/<sleutel>.html   alleen de <main>-inhoud, met bovenaan een kopblok tussen <!-- -->
  sleutels: home, weddings, corporate, gallery, contact
  De galerij wordt hier gegenereerd (GALLERY_ALTS), niet uit src.

In src mag je gebruiken:
  {{base}}       pad naar de root (leeg voor BG, "../" voor EN/RU) -> voor img/, css/, js/
  {{weddings}}   link naar de bruiloftspagina in dezelfde taal (idem home, corporate, gallery, contact)

Gebruik:  python3 build.py
Na een wijziging aan css/js: VERSION ophogen, anders zien bezoekers de oude versie.
"""
import pathlib
import re

ROOT = pathlib.Path(__file__).parent
VERSION = "20261023d"
KEYS = ["home", "weddings", "corporate", "gallery", "contact"]

LANGS = {
    "bg": {
        "dir": "",
        "label": "BG",
        "pages": {"home": "index.html", "weddings": "svatbi.html", "corporate": "firmeni-tarzhestva.html",
                  "gallery": "galeria.html", "contact": "kontakt.html"},
        "nav": {"home": "Начало", "weddings": "Сватби", "corporate": "Фирмени тържества",
                "gallery": "Галерия", "contact": "Контакт"},
        "t": {"phone_label": "088 686 1001", "inquiry": "Запитване", "menu": "Меню", "nav_aria": "Основна навигация", "home_aria": "First Line – начало",
              "address": "Централен плаж, 9649 Кранево", "follow": "Следвайте ни", "site": "Уебсайт",
              "pages_aria": "Страници", "lang_aria": "Език", "gallery_title": "Галерия – First Line, Кранево",
              "gallery_desc": "Снимки на First Line Restaurant & Bar на Централния плаж в Кранево: залата, плажът, сватби и събития.",
              "gallery_h1": "Галерия", "gallery_lead": "Залата, плажът и събитията, които сме организирали.",
              "photo": "Снимка", "close": "Затвори", "prev": "Предишна снимка", "next": "Следваща снимка"},
    },
    "en": {
        "dir": "en/",
        "label": "EN",
        "pages": {"home": "index.html", "weddings": "weddings.html", "corporate": "corporate-events.html",
                  "gallery": "gallery.html", "contact": "contact.html"},
        "nav": {"home": "Home", "weddings": "Weddings", "corporate": "Corporate events",
                "gallery": "Gallery", "contact": "Contact"},
        "t": {"phone_label": "+359 88 686 1001", "inquiry": "Enquire", "menu": "Menu", "nav_aria": "Main navigation", "home_aria": "First Line – home",
              "address": "Central Beach, 9649 Kranevo, Bulgaria", "follow": "Follow us", "site": "Website",
              "pages_aria": "Pages", "lang_aria": "Language", "gallery_title": "Gallery – First Line, Kranevo",
              "gallery_desc": "Photos of First Line Restaurant & Bar on Central Beach in Kranevo: the venue, the beach, weddings and events.",
              "gallery_h1": "Gallery", "gallery_lead": "The venue, the beach and the events we have hosted.",
              "photo": "Photo", "close": "Close", "prev": "Previous photo", "next": "Next photo"},
    },
    "ru": {
        "dir": "ru/",
        "label": "RU",
        "pages": {"home": "index.html", "weddings": "svadby.html", "corporate": "korporativy.html",
                  "gallery": "galereya.html", "contact": "kontakty.html"},
        "nav": {"home": "Главная", "weddings": "Свадьбы", "corporate": "Корпоративы",
                "gallery": "Галерея", "contact": "Контакты"},
        "t": {"phone_label": "+359 88 686 1001", "inquiry": "Запрос", "menu": "Меню", "nav_aria": "Основная навигация", "home_aria": "First Line – главная",
              "address": "Центральный пляж, 9649 Кранево, Болгария", "follow": "Мы в соцсетях", "site": "Сайт",
              "pages_aria": "Страницы", "lang_aria": "Язык", "gallery_title": "Галерея – First Line, Кранево",
              "gallery_desc": "Фотографии First Line Restaurant & Bar на Центральном пляже в Кранево: зал, пляж, свадьбы и мероприятия.",
              "gallery_h1": "Галерея", "gallery_lead": "Зал, пляж и мероприятия, которые мы организовали.",
              "photo": "Фото", "close": "Закрыть", "prev": "Предыдущее фото", "next": "Следующее фото"},
    },
}

# Galerij: (bestandsnummer, alt BG, alt EN, alt RU)
GALLERY_ALTS = [
    (1, "Залата, подредена с кръгли маси за празнично събитие", "The hall set with round tables for a celebration", "Зал с круглыми столами, сервированными для праздника"),
    (2, "Арка за изнесен ритуал на плажа", "Ceremony arch on the beach", "Арка для выездной церемонии на пляже"),
    (3, "Лаундж със стъклени стени към плажа", "Lounge with glass walls facing the beach", "Лаунж со стеклянными стенами с видом на пляж"),
    (4, "Кръгла маса с изглед към морето", "Round table with a sea view", "Круглый стол с видом на море"),
    (5, "Младоженци с кумове на плажа", "Bride and groom with their witnesses on the beach", "Молодожёны со свидетелями на пляже"),
    (6, "Маса на младоженците с цветя", "Head table decorated with flowers", "Стол молодожёнов, украшенный цветами"),
    (7, "Лаундж с кресла и маси", "Lounge with armchairs and tables", "Лаунж с креслами и столиками"),
    (8, "Пътеката към морето вечер", "The boardwalk to the sea in the evening", "Дорожка к морю вечером"),
    (9, "Дълга маса с бели столове", "Long table with white chairs", "Длинный стол с белыми стульями"),
    (10, "Подредена маса с цветя и изглед към плажа", "Table set with flowers and a beach view", "Сервированный стол с цветами и видом на пляж"),
    (11, "Маса на младоженците с бели цветя", "Head table with white flowers", "Стол молодожёнов с белыми цветами"),
    (12, "Лаундж с дивани в залата", "Lounge sofas in the hall", "Диваны в лаунж-зоне зала"),
    (13, "Маса на младоженците със сухи цветя", "Head table with dried flowers", "Стол молодожёнов с сухоцветами"),
    (14, "Украса на плажа пред ресторанта", "Beach decoration in front of the restaurant", "Украшения на пляже перед рестораном"),
    (15, "Кресла и маса в залата", "Armchairs and table in the hall", "Кресла и стол в зале"),
    (16, "Маса на младоженците с пастелни цветя", "Head table with pastel flowers", "Стол молодожёнов с пастельными цветами"),
    (17, "Подредена маса с плетени кресла", "Table set with wicker armchairs", "Сервированный стол с плетёными креслами"),
    (18, "Залата с дивани до прозорците", "The hall with sofas by the windows", "Зал с диванами у окон"),
]
GALLERY_SIZES = {}  # gevuld bij het bouwen

HEAD = """<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{description}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{description}">
<meta property="og:image" content="{base}{og_image}">
<meta property="og:type" content="website">
{alternates}
<link rel="icon" type="image/svg+xml" href="{base}img/favicon.svg">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Prata&family=Commissioner:wght@400;500;600&display=swap">
<link rel="stylesheet" href="{base}css/style.css?v={version}">
</head>
<body>
"""

HEADER = """
<header class="site-header">
  <div class="wrap header-inner">
    <a href="{home}" class="brand" aria-label="{home_aria}">
      <img src="{base}img/logo-600.png" alt="First Line Beach Restaurant &amp; Bar" width="600" height="189">
    </a>
    <nav class="main-nav" id="main-nav" aria-label="{nav_aria}">
      <ul>
{nav_items}
      </ul>
    </nav>
    <div class="header-actions">
      <nav class="lang-switch" aria-label="{lang_aria}">
{lang_items}
      </nav>
      <a class="header-phone" href="tel:+359886861001">{phone_label}</a>
      <a class="btn btn-small" href="{contact}#zapitvane">{inquiry}</a>
      <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="main-nav" aria-label="{menu}">
        <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 7h16M4 12h16M4 17h16"/></svg>
      </button>
    </div>
  </div>
</header>
"""

FOOTER = """
<footer class="site-footer">
  <div class="wrap footer-inner">
    <img src="{base}img/logo-600.png" alt="First Line Beach Restaurant &amp; Bar" width="600" height="189" class="footer-logo">
    <div class="footer-contact">
      <p>First Line Restaurant &amp; Bar</p>
      <p>{address}</p>
      <p><a href="tel:+359886861001">+359 88 686 1001</a></p>
      <p><a href="mailto:kranevo.firstline@gmail.com">kranevo.firstline@gmail.com</a></p>
    </div>
    <nav class="footer-nav" aria-label="{pages_aria}">
      <ul>
{footer_items}
      </ul>
    </nav>
    <div class="footer-contact">
      <p>{follow}</p>
      <p><a href="https://www.facebook.com/firstlinebar" rel="noopener">Facebook</a></p>
      <p><a href="https://www.instagram.com/first_line_restaurant_kranevo/" rel="noopener">Instagram</a></p>
    </div>
    <p class="credit">{site}: <a href="https://maxxmarketing.eu" rel="noopener">MaxxMarketing</a></p>
  </div>
</footer>

<script src="{base}js/main.js?v={version}"></script>
</body>
</html>
"""

GALLERY = """<!--
title: {gallery_title}
description: {gallery_desc}
og_image: img/galerij/03.jpg
-->
<main id="top">

  <section class="page-hero page-hero-simple">
    <div class="wrap">
      <h1>{gallery_h1}</h1>
      <p class="lead">{gallery_lead}</p>
    </div>
  </section>

  <section class="gallery">
    <div class="wrap">
      <div class="gallery-grid">
{items}
      </div>
    </div>
  </section>

  <dialog class="lightbox" aria-label="{photo}">
    <div class="lightbox-inner">
      <img src="" alt="">
      <button class="lb-btn lb-close" type="button" aria-label="{close}"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6 6l12 12M18 6L6 18"/></svg></button>
      <button class="lb-btn lb-prev" type="button" aria-label="{prev}"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M15 5l-7 7 7 7"/></svg></button>
      <button class="lb-btn lb-next" type="button" aria-label="{next}"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M9 5l7 7-7 7"/></svg></button>
    </div>
  </dialog>

</main>
"""


def image_size(path):
    """Breedte/hoogte uit een JPEG-header lezen (geen extra libraries nodig)."""
    data = path.read_bytes()
    i = 2
    while i < len(data):
        if data[i] != 0xFF:
            i += 1
            continue
        marker = data[i + 1]
        length = int.from_bytes(data[i + 2:i + 4], "big")
        if marker in (0xC0, 0xC1, 0xC2):
            h = int.from_bytes(data[i + 5:i + 7], "big")
            w = int.from_bytes(data[i + 7:i + 9], "big")
            return w, h
        i += 2 + length
    return 720, 540


def gallery_source(code):
    idx = {"bg": 1, "en": 2, "ru": 3}[code]
    lines = []
    for row in GALLERY_ALTS:
        n = row[0]
        w, h = image_size(ROOT / f"img/galerij/{n:02d}-k.jpg")
        lines.append(
            f'        <a href="{{{{base}}}}img/galerij/{n:02d}.jpg" data-lightbox>'
            f'<img src="{{{{base}}}}img/galerij/{n:02d}-k.jpg" alt="{row[idx]}" width="{w}" height="{h}" loading="lazy"></a>'
        )
    return GALLERY.format(items="\n".join(lines), **LANGS[code]["t"])


def meta(src):
    m = re.match(r"\s*<!--(.*?)-->", src, re.S)
    data = {}
    for line in m.group(1).strip().splitlines():
        key, _, value = line.partition(":")
        data[key.strip()] = value.strip()
    return data, src[m.end():]


def rel(from_code, to_code, key):
    """Relatief pad van een pagina in taal from_code naar pagina key in taal to_code."""
    up = "../" if LANGS[from_code]["dir"] else ""
    return up + LANGS[to_code]["dir"] + LANGS[to_code]["pages"][key]


def build():
    for code, L in LANGS.items():
        base = "../" if L["dir"] else ""
        outdir = ROOT / L["dir"]
        outdir.mkdir(exist_ok=True)
        for key in KEYS:
            if key == "gallery":
                src = gallery_source(code)
            else:
                src = (ROOT / "src" / code / f"{key}.html").read_text(encoding="utf-8")
            data, body = meta(src)
            body = body.replace("{{base}}", base)
            for k in KEYS:
                body = body.replace("{{" + k + "}}", L["pages"][k])

            nav_items = "\n".join(
                f'        <li><a href="{L["pages"][k]}"{" aria-current=\"page\"" if k == key else ""}>{L["nav"][k]}</a></li>'
                for k in KEYS
            )
            footer_items = "\n".join(f'        <li><a href="{L["pages"][k]}">{L["nav"][k]}</a></li>' for k in KEYS)
            lang_items = "\n".join(
                f'        <a href="{rel(code, c, key)}" hreflang="{c}" lang="{c}"'
                f'{" aria-current=\"true\"" if c == code else ""}>{LANGS[c]["label"]}</a>'
                for c in LANGS
            )
            alternates = "\n".join(
                f'<link rel="alternate" hreflang="{c}" href="{rel(code, c, key)}">' for c in LANGS
            )

            html = (
                HEAD.format(lang=code, base=base, version=VERSION, alternates=alternates, **data)
                + HEADER.format(base=base, nav_items=nav_items, lang_items=lang_items,
                                home=L["pages"]["home"], contact=L["pages"]["contact"], **L["t"])
                + body.strip("\n") + "\n"
                + FOOTER.format(base=base, footer_items=footer_items, version=VERSION, **L["t"])
            )
            out = outdir / L["pages"][key]
            out.write_text(html, encoding="utf-8")
            print("gebouwd:", out.relative_to(ROOT))


if __name__ == "__main__":
    build()
