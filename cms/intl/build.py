#!/usr/bin/env python3
"""Pembangun halaman internasional indonesiayanwoo.com: /en/ (Inggris) dan /zh/ (Mandarin sederhana).

    python3 cms/intl/build.py            # tulis ulang semua halaman + sitemap + hreflang halaman Indonesia
    python3 cms/intl/build.py --check    # hanya periksa: tidak menulis apa pun

Kenapa generator, bukan 16 berkas HTML yang disunting tangan: header, footer, hreflang dan
harga harus sama di kedua bahasa. Isi halaman ada di `pages.py`; fakta perusahaan, harga dan
sertifikat ada di SITE / PRICES di bawah — ubah di sini, jalankan ulang, commit hasilnya.

Gambar di assets/intl/img/ dibuat sekali dari aset Figma "WEBSITE NESTSENSIALS" (potongan produk,
box hadiah, sachet) dan wp-content/uploads/2023/03 (foto proses, tim, rumah walet), disimpan JPEG.

Halaman sengaja TIDAK memuat apa pun dari domain lain (font Google, GTM, piksel iklan):
semua itu lambat atau diblokir di Tiongkok daratan. `--check` menolak kalau ada yang terselip.
"""
import html
import json
import os
import re
import sys
from datetime import date

sys.dont_write_bytecode = True  # jangan tinggalkan __pycache__ di repo situs statis

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
ORIGIN = "https://indonesiayanwoo.com"
CSS_VER = "20261111c"

# ── Fakta perusahaan ────────────────────────────────────────────────────────
# Yang kosong tidak ditampilkan. JANGAN mengisi sertifikat/nomor yang belum dipegang:
# halaman ini dibaca calon importir, dan klaim sertifikat yang keliru jauh lebih mahal
# daripada blok yang belum tampil.
SITE = {
    "brand": "Indonesia Yanwoo",
    "pack_brand": "Nestsensials",
    "company": "PT Lentera Alam Nusantara",
    "wa": "6287725260196",
    "phone": "+62 877-2526-0196",
    "email": "sales@markaswalet.com",
    "street": "Jl. Gubeng Kertajaya V D No. 20, Airlangga, Gubeng",
    "city": "Surabaya",
    "postal": "60286",
    "instagram": "nestsensials_official",
    "wechat_id": "",        # isi ID WeChat → tombol & blok WeChat muncul di semua halaman
    "wechat_qr": "",        # path gambar QR, mis. "/assets/intl/img/wechat-qr.png"
    "baidu_verify": "",     # kode verifikasi Baidu 站长平台 (meta baidu-site-verification)
    "google_verify": "",
    # Sertifikat yang SUDAH dipegang, mis.
    # {"en": "NKV (Veterinary Control Number)", "zh": "NKV 兽医监管编号", "no": "…", "holder": "…"}
    "certs": [],
}

# Harga eceran per kemasan dalam Rupiah (sumber: desain situs Nestsensials, Nov 2026).
# None = "tanyakan harga hari ini".
PRICES = {"bowl": 1400000, "corner": 1300000, "strips": 1100000, "cake": 825000, "sachet": 360000}
PRICE_DATE = {"en": "November 2026", "zh": "2026年11月"}
RULES_CHECKED = {"en": "November 2026", "zh": "2026年11月"}

LANGS = {"en": "en", "zh": "zh-CN"}
HREFLANG = {"en": "en", "zh": "zh-Hans"}

# slug, label Inggris, label Mandarin
NAV = [
    ("products", "Products", "产品与价格"),
    ("process", "Process & quality", "加工与品质"),
    ("visitors", "Visiting Indonesia", "来印尼买燕窝"),
    ("bring-home", "Taking it home", "能带回国吗"),
    ("about", "About", "关于我们"),
    ("faq", "FAQ", "常见问题"),
    ("contact", "Contact", "联系我们"),
]
SLUGS = [""] + [n[0] for n in NAV]
# Padanan halaman Indonesia (untuk hreflang="id")
ID_ALT = {"": "/", "products": "/produk/", "about": "/tentang/", "contact": "/tentang/kontak/"}


