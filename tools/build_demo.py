"""Vygeneruje ukázkový e-shop pro chatbota na eshop-poradce.eu:
   public/ukazkovy-eshop/index.html, detail každého produktu a feed.xml (formát Shoptet XML exportu).
   Spuštění: python tools/build_demo.py   (po úpravě products.py)"""
import json, html, os
from xml.sax.saxutils import escape
from products import PRODUCTS

BASE = "https://eshop-poradce.eu/ukazkovy-eshop"
ROOT = os.path.join(os.path.dirname(__file__), "..", "public", "ukazkovy-eshop")
CATS = []
for p in PRODUCTS:
    if p["cat"] not in CATS: CATS.append(p["cat"])

def kc(n): return f"{n:,}".replace(",", " ") + " Kč"
def url(p): return f"{BASE}/{p['slug']}/"
def stock_text(p): return "Skladem" if p["stock"] > 0 else "Momentálně nedostupné"

STYLE = """
:root{--bg:#f7f4ee;--ink:#17302f;--ink2:#4d605e;--line:#e6dfd1;--teal:#0b7f7a;--ok:#1f9a5e;--no:#b5452f}
*{box-sizing:border-box}body{margin:0;font:16px/1.55 "Nunito Sans","Segoe UI",system-ui,sans-serif;background:var(--bg);color:var(--ink)}
a{color:inherit}img{max-width:100%;display:block}
.note{background:#14313a;color:#d9f1ec;font-size:14px;text-align:center;padding:9px 16px}
.note a{color:#fff;font-weight:700}
header{background:#fff;border-bottom:1px solid var(--line)}
header .in{max-width:1120px;margin:0 auto;padding:16px 20px;display:flex;justify-content:space-between;align-items:center;gap:16px;flex-wrap:wrap}
.logo{font-weight:800;font-size:21px;text-decoration:none;letter-spacing:-.01em}.logo span{color:var(--teal)}
nav{display:flex;gap:6px;flex-wrap:wrap}nav a{text-decoration:none;font-weight:700;color:var(--ink2);padding:6px 12px;border-radius:999px;font-size:15px}nav a:hover{background:#eef5f3;color:var(--teal)}
main{max-width:1120px;margin:0 auto;padding:28px 20px 90px}
h1{font-size:clamp(26px,4vw,38px);margin:0 0 6px;letter-spacing:-.02em;line-height:1.15}
.sub{color:var(--ink2);margin:0 0 26px}
h2{font-size:22px;margin:34px 0 14px}
.grid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:18px}
.card{background:#fff;border:1px solid var(--line);border-radius:18px;overflow:hidden;text-decoration:none;display:flex;flex-direction:column;transition:box-shadow .15s}
.card:hover{box-shadow:0 10px 24px rgba(23,48,47,.1)}
.card img{aspect-ratio:1;width:100%;object-fit:cover}
.card .b{padding:12px 14px 16px;display:flex;flex-direction:column;gap:4px;flex:1}
.card b{font-size:16px;line-height:1.3}
.price{font-weight:800;color:var(--teal);font-size:18px}.price s{color:#8a9896;font-weight:600;font-size:14px;margin-left:6px}
.st{font-size:14px;font-weight:700;color:var(--ok)}.st.no{color:var(--no)}
.crumbs{font-size:14px;color:var(--ink2);margin-bottom:18px}.crumbs a{text-decoration:none;font-weight:700}
.detail{display:grid;grid-template-columns:1fr 1fr;gap:36px;align-items:start}
.detail img{border-radius:22px;border:1px solid var(--line);aspect-ratio:1;width:100%;object-fit:cover}
.detail .price{font-size:30px;margin:14px 0 4px}
.buy{margin-top:18px;display:inline-block;padding:14px 22px;border-radius:12px;background:#d9e3e1;color:#4d605e;font-weight:800;cursor:not-allowed;border:0;font:inherit;font-weight:800}
table{border-collapse:collapse;margin-top:20px;width:100%;max-width:420px}td{padding:8px 0;border-top:1px solid var(--line)}td:first-child{color:var(--ink2);width:45%}
footer{border-top:1px solid var(--line);color:var(--ink2);font-size:14px;text-align:center;padding:24px 16px 90px}
@media(max-width:860px){.grid{grid-template-columns:repeat(2,minmax(0,1fr));gap:12px}.detail{grid-template-columns:1fr;gap:20px}}
@media(max-width:420px){main{padding:20px 14px 90px}.card .b{padding:10px 11px 14px}.card b{font-size:15px}}
"""

def page(title, desc, body, extra_head=""):
    nav = "".join(f'<a href="/ukazkovy-eshop/#{c.lower().replace(" ", "-")}">{html.escape(c)}</a>' for c in CATS)
    return f"""<!doctype html>
<html lang="cs"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title><meta name="description" content="{html.escape(desc)}"><meta name="robots" content="noindex">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link href="/fonts/fonts.css" rel="stylesheet">
<style>{STYLE}</style>{extra_head}</head><body>
<div class="note">Tohle je <b>ukázkový e-shop</b> pro vyzkoušení chatbota. Nic se tu neprodává. <a href="/">Zpět na E-shop poradce</a></div>
<header><div class="in"><a class="logo" href="/ukazkovy-eshop/">Ukázkový <span>e-shop</span></a><nav aria-label="Kategorie">{nav}</nav></div></header>
<main>{body}</main>
<footer>Ukázkový e-shop · produkty jsou vymyšlené · <a href="/chat-gdpr.html" target="_blank" rel="noopener">Ochrana osobních údajů</a> · <a href="#" data-cookie-settings>Nastavení cookies</a></footer>
<script src="/demo-chat.js" defer></script>
<script src="/consent.js" defer></script>
</body></html>
"""

