"""Bouwt de pagina's van First Line.

Elke pagina staat in src/<naam>.html (alleen de <main>-inhoud, met bovenaan
een kopblok tussen <!-- ... -->). Dit script zet de gedeelde <head>, header en
footer eromheen en schrijft het resultaat naar de projectmap.

Gebruik:  python3 build.py
Na een wijziging aan css/js: VERSION ophogen, anders zien bezoekers de oude versie.
"""
import pathlib
import re

ROOT = pathlib.Path(__file__).parent
VERSION = "20261023c"

PHONE_HREF = "tel:+359886861001"
PHONE = "088 686 1001"
EMAIL = "kranevo.firstline@gmail.com"

NAV = [
    ("index.html", "Начало"),
    ("svatbi.html", "Сватби"),
    ("firmeni-tarzhestva.html", "Фирмени тържества"),
    ("galeria.html", "Галерия"),
    ("kontakt.html", "Контакт"),
]

HEAD = """<!doctype html>
<html lang="bg">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{description}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{description}">
<meta property="og:image" content="{og_image}">
<meta property="og:type" content="website">
<link rel="icon" type="image/svg+xml" href="img/favicon.svg">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Prata&family=Commissioner:wght@400;500;600&display=swap">
<link rel="stylesheet" href="css/style.css?v={version}">
</head>
<body>
"""

HEADER = """
<header class="site-header">
  <div class="wrap header-inner">
    <a href="index.html" class="brand" aria-label="First Line – начало">
      <img src="img/logo-600.png" alt="First Line Beach Restaurant &amp; Bar" width="600" height="189">
    </a>
    <nav class="main-nav" id="main-nav" aria-label="Основна навигация">
      <ul>
{nav_items}
      </ul>
    </nav>
    <div class="header-actions">
      <a class="header-phone" href="{phone_href}">{phone}</a>
      <a class="btn btn-small" href="kontakt.html#zapitvane">Запитване</a>
      <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="main-nav" aria-label="Меню">
        <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 7h16M4 12h16M4 17h16"/></svg>
      </button>
    </div>
  </div>
</header>
"""

FOOTER = """
<footer class="site-footer">
  <div class="wrap footer-inner">
    <img src="img/logo-600.png" alt="First Line Beach Restaurant &amp; Bar" width="600" height="189" class="footer-logo">
    <div class="footer-contact">
      <p>First Line Restaurant &amp; Bar</p>
      <p>Централен плаж, 9649 Кранево</p>
      <p><a href="{phone_href}">{phone}</a></p>
      <p><a href="mailto:{email}">{email}</a></p>
    </div>
    <nav class="footer-nav" aria-label="Страници">
      <ul>
{footer_items}
      </ul>
    </nav>
    <div>
      <p class="footer-contact">Следвайте ни</p>
      <p class="footer-contact"><a href="https://www.facebook.com/firstlinebar" rel="noopener">Facebook</a></p>
      <p class="footer-contact"><a href="https://www.instagram.com/first_line_restaurant_kranevo/" rel="noopener">Instagram</a></p>
    </div>
    <p class="credit">Уебсайт: <a href="https://maxxmarketing.eu" rel="noopener">MaxxMarketing</a></p>
  </div>
</footer>

<script src="js/main.js?v={version}"></script>
</body>
</html>
"""


def meta(src: str) -> tuple[dict, str]:
    m = re.match(r"\s*<!--(.*?)-->", src, re.S)
    data = {}
    for line in m.group(1).strip().splitlines():
        key, _, value = line.partition(":")
        data[key.strip()] = value.strip()
    return data, src[m.end():]


def build():
    for page in sorted((ROOT / "src").glob("*.html")):
        data, body = meta(page.read_text(encoding="utf-8"))
        name = page.name
        nav_items = "\n".join(
            f'        <li><a href="{href}"{" aria-current=\"page\"" if href == name else ""}>{label}</a></li>'
            for href, label in NAV
        )
        footer_items = "\n".join(
            f'        <li><a href="{href}">{label}</a></li>' for href, label in NAV
        )
        html = (
            HEAD.format(version=VERSION, **data)
            + HEADER.format(nav_items=nav_items, phone=PHONE, phone_href=PHONE_HREF)
            + body.strip("\n")
            + "\n"
            + FOOTER.format(footer_items=footer_items, phone=PHONE, phone_href=PHONE_HREF,
                            email=EMAIL, version=VERSION)
        )
        (ROOT / name).write_text(html, encoding="utf-8")
        print("gebouwd:", name)


if __name__ == "__main__":
    build()