def esc(s):
    return html.escape(str(s), quote=True)


def url(lang, slug=""):
    return f"/{lang}/{slug}/" if slug else f"/{lang}/"


def img(name):
    return f"/assets/intl/img/{name}"


def wa_link(lang, text=None):
    from urllib.parse import quote
    if text is None:
        text = ("Hello Indonesia Yanwoo, I would like to ask about your bird's nest."
                if lang == "en" else
                "您好 Indonesia Yanwoo，我想咨询燕窝。(Hello, I am writing from your Chinese page.)")
    return f"https://wa.me/{SITE['wa']}?text={quote(text)}"


def rupiah(n, lang):
    if n is None:
        return "Ask for today's price" if lang == "en" else "请咨询当日价格"
    s = f"{n:,}"
    return f"IDR {s}" if lang == "en" else f"{s} 印尼盾"


def ld(obj):
    """JSON-LD yang aman ditanam di HTML ('<' di-escape supaya tidak bisa menutup <script>)."""
    return '<script type="application/ld+json">' + json.dumps(obj, ensure_ascii=False).replace("<", "\\u003c") + "</script>"


def org_ld():
    return {
        "@context": "https://schema.org", "@type": "Organization",
        "name": SITE["brand"], "legalName": SITE["company"], "url": ORIGIN + "/en/",
        "logo": ORIGIN + img("logo.png"), "email": SITE["email"], "telephone": SITE["phone"],
        "address": {"@type": "PostalAddress", "streetAddress": SITE["street"], "addressLocality": SITE["city"],
                    "addressRegion": "Jawa Timur", "postalCode": SITE["postal"], "addressCountry": "ID"},
    }


def crumbs_ld(lang, slug, label):
    home = "Home" if lang == "en" else "首页"
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": home, "item": ORIGIN + url(lang)},
        {"@type": "ListItem", "position": 2, "name": label, "item": ORIGIN + url(lang, slug)},
    ]}