def card(p):
    std = f"<s>{kc(p['std'])}</s>" if p["std"] else ""
    st = f'<span class="st{"" if p["stock"] > 0 else " no"}">{stock_text(p)}</span>'
    return (f'<a class="card" href="/ukazkovy-eshop/{p["slug"]}/"><img src="/ukazkovy-eshop/img/{p["img"]}.jpg" alt="" loading="lazy" width="600" height="600">'
            f'<div class="b"><b>{html.escape(p["name"])}</b><span class="price">{kc(p["price"])}{std}</span>{st}</div></a>')

def build():
    os.makedirs(ROOT, exist_ok=True)
    sections = ""
    for c in CATS:
        items = "".join(card(p) for p in PRODUCTS if p["cat"] == c)
        sections += f'<h2 id="{c.lower().replace(" ", "-")}">{html.escape(c)}</h2><div class="grid">{items}</div>'
    body = ('<h1>Chutě Středomoří</h1><p class="sub">Olivový olej, med, olivy a dárky. Zkuste se zeptat chatbota vpravo dole, třeba „hledám dárek pro mámu do 500 Kč“.</p>'
            + sections)
    open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8").write(page("Ukázkový e-shop | Chutě Středomoří", "Ukázkový e-shop pro vyzkoušení AI nákupního asistenta.", body))

    for p in PRODUCTS:
        avail = "https://schema.org/InStock" if p["stock"] > 0 else "https://schema.org/OutOfStock"
        ld = {"@context": "https://schema.org", "@type": "Product", "name": p["name"], "sku": p["id"],
              "image": f"{BASE}/img/{p['img']}.jpg", "description": p["desc"], "brand": {"@type": "Brand", "name": p["maker"]},
              "offers": {"@type": "Offer", "url": url(p), "priceCurrency": "CZK", "price": p["price"], "availability": avail}}
        rows = "".join(f"<tr><td>{html.escape(k)}</td><td>{html.escape(v)}</td></tr>" for k, v in p["params"].items())
        std = f"<s>{kc(p['std'])}</s>" if p["std"] else ""
        body = (f'<div class="crumbs"><a href="/ukazkovy-eshop/">Ukázkový e-shop</a> › <a href="/ukazkovy-eshop/#{p["cat"].lower().replace(" ", "-")}">{html.escape(p["cat"])}</a></div>'
                f'<div class="detail"><img src="/ukazkovy-eshop/img/{p["img"]}.jpg" alt="{html.escape(p["name"])}" width="600" height="600">'
                f'<div><h1>{html.escape(p["name"])}</h1><p class="sub" style="margin:0">{html.escape(p["short"])}</p>'
                f'<div class="price">{kc(p["price"])}{std}</div><div class="st{"" if p["stock"] > 0 else " no"}">{stock_text(p)}</div>'
                f'<button class="buy" type="button" disabled>Ukázka, nelze koupit</button>'
                f'<p>{html.escape(p["desc"])}</p><table>{rows}<tr><td>Výrobce</td><td>{html.escape(p["maker"])}</td></tr></table></div></div>')
        d = os.path.join(ROOT, p["slug"]); os.makedirs(d, exist_ok=True)
        head = f'<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script><link rel="canonical" href="{url(p)}">'
        open(os.path.join(d, "index.html"), "w", encoding="utf-8").write(page(f"{p['name']} | Ukázkový e-shop", p["short"], body, head))

    items = []
    for p in PRODUCTS:
        params = "".join(f"<PARAMETER><NAME>{escape(k)}</NAME><VALUE>{escape(v)}</VALUE></PARAMETER>" for k, v in p["params"].items())
        std = f"<STANDARD_PRICE>{p['std']}</STANDARD_PRICE>" if p["std"] else ""
        items.append(f"""  <SHOPITEM id="{p['id']}">
    <NAME>{escape(p['name'])}</NAME>
    <SHORT_DESCRIPTION>{escape(p['short'])}</SHORT_DESCRIPTION>
    <DESCRIPTION>{escape(p['desc'])}</DESCRIPTION>
    <MANUFACTURER>{escape(p['maker'])}</MANUFACTURER>
    <ORIG_URL>{url(p)}</ORIG_URL>
    <IMAGES><IMAGE>{BASE}/img/{p['img']}.jpg</IMAGE></IMAGES>
    <CATEGORIES><CATEGORY>{escape(p['cat'])}</CATEGORY><DEFAULT_CATEGORY>{escape(p['cat'])}</DEFAULT_CATEGORY></CATEGORIES>
    <CODE>DEMO-{p['id']}</CODE>
    <CURRENCY>CZK</CURRENCY>
    <PRICE_VAT>{p['price']}</PRICE_VAT>{std}
    <STOCK><AMOUNT>{p['stock']}</AMOUNT></STOCK>
    <AVAILABILITY_IN_STOCK>Skladem</AVAILABILITY_IN_STOCK>
    <AVAILABILITY_OUT_OF_STOCK>Momentálně nedostupné</AVAILABILITY_OUT_OF_STOCK>
    <VISIBILITY>visible</VISIBILITY>
    <PARAMETERS>{params}</PARAMETERS>
  </SHOPITEM>""")
    xml = '<?xml version="1.0" encoding="utf-8"?>\n<!-- Ukázkový e-shop pro chatbota na eshop-poradce.eu (vymyšlené produkty). -->\n<SHOP>\n' + "\n".join(items) + "\n</SHOP>\n"
    open(os.path.join(ROOT, "feed.xml"), "w", encoding="utf-8").write(xml)
    print(f"Hotovo: {len(PRODUCTS)} produktů, {len(CATS)} kategorií.")

if __name__ == "__main__":
    build()