def layout(lang, slug, p):
    """p = dict(title, desc, body, [keywords], [jsonld], [og_image])."""
    t = (lambda en, zh: en if lang == "en" else zh)
    other = "zh" if lang == "en" else "en"
    canonical = ORIGIN + url(lang, slug)
    alts = [f'<link rel="alternate" hreflang="{HREFLANG[l]}" href="{ORIGIN}{url(l, slug)}">' for l in LANGS]
    if slug in ID_ALT:
        alts.append(f'<link rel="alternate" hreflang="id" href="{ORIGIN}{ID_ALT[slug]}">')
    alts.append(f'<link rel="alternate" hreflang="x-default" href="{ORIGIN}{url("en", slug)}">')
    og_image = ORIGIN + img(p.get("og_image", "og.jpg"))
    head_extra = []
    if lang == "zh":
        # Baidu: jangan transcoding halaman, dan halaman ini sama untuk PC maupun HP.
        head_extra += ['<meta name="applicable-device" content="pc,mobile">',
                       '<meta http-equiv="Cache-Control" content="no-transform">',
                       '<meta http-equiv="Cache-Control" content="no-siteapp">']
        if p.get("keywords"):
            head_extra.append(f'<meta name="keywords" content="{esc(p["keywords"])}">')
        if SITE["baidu_verify"]:
            head_extra.append(f'<meta name="baidu-site-verification" content="{esc(SITE["baidu_verify"])}">')
    if SITE["google_verify"]:
        head_extra.append(f'<meta name="google-site-verification" content="{esc(SITE["google_verify"])}">')
    jsonld = [org_ld()] + list(p.get("jsonld", []))

    cur_page, cur_lang = ' aria-current="page"', ' aria-current="true"'
    nav = "".join(
        '<a href="%s"%s>%s</a>' % (url(lang, s), cur_page if s == slug else "", esc(en if lang == "en" else zh))
        for s, en, zh in NAV)
    lang_sw = (
        '<a href="%s" hreflang="en"%s>EN</a>' % (url("en", slug), cur_lang if lang == "en" else "")
        + '<a href="%s" hreflang="zh-Hans"%s>中文</a>' % (url("zh", slug), cur_lang if lang == "zh" else "")
        + '<a href="%s" hreflang="id">ID</a>' % ID_ALT.get(slug, "/"))
    wx_float = (f'<a class="wx" href="{url(lang, "contact")}#wechat">{t("WeChat", "微信")}: {esc(SITE["wechat_id"])}</a>'
                if SITE["wechat_id"] else "")
    foot_links = "".join(f'<li><a href="{url(lang, s)}">{esc(en if lang == "en" else zh)}</a></li>' for s, en, zh in NAV)
    wechat_li = f'<li>{t("WeChat", "微信")}: {esc(SITE["wechat_id"])}</li>' if SITE["wechat_id"] else ""

    return f"""<!doctype html>
<html lang="{LANGS[lang]}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(p["title"])}</title>
<meta name="description" content="{esc(p["desc"])}">
<link rel="canonical" href="{canonical}">
{chr(10).join(alts)}
{chr(10).join(head_extra)}
<meta property="og:type" content="website">
<meta property="og:site_name" content="{esc(SITE["brand"])}">
<meta property="og:locale" content="{t("en_US", "zh_CN")}">
<meta property="og:title" content="{esc(p["title"])}">
<meta property="og:description" content="{esc(p["desc"])}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{og_image}">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" type="image/png" sizes="32x32" href="/wp-content/uploads/2023/03/cropped-LOGO-INDONESIA-YANWOO-HITAM-FAVICON-Copy-32x32.png">
<link rel="apple-touch-icon" href="/wp-content/uploads/2023/03/cropped-LOGO-INDONESIA-YANWOO-HITAM-FAVICON-Copy-180x180.png">
<link rel="stylesheet" href="/assets/intl/site.css?v={CSS_VER}">
{chr(10).join(ld(j) for j in jsonld)}
</head>
<body>
<a class="skip" href="#main">{t("Skip to content", "跳到正文")}</a>
<header class="site-head">
  <div class="wrap head-row">
    <a class="logo" href="{url(lang)}">
      <img src="{img("logo.png")}" width="44" height="44" alt="{esc(SITE["brand"])}">
      <span><b>Indonesia Yanwoo</b><small>{t("Edible bird's nest · 印尼燕窝", "印尼燕窝 · 产地直供")}</small></span>
    </a>
    <nav class="nav" aria-label="{t("Main", "主导航")}">{nav}</nav>
    <div class="lang" aria-label="{t("Language", "语言")}">{lang_sw}</div>
  </div>
</header>
<main id="main">
{p["body"]}
</main>
<footer class="site-foot">
  <div class="wrap">
    <div class="foot-grid">
      <div>
        <h3>Indonesia Yanwoo</h3>
        <p>{t("Cleaned edible bird's nest from Markaswalet partner farmers in Kalimantan, Indonesia, packed under the Nestsensials brand.",
              "来自印尼加里曼丹 Markaswalet 合作燕农的洁净燕窝，以 Nestsensials 品牌包装。")}</p>
        <p>{esc(SITE["company"])}<br>{esc(SITE["street"])}<br>{esc(SITE["city"])} {esc(SITE["postal"])}, {t("East Java, Indonesia", "印度尼西亚 东爪哇省")}</p>
      </div>
      <div>
        <h3>{t("Pages", "页面")}</h3>
        <ul>{foot_links}</ul>
      </div>
      <div>
        <h3>{t("Contact", "联系方式")}</h3>
        <ul>
          <li>WhatsApp: <a href="{wa_link(lang)}" rel="noopener">{esc(SITE["phone"])}</a></li>
          {wechat_li}
          <li><a href="mailto:{esc(SITE["email"])}">{esc(SITE["email"])}</a></li>
          <li><a href="{ID_ALT.get(slug, "/")}" hreflang="id">Bahasa Indonesia</a> · <a href="{url(other, slug)}">{t("中文", "English")}</a></li>
        </ul>
      </div>
    </div>
    <div class="foot-base">© {date.today().year} {esc(SITE["brand"])} · {esc(SITE["company"])}</div>
  </div>
</footer>
<div class="float">{wx_float}<a href="{wa_link(lang)}" rel="noopener">WhatsApp</a></div>
</body>
</html>
"""


# ── Pemeriksaan ─────────────────────────────────────────────────────────────
_EXT = re.compile(r'<(?:script|link|img|iframe|source|video|audio)\b[^>]*?\b(?:src|href)="(https?:)?//([^"/]+)', re.I)


def check_page(path, text):
    """Kembalikan daftar masalah. Sumber daya dari domain lain = masalah (lihat docstring)."""
    out = []
    for m in _EXT.finditer(text):
        tag = m.group(0)
        host = m.group(2)
        if host == "indonesiayanwoo.com":
            continue
        if tag.lower().startswith("<link") and ('rel="alternate"' in tag or 'rel="canonical"' in tag):
            continue
        out.append(f"{path}: memuat sumber daya dari {host}")
    for m in re.finditer(r'(?:src|href)="(/assets/intl/[^"?#]+)', text):
        if not os.path.exists(os.path.join(ROOT, m.group(1).lstrip("/"))):
            out.append(f"{path}: berkas tidak ada {m.group(1)}")
    for m in re.finditer(r'href="(/(?:en|zh)/[^"#?]*)', text):
        target = os.path.join(ROOT, m.group(1).strip("/"), "index.html")
        if not os.path.exists(target) and m.group(1).strip("/").split("/", 1)[-1] not in SLUGS and m.group(1).strip("/") not in ("en", "zh"):
            out.append(f"{path}: tautan internal mati {m.group(1)}")
    if text.count("<h1") != 1:
        out.append(f"{path}: jumlah <h1> = {text.count('<h1')}")
    return out


# ── Sitemap & halaman Indonesia ─────────────────────────────────────────────
def update_sitemap(today, write=True):
    """Tambahkan/perbarui URL /en/ dan /zh/ di page-sitemap.xml, naikkan lastmod-nya di index."""
    p = os.path.join(ROOT, "page-sitemap.xml")
    xml = open(p, encoding="utf-8").read()
    changed = 0
    for lang in LANGS:
        for slug in SLUGS:
            loc = ORIGIN + url(lang, slug)
            block = f"  <url>\n    <loc>{loc}</loc>\n    <lastmod>{today}</lastmod>\n  </url>\n"
            pat = re.compile(r"  <url>\s*<loc>" + re.escape(loc) + r"</loc>.*?</url>\n", re.S)
            if pat.search(xml):
                new = pat.sub(block, xml)
            else:
                new = xml.replace("</urlset>", block + "</urlset>")
            changed += new != xml
            xml = new
    if write:
        open(p, "w", encoding="utf-8").write(xml)
        ip = os.path.join(ROOT, "sitemap_index.xml")
        idx = open(ip, encoding="utf-8").read()
        idx = re.sub(r"(<loc>" + re.escape(ORIGIN) + r"/page-sitemap\.xml</loc>\s*<lastmod>)[^<]*", r"\g<1>" + today, idx)
        open(ip, "w", encoding="utf-8").write(idx)
    return changed


_MARK_A, _MARK_B = "<!-- intl:hreflang -->", "<!-- /intl:hreflang -->"
_PILL_A, _PILL_B = "<!-- intl:lang -->", "<!-- /intl:lang -->"


def patch_id_page(slug, write=True):
    """Pasang hreflang timbal balik + tautan bahasa di halaman Indonesia padanannya (idempoten)."""
    rel = ID_ALT[slug].strip("/")
    path = os.path.join(ROOT, rel, "index.html") if rel else os.path.join(ROOT, "index.html")
    s = open(path, encoding="utf-8").read()
    orig = s
    tags = "".join(
        [f'<link rel="alternate" hreflang="id" href="{ORIGIN}{ID_ALT[slug]}" />'] +
        [f'<link rel="alternate" hreflang="{HREFLANG[l]}" href="{ORIGIN}{url(l, slug)}" />' for l in LANGS] +
        [f'<link rel="alternate" hreflang="x-default" href="{ORIGIN}{url("en", slug)}" />'])
    block = f"{_MARK_A}{tags}{_MARK_B}"
    if _MARK_A in s:
        s = re.sub(re.escape(_MARK_A) + ".*?" + re.escape(_MARK_B), lambda _: block, s, flags=re.S)
    else:
        s, n = re.subn(r'(<link rel="canonical" href="[^"]*" ?/?>)', lambda m: m.group(1) + "\n    " + block, s, count=1)
        if not n:
            raise SystemExit(f"canonical tidak ditemukan di {path}")
    pill = (f'{_PILL_A}<div style="position:fixed;left:14px;bottom:14px;z-index:9999;background:#fff;border:1px solid #ddd;'
            f'border-radius:999px;padding:7px 14px;font:600 13px/1.2 system-ui,sans-serif;box-shadow:0 4px 14px rgba(0,0,0,.15)">'
            f'<a href="{url("en", slug)}" hreflang="en" style="color:#0b6b57;text-decoration:none">English</a>'
            f'<span style="color:#bbb"> · </span>'
            f'<a href="{url("zh", slug)}" hreflang="zh-Hans" style="color:#0b6b57;text-decoration:none">中文</a></div>{_PILL_B}')
    if _PILL_A in s:
        s = re.sub(re.escape(_PILL_A) + ".*?" + re.escape(_PILL_B), lambda _: pill, s, flags=re.S)
    else:
        i = s.rfind("</body>")
        if i < 0:
            raise SystemExit(f"</body> tidak ditemukan di {path}")
        s = s[:i] + pill + "\n" + s[i:]
    # Halaman ini berbahasa Indonesia; ekspor WordPress menandainya en-US.
    s = s.replace('<html lang="en-US"', '<html lang="id"', 1)
    if write and s != orig:
        open(path, "w", encoding="utf-8").write(s)
    return s != orig


def main():
    check_only = "--check" in sys.argv
    sys.path.insert(0, os.path.dirname(__file__))
    import pages  # noqa: E402

    problems, written = [], 0
    for lang in LANGS:
        for slug in SLUGS:
            p = pages.PAGES[slug](lang)
            text = layout(lang, slug, p)
            rel = os.path.join(lang, slug, "index.html") if slug else os.path.join(lang, "index.html")
            path = os.path.join(ROOT, rel)
            if not check_only:
                os.makedirs(os.path.dirname(path), exist_ok=True)
                old = open(path, encoding="utf-8").read() if os.path.exists(path) else None
                if old != text:
                    open(path, "w", encoding="utf-8").write(text)
                    written += 1
            problems += check_page(rel, text)
            if len(p["title"]) > 70 and lang == "en":
                problems.append(f"{rel}: judul {len(p['title'])} karakter (> 70)")
            if not (50 <= len(p["desc"]) <= (170 if lang == "en" else 100)):
                problems.append(f"{rel}: deskripsi {len(p['desc'])} karakter")
    today = date.today().isoformat()
    if not check_only:
        # lastmod hanya dinaikkan kalau ada halaman yang benar-benar berubah
        if written:
            update_sitemap(today)
        patched = sum(patch_id_page(s) for s in ID_ALT)
        print(f"{written} halaman ditulis, {patched} halaman Indonesia diperbarui")
    for x in problems:
        print("MASALAH:", x)
    print("OK" if not problems else f"{len(problems)} masalah")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
