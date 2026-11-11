"""Isi halaman internasional indonesiayanwoo.com (Inggris + Mandarin sederhana).

Tata letak, fakta perusahaan dan harga ada di build.py; berkas ini hanya teks.
Aturan isi:
  * Tidak ada klaim yang tidak bisa dibuktikan pemilik: tidak ada sertifikat (lihat SITE["certs"]),
    tidak ada klaim kesehatan, tidak ada jatah bawaan penumpang selain yang bersumber resmi.
  * Halaman "bring-home" memuat aturan bea cukai per negara + sumbernya. Kalau aturannya berubah,
    ubah teks DAN RULES_CHECKED di build.py.
  * Teks Inggris memakai apostrof tipografis (’) supaya string Python tidak perlu di-escape.
"""
import re

from build import SITE, PRICES, PRICE_DATE, RULES_CHECKED, url, img, wa_link, rupiah, crumbs_ld, esc

NAV_LABEL = {
    "products": ("Products", "产品与价格"), "process": ("Process & quality", "加工与品质"),
    "visitors": ("Visiting Indonesia", "来印尼买燕窝"), "bring-home": ("Taking it home", "能带回国吗"),
    "about": ("About", "关于我们"), "faq": ("FAQ", "常见问题"), "contact": ("Contact", "联系我们"),
}


def label(lang, slug):
    return NAV_LABEL[slug][0 if lang == "en" else 1]


def head(lang, slug, h1, lead):
    home = "Home" if lang == "en" else "首页"
    return (f'<div class="page-head"><div class="wrap"><div class="crumbs"><a href="{url(lang)}">{home}</a> / '
            f'{esc(label(lang, slug))}</div><h1>{h1}</h1><p>{lead}</p></div></div>')


def ext(href, text):
    return f'<a href="{href}" rel="nofollow noopener" target="_blank">{text}</a>'


def strip_tags(s):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", s)).strip()


def faq_ld(items):
    return {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": strip_tags(q), "acceptedAnswer": {"@type": "Answer", "text": strip_tags(a)}}
        for q, a in items]}


def qa_html(items):
    return "".join(f'<details class="qa"><summary>{q}</summary><div class="a">{a}</div></details>' for q, a in items)


def certs_block(lang):
    """Hanya tampil kalau SITE['certs'] diisi (sertifikat yang benar-benar dipegang)."""
    if not SITE["certs"]:
        return ""
    title = "Certificates" if lang == "en" else "资质证书"
    rows = "".join(
        f'<div><b>{esc(c[lang])}</b><span>{esc(c.get("no", ""))}'
        f'{(" · " + esc(c["holder"])) if c.get("holder") else ""}</span></div>' for c in SITE["certs"])
    return f'<h2>{title}</h2><div class="certs">{rows}</div>'


# ── Produk ──────────────────────────────────────────────────────────────────
PACK50 = {"en": "50 g", "zh": "50 克（一两）"}
GRADES = [
    {"key": "bowl", "img": "grade-bowl.jpg", "id": "Sarang Utuh Mangkok", "pack": PACK50,
     "en": {"name": "Whole Bowl", "alt": "燕盏 · Sarang Utuh Mangkok", "form": "Whole, tidy bowl",
            "desc": "Whole bowl-shaped nests with dense, tidy strands, the best pieces sorted from each harvest. Springy once cooked and handsome on the table.",
            "short": "Whole bowls, the best pieces of each harvest.", "for": "Gifts and special occasions"},
     "zh": {"name": "燕盏", "alt": "Whole Bowl · Sarang Utuh Mangkok", "form": "完整盏形",
            "desc": "完整盏形，燕丝紧密整齐，是每次采收中分拣出的上品。炖煮后口感爽滑有弹性，上桌也好看。",
            "short": "完整盏形，每次采收中的上品。", "for": "送礼、宴客"}},
    {"key": "corner", "img": "grade-corner.jpg", "id": "Sarang Sudut", "pack": PACK50,
     "en": {"name": "Corner Pieces", "alt": "燕角 · Sarang Sudut", "form": "Pieces from the corners of the nest",
            "desc": "Pieces from the corners of the nest, with dense strands. A good choice for regular use.",
            "short": "Corner pieces with dense strands.", "for": "Regular use"},
     "zh": {"name": "燕角", "alt": "Corner Pieces · Sarang Sudut", "form": "燕窝的角位",
            "desc": "取自燕窝的角位，燕丝密实，适合经常食用。",
            "short": "取自角位，燕丝密实。", "for": "经常食用"}},
    {"key": "strips", "img": "grade-strips.jpg", "id": "Sarang Patahan", "pack": PACK50,
     "en": {"name": "Strips", "alt": "燕条 · Sarang Patahan", "form": "Broken pieces, large and small",
            "desc": "Clean broken pieces, large and small. The practical choice for the whole family, day to day.",
            "short": "Clean broken pieces for the family.", "for": "Everyday family use"},
     "zh": {"name": "燕条", "alt": "Strips · Sarang Patahan", "form": "大小碎盏，呈条状",
            "desc": "洁净的大小碎盏，呈条状，适合全家日常享用。",
            "short": "洁净碎盏，全家日常享用。", "for": "全家日常食用"}},
    {"key": "cake", "img": "grade-cake.jpg", "id": "Hancuran (Yenping)", "pack": PACK50,
     "en": {"name": "Nest Cake", "alt": "燕饼 · Hancuran (Yenping)", "form": "Fine pieces pressed flat",
            "desc": "Fine pieces of clean nest, pressed flat. The most economical form, made for cooking every day.",
            "short": "Fine pieces, the most economical.", "for": "Most economical, daily cooking"},
     "zh": {"name": "燕饼", "alt": "Nest Cake · Hancuran (Yenping)", "form": "细碎燕丝压成饼状",
            "desc": "细碎的洁净燕丝压成饼状，最实惠，适合天天炖煮。",
            "short": "细碎燕丝成饼，最实惠。", "for": "最实惠，天天炖煮"}},
    {"key": "sachet", "img": "pack-sachet.jpg", "id": "Nestsensials Sachet",
     "pack": {"en": "5 sachets × 5 g", "zh": "5 袋 × 5 克"},
     "en": {"name": "Sachet Pack", "alt": "小袋装 · Nestsensials Sachet", "form": "Five single-use sachets",
            "desc": "One sachet is one cooking. A good way to try bird’s nest for the first time, and easy to carry.",
            "short": "One sachet, one cooking. Easy to carry.", "for": "First try, travelling"},
     "zh": {"name": "便携小袋装", "alt": "Sachet Pack · Nestsensials Sachet", "form": "5 小袋，每袋一次用量",
            "desc": "一袋正好炖一次，适合第一次尝试，也方便随身携带。",
            "short": "一袋炖一次，方便携带。", "for": "初次尝试、旅途携带"}},
]


def price_line(lang, g):
    return f'{rupiah(PRICES.get(g["key"]), lang)} <small>/ {g["pack"][lang]}</small>'


def card(lang, g):
    n = g[lang]
    return (f'<a class="card" href="{url(lang, "products")}#{g["key"]}" style="text-decoration:none;color:inherit">'
            f'<img src="{img(g["img"])}" width="800" height="800" loading="lazy" alt="{esc(n["name"])}">'
            f'<div class="pad"><h3>{esc(n["name"])}</h3><div class="tagline">{esc(n["alt"].split(" · ")[0])}</div>'
            f'<p>{esc(n["short"])}</p><div class="price">{price_line(lang, g)}</div></div></a>')


STEPS = {
    "en": [("Harvested", "Nests are collected from the swiftlet houses of partner farmers in Kalimantan."),
           ("Sorted", "Graded by shape and size: bowl, corner, strips and fine pieces."),
           ("Cleaned", "Feathers and dirt are lifted out one by one, by hand, with no bleach or chemicals."),
           ("Packed", "Quality-checked, weighed and packed neatly.")],
    "zh": [("采收", "从加里曼丹合作燕农的燕屋采下燕窝。"),
           ("分拣", "按形态和大小分为燕盏、燕角、燕条和细碎燕丝。"),
           ("清洁", "人工一根一根挑去羽毛和杂质，不用漂白剂和化学品。"),
           ("包装", "检验品质、称重，整齐包装。")],
}


def steps_html(lang, cols=True):
    li = "".join(f"<li><b>{a}</b><span>{b}</span></li>" for a, b in STEPS[lang])
    return f'<ol class="steps{" cols" if cols else ""}">{li}</ol>'


ORDER = {
    "en": [("Choose", "Pick the form and quantity from the product list."),
           ("Message our admin", "Send your order on WhatsApp. The admin checks stock and the shipping cost."),
           ("Transfer", "Pay to the company account and send the proof of transfer."),
           ("Delivery", "Your order is packed and shipped, and we share the tracking number with you.")],
    "zh": [("选择产品", "在产品列表中选好形态和数量。"),
           ("联系客服", "通过 WhatsApp 发来订单，客服确认库存和运费。"),
           ("转账付款", "转账到公司账户，并发来转账凭证。"),
           ("发货", "我们包装发货，并把快递单号发给您。")],
}


def order_html(lang):
    li = "".join(f"<li><b>{a}</b><span>{b}</span></li>" for a, b in ORDER[lang])
    return f'<ol class="steps cols">{li}</ol>'


def pay_note(lang):
    if lang == "en":
        return (f'<div class="note"><p><b>Payment goes only to accounts in the name of {esc(SITE["company"])}.</b> '
                'We never ask you to transfer to a personal account. If in doubt, confirm with our admin first.</p></div>')
    return (f'<div class="note"><p><b>货款只付至户名为 {esc(SITE["company"])} 的公司账户。</b>'
            '我们从不要求转账到个人账户。如有疑问，请先向客服确认。</p></div>')


# ── Beranda ─────────────────────────────────────────────────────────────────
def home(lang):
    en = lang == "en"
    u = lambda s: url(lang, s)  # noqa: E731
    cards = "".join(card(lang, g) for g in GRADES)
    if en:
        c = dict(
            title="Indonesia Yanwoo | Cleaned Bird’s Nest from Kalimantan, Indonesia",
            desc="Hand-cleaned edible bird’s nest from Markaswalet partner farmers in Kalimantan, Indonesia. Four forms plus sachets, packed as Nestsensials in Surabaya.",
            eyebrow="Bird’s nest from Kalimantan, Indonesia",
            h1="Clean bird’s nest, straight from Indonesian swiftlet houses",
            lead="Our nests come from Markaswalet partner farmers in Kalimantan. They are cleaned by hand without chemicals and packed ready to soak and steam: for yourself, for your family, or as a gift.",
            b1="See products and prices", b2="Visiting Indonesia?",
            hero_alt="Nestsensials gift box with cleaned bird’s nest and rock sugar",
            facts=[("No chemicals", "Cleaned by hand. No bleach, colouring or additives."),
                   ("From Kalimantan", "Harvested in the swiftlet houses of partner farmers."),
                   ("Clear origin", "Every pack traces back to a swiftlet house through the Markaswalet ecosystem."),
                   ("Fair to farmers", "Bought directly from farmers, without a long chain of middlemen.")],
            p_eyebrow="Products", p_h2="Four forms and a sachet",
            p_lead=f"It is all the same cleaned nest; the name describes the shape. Prices are per pack in Indonesian rupiah, as of {PRICE_DATE['en']}.",
            v_eyebrow="For visitors", v_h2="In Indonesia right now?",
            v_p="Buy at the source and enjoy it during your stay. We ship to hotels and homes across Indonesia. Check the customs rules before you fly: dried bird’s nest may not be carried into mainland China, while Singapore allows 1 kg per traveller.",
            v_b1="How to buy while travelling", v_b2="Rules by destination",
            s_eyebrow="Our process", s_h2="From swiftlet house to table",
            s_lead="Every piece goes through four stages before it reaches you.", s_more="More about process and quality",
            e_eyebrow="Serving", e_h2="Soak, steam, enjoy",
            e_p="The nests are already clean, so cooking is simple. Soak in clean water until fully expanded, pour the soaking water away, add fresh water and steam for 10 to 15 minutes. Serve with rock sugar, dates or milk.",
            e_p2="About 5 g of dry nest makes two servings.", e_alt="Soaked bird’s nest in a glass bowl next to a dry nest",
            g_eyebrow="Gifts", g_h2="Gift boxes and hampers",
            g_p="Our gift box holds a tray of cleaned nests and a jar of rock sugar. Seasonal editions for Lunar New Year and Eid, and orders for companies, can be arranged. Tell us the quantity, the budget and the delivery date.",
            g_b="Ask about hampers", g_alt="Nestsensials gift box with a tray of cleaned bird’s nest and a jar of rock sugar",
            a_eyebrow="Who we are", a_h2="Part of Markaswalet",
            a_p="Markaswalet is a platform owned by PT Lentera Alam Nusantara. It helps swiftlet farmers look after their swiftlet houses, monitor their bird populations and sell their nests at fairer prices. Indonesia Yanwoo brings those nests, packed under our Nestsensials brand, to buyers and visitors from abroad.",
            a_b="About us", a_alt="The Markaswalet team with plates of cleaned bird’s nest",
            i_h2="Wholesale and import enquiries",
            i_p="Import rules differ from country to country. Mainland China, for example, only accepts bird’s nest from Indonesian processing plants registered with China Customs (GACC). Tell us your destination and volume, and we will say plainly which forms we can supply and which documents we can provide.",
            i_b="Contact us",
        )
    else:
        c = dict(
            title="印尼燕窝 Indonesia Yanwoo｜加里曼丹屋燕·人工挑毛·产地直供",
            desc="印尼加里曼丹合作燕农的屋燕，人工挑毛，不加化学物质。燕盏、燕角、燕条、燕饼及便携小袋装，泗水 PT Lentera Alam Nusantara 出品。",
            keywords="印尼燕窝,加里曼丹燕窝,燕盏,燕角,燕条,燕饼,印尼燕窝多少钱,印尼燕窝能带回国吗",
            eyebrow="印尼加里曼丹燕窝",
            h1="来自印尼燕屋的洁净燕窝",
            lead="燕窝来自 Markaswalet 在加里曼丹的合作燕农，人工挑毛，不使用化学物质，泡发后即可炖煮。自用、孝敬长辈、送礼皆宜。",
            b1="查看产品与价格", b2="您正在印尼？",
            hero_alt="Nestsensials 礼盒：洁净燕窝配冰糖",
            facts=[("不加化学物质", "人工挑毛，不漂白、不染色、无添加。"),
                   ("加里曼丹产地", "采自合作燕农的燕屋。"),
                   ("来源清楚", "每一包都能通过 Markaswalet 体系追溯到燕屋。"),
                   ("善待燕农", "直接向燕农收购，不经层层中间商。")],
            p_eyebrow="产品", p_h2="四种形态，外加便携小袋",
            p_lead=f"都是同样洁净的燕窝，名称只是形态不同。价格按每包计算，单位为印尼盾，{PRICE_DATE['zh']}价格。",
            v_eyebrow="来印尼的朋友", v_h2="您正在印尼？",
            v_p="在产地购买，在印尼期间就能享用，我们可寄送到印尼各地的酒店和住址。上飞机前请先了解入境规定：干燕窝不能随身带入中国大陆，新加坡则允许每人携带 1 公斤。",
            v_b1="旅途中怎么买", v_b2="各地入境规定",
            s_eyebrow="加工流程", s_h2="从燕屋到餐桌",
            s_lead="每一片燕窝到您手上之前，都要经过四道工序。", s_more="了解加工与品质",
            e_eyebrow="食用方法", e_h2="泡发、清蒸，即可享用",
            e_p="燕窝已经清洁干净，做法很简单：用干净的水泡至完全发开，倒掉泡发的水，换上清水，蒸 10 至 15 分钟即可。可搭配冰糖、椰枣或牛奶。",
            e_p2="约 5 克干燕窝可做两人份。", e_alt="玻璃碗中泡发好的燕窝，旁边是干燕窝",
            g_eyebrow="礼品", g_h2="礼盒与节庆礼篮",
            g_p="礼盒内含一盒洁净燕窝和一罐冰糖。可安排春节、开斋节等节庆款，也接受企业批量订购。请告诉我们数量、预算和送达日期。",
            g_b="咨询礼盒", g_alt="Nestsensials 礼盒：一盒洁净燕窝和一罐冰糖",
            a_eyebrow="我们是谁", a_h2="Markaswalet 旗下",
            a_p="Markaswalet 是 PT Lentera Alam Nusantara 旗下的平台，帮助燕农管理燕屋、监测燕群数量，并以更公道的价格出售燕窝。Indonesia Yanwoo 把这些燕窝以 Nestsensials 品牌包装，介绍给海外买家和来印尼的朋友。",
            a_b="关于我们", a_alt="Markaswalet 团队与洁净燕窝",
            i_h2="批发与进口咨询",
            i_p="各国进口要求不同。例如中国大陆只接受在中国海关总署（GACC）注册的印尼加工企业出口的燕窝。请告诉我们目的地和数量，我们会如实说明可以供应的形态和能够提供的文件。",
            i_b="联系我们",
        )
    facts = "".join(f"<li><b>{a}</b><span>{b}</span></li>" for a, b in c["facts"])
    body = f'''
<section class="hero"><div class="wrap split">
  <div>
    <span class="eyebrow">{c["eyebrow"]}</span>
    <h1>{c["h1"]}</h1>
    <p class="lead">{c["lead"]}</p>
    <div class="btn-row"><a class="btn btn-green" href="{u("products")}">{c["b1"]}</a><a class="btn btn-line" href="{u("visitors")}">{c["b2"]}</a></div>
  </div>
  <img src="{img("hero-box.jpg")}" width="1000" height="1000" alt="{esc(c["hero_alt"])}">
</div></section>
<section class="alt"><div class="wrap"><ul class="facts">{facts}</ul></div></section>
<section><div class="wrap">
  <span class="eyebrow">{c["p_eyebrow"]}</span>
  <h2>{c["p_h2"]}</h2>
  <p class="lead">{c["p_lead"]}</p>
  <div class="grid g5" style="margin-top:26px">{cards}</div>
</div></section>
<section class="dark"><div class="wrap">
  <span class="eyebrow">{c["v_eyebrow"]}</span>
  <h2>{c["v_h2"]}</h2>
  <p class="lead">{c["v_p"]}</p>
  <div class="btn-row"><a class="btn btn-brand" href="{u("visitors")}">{c["v_b1"]}</a><a class="btn btn-line" href="{u("bring-home")}">{c["v_b2"]}</a></div>
</div></section>
<section><div class="wrap">
  <span class="eyebrow">{c["s_eyebrow"]}</span>
  <h2>{c["s_h2"]}</h2>
  <p class="lead">{c["s_lead"]}</p>
  <div style="margin-top:24px">{steps_html(lang)}</div>
  <div class="btn-row"><a class="btn btn-line" href="{u("process")}">{c["s_more"]}</a></div>
</div></section>
<section class="alt"><div class="wrap split">
  <img class="sq" src="{img("serve-soaked.jpg")}" width="900" height="900" loading="lazy" alt="{esc(c["e_alt"])}">
  <div>
    <span class="eyebrow">{c["e_eyebrow"]}</span>
    <h2>{c["e_h2"]}</h2>
    <p>{c["e_p"]}</p>
    <p class="small">{c["e_p2"]}</p>
  </div>
</div></section>
<section><div class="wrap split">
  <div>
    <span class="eyebrow">{c["g_eyebrow"]}</span>
    <h2>{c["g_h2"]}</h2>
    <p>{c["g_p"]}</p>
    <div class="btn-row"><a class="btn btn-green" href="{wa_link(lang)}" rel="noopener">{c["g_b"]}</a></div>
  </div>
  <img class="sq" src="{img("gift-box.jpg")}" width="900" height="900" loading="lazy" alt="{esc(c["g_alt"])}">
</div></section>
<section class="alt"><div class="wrap split">
  <img src="{img("team.jpg")}" width="1200" height="600" loading="lazy" alt="{esc(c["a_alt"])}">
  <div>
    <span class="eyebrow">{c["a_eyebrow"]}</span>
    <h2>{c["a_h2"]}</h2>
    <p>{c["a_p"]}</p>
    <div class="btn-row"><a class="btn btn-line" href="{u("about")}">{c["a_b"]}</a></div>
  </div>
</div></section>
<section><div class="wrap prose">
  <h2>{c["i_h2"]}</h2>
  <p>{c["i_p"]}</p>
  <div class="btn-row"><a class="btn btn-green" href="{u("contact")}">{c["i_b"]}</a></div>
</div></section>
'''
    return {"title": c["title"], "desc": c["desc"], "keywords": c.get("keywords", ""), "body": body,
            "jsonld": [{"@context": "https://schema.org", "@type": "WebSite", "name": SITE["brand"],
                        "url": "https://indonesiayanwoo.com" + url(lang), "inLanguage": "en" if en else "zh-CN"}]}


# ── Produk ──────────────────────────────────────────────────────────────────
def products(lang):
    en = lang == "en"
    if en:
        c = dict(
            title="Bird’s Nest Products and Prices | Indonesia Yanwoo",
            desc="Whole bowl, corner pieces, strips, nest cake and sachets of cleaned Kalimantan bird’s nest, with prices per pack in Indonesian rupiah and how to order.",
            h1="Products and prices",
            lead="All our bird’s nest comes from partner farmers in Kalimantan and is already cleaned. Prices are per pack; stock can change at any time.",
            k_form="Form", k_for="Best for", k_pack="Net weight", k_price="Price",
            common_h2="The same for every pack",
            common=[("Origin", "Swiftlet houses of partner farmers, Kalimantan, Indonesia"),
                    ("Condition", "Clean, ready to soak and steam"),
                    ("Cleaning", "By hand, with no bleach, colouring or additives"),
                    ("Storage", "Closed container, in a cool and dry place")],
            guide_h2="Which one should I choose?", th=("Type", "Shape", "Best for", "Price per pack"),
            price_note=f"Price list as of {PRICE_DATE['en']}, in Indonesian rupiah (IDR). Please confirm today’s price and stock on WhatsApp before you pay.",
            order_h2="How to order", order_lead="Orders are handled by our admin on WhatsApp.",
            b_wa="Order on WhatsApp", help_h2="Not sure which one?",
            help_p="Tell us what it is for: daily use, a gift, or for your parents. Our admin will help you pick.",
        )
    else:
        c = dict(
            title="印尼燕窝多少钱？燕盏、燕角、燕条、燕饼产品与价格｜Indonesia Yanwoo",
            desc="加里曼丹洁净燕窝的产品与价格：燕盏、燕角、燕条、燕饼和便携小袋装，附每包印尼盾价格、适合用途及订购方法。",
            keywords="印尼燕窝多少钱,印尼燕窝价格,燕盏,燕角,燕条,燕饼,加里曼丹燕窝",
            h1="产品与价格",
            lead="所有燕窝均来自加里曼丹的合作燕农，已清洁干净。价格按每包计算，库存随时可能变动。",
            k_form="形态", k_for="适合", k_pack="净重", k_price="价格",
            common_h2="每一包都一样",
            common=[("产地", "印尼加里曼丹，合作燕农的燕屋"),
                    ("状态", "已清洁，泡发后即可蒸炖"),
                    ("清洁方式", "人工挑毛，不漂白、不染色、无添加"),
                    ("保存", "密封容器，置于阴凉干燥处")],
            guide_h2="怎么选？", th=("种类", "形态", "适合", "每包价格"),
            price_note=f"以上为{PRICE_DATE['zh']}价格，单位为印尼盾（IDR）。每包 50 克即一两。付款前请通过 WhatsApp 确认当日价格和库存。",
            order_h2="订购方法", order_lead="订单由客服通过 WhatsApp 处理。",
            b_wa="通过 WhatsApp 订购", help_h2="不知道选哪种？",
            help_p="告诉我们用途：日常食用、送礼，还是给长辈。客服会帮您挑选。",
        )
    blocks = ""
    for g in GRADES:
        n = g[lang]
        blocks += f'''
  <div class="grade" id="{g["key"]}">
    <img src="{img(g["img"])}" width="800" height="800" loading="lazy" alt="{esc(n["name"])}">
    <div>
      <h3>{esc(n["name"])}</h3>
      <div class="alt-names">{esc(n["alt"])}</div>
      <p>{esc(n["desc"])}</p>
      <dl class="spec">
        <dt>{c["k_form"]}</dt><dd>{esc(n["form"])}</dd>
        <dt>{c["k_for"]}</dt><dd>{esc(n["for"])}</dd>
        <dt>{c["k_pack"]}</dt><dd>{g["pack"][lang]}</dd>
        <dt>{c["k_price"]}</dt><dd class="price">{rupiah(PRICES.get(g["key"]), lang)}</dd>
      </dl>
    </div>
  </div>'''
    rows = "".join(
        f'<tr><td>{esc(g[lang]["name"])}</td><td data-label="{c["th"][1]}">{esc(g[lang]["form"])}</td>'
        f'<td data-label="{c["th"][2]}">{esc(g[lang]["for"])}</td>'
        f'<td data-label="{c["th"][3]}">{rupiah(PRICES.get(g["key"]), lang)} / {g["pack"][lang]}</td></tr>' for g in GRADES)
    common = "".join(f"<dt>{a}</dt><dd>{b}</dd>" for a, b in c["common"])
    th = "".join(f"<th>{x}</th>" for x in c["th"])
    body = head(lang, "products", c["h1"], c["lead"]) + f'''
<section><div class="wrap">{blocks}
</div></section>
<section class="alt"><div class="wrap">
  <h2>{c["guide_h2"]}</h2>
  <div class="table-scroll"><table class="stack"><thead><tr>{th}</tr></thead><tbody>{rows}</tbody></table></div>
  <p class="small" style="margin-top:14px">{c["price_note"]}</p>
  <h2 style="margin-top:1.6em">{c["common_h2"]}</h2>
  <dl class="spec">{common}</dl>
</div></section>
<section><div class="wrap">
  <h2>{c["order_h2"]}</h2>
  <p class="lead">{c["order_lead"]}</p>
  <div style="margin-top:22px">{order_html(lang)}</div>
  {pay_note(lang)}
  <div class="btn-row"><a class="btn btn-green" href="{wa_link(lang)}" rel="noopener">{c["b_wa"]}</a></div>
</div></section>
<section class="dark"><div class="wrap">
  <h2>{c["help_h2"]}</h2>
  <p class="lead">{c["help_p"]}</p>
  <div class="btn-row"><a class="btn btn-brand" href="{wa_link(lang)}" rel="noopener">WhatsApp {esc(SITE["phone"])}</a></div>
</div></section>
'''
    return {"title": c["title"], "desc": c["desc"], "keywords": c.get("keywords", ""), "body": body,
            "jsonld": [crumbs_ld(lang, "products", label(lang, "products"))]}


# ── Proses & mutu ───────────────────────────────────────────────────────────
def process(lang):
    en = lang == "en"
    if en:
        c = dict(
            title="How Our Bird’s Nest Is Cleaned: Process and Quality | Indonesia Yanwoo",
            desc="Four stages from swiftlet house to pack: harvested, sorted, cleaned by hand and packed. Nitrite below 30 ppm, reverse-osmosis water, no bleach or additives.",
            h1="Process and quality",
            lead="Every piece of nest goes through four stages before it reaches you. Nothing is added along the way.",
            s_h2="Four stages", alt="Workers lifting feathers out of bird’s nest by hand with tweezers",
            q_h2="Our cleaning standard",
            q_lead="These are the figures we work to when we wash and pack.",
            facts=[("Below 30 ppm", "Nitrite content. China’s limit for imported bird’s nest is 30 mg/kg."),
                   ("Reverse-osmosis water", "Nests are washed in RO water with TDS below 40."),
                   ("Ozonated wash", "Ozonation is part of the washing step."),
                   ("Heated before packing", "A heating step before packing, to remove bacteria.")],
            n_h2="What we do not do",
            n_li=["No bleach. Natural bird’s nest is ivory to off-white, and we leave it that way.",
                  "No colouring.", "No additives of any kind."],
            t_h2="Clear origin",
            t_p="We buy directly from partner farmers, without a long chain of middlemen. Every pack comes from a swiftlet house that can be traced through the Markaswalet ecosystem, the platform we use every day to work with swiftlet farmers.",
            b="See products and prices",
        )
    else:
        c = dict(
            title="燕窝是怎样清洁的：加工流程与品质标准｜Indonesia Yanwoo 印尼燕窝",
            desc="从燕屋到包装的四道工序：采收、分拣、人工挑毛、包装。亚硝酸盐低于 30 ppm，反渗透纯净水清洗，不漂白、无添加。",
            keywords="燕窝加工流程,燕窝挑毛,燕窝亚硝酸盐,印尼燕窝品质,屋燕",
            h1="加工流程与品质",
            lead="每一片燕窝到您手上之前，都要经过四道工序，全程不添加任何东西。",
            s_h2="四道工序", alt="工人用镊子人工挑去燕窝中的羽毛",
            q_h2="我们的清洁标准",
            q_lead="清洗和包装时，我们按以下指标操作。",
            facts=[("低于 30 ppm", "亚硝酸盐含量。中国对进口燕窝的限量为 30 mg/kg。"),
                   ("反渗透纯净水", "使用 TDS 低于 40 的反渗透（RO）水清洗。"),
                   ("臭氧处理", "清洗过程中进行臭氧处理。"),
                   ("包装前加热", "包装前经过加热，去除细菌。")],
            n_h2="我们不做的事",
            n_li=["不漂白。天然燕窝本来就是象牙白或米白色，我们保持原样。", "不染色。", "不添加任何东西。"],
            t_h2="来源清楚",
            t_p="我们直接向合作燕农收购，不经层层中间商。每一包燕窝都来自一间可以通过 Markaswalet 体系追溯的燕屋；Markaswalet 是我们每天用来服务燕农的平台。",
            b="查看产品与价格",
        )
    facts = "".join(f"<li><b>{a}</b><span>{b}</span></li>" for a, b in c["facts"])
    nli = "".join(f"<li>{x}</li>" for x in c["n_li"])
    certs = certs_block(lang)
    certs_sec = f'<section><div class="wrap">{certs}</div></section>' if certs else ""
    body = head(lang, "process", c["h1"], c["lead"]) + f'''
<section><div class="wrap">
  <h2>{c["s_h2"]}</h2>
  <div style="margin-top:20px">{steps_html(lang)}</div>
  <img src="{img("cleaning-by-hand.jpg")}" width="1200" height="600" loading="lazy" alt="{esc(c["alt"])}" style="border-radius:16px;margin-top:28px;width:100%">
</div></section>
<section class="alt"><div class="wrap">
  <h2>{c["q_h2"]}</h2>
  <p class="lead">{c["q_lead"]}</p>
  <ul class="facts" style="margin-top:22px">{facts}</ul>
</div></section>
<section><div class="wrap prose">
  <h2>{c["n_h2"]}</h2>
  <ul>{nli}</ul>
  <h2>{c["t_h2"]}</h2>
  <p>{c["t_p"]}</p>
  <div class="btn-row"><a class="btn btn-green" href="{url(lang, "products")}">{c["b"]}</a></div>
</div></section>
{certs_sec}
'''
    return {"title": c["title"], "desc": c["desc"], "keywords": c.get("keywords", ""), "body": body,
            "jsonld": [crumbs_ld(lang, "process", label(lang, "process"))]}


# ── Untuk pengunjung ────────────────────────────────────────────────────────
def visitors(lang):
    en = lang == "en"
    u_bring, u_prod = url(lang, "bring-home"), url(lang, "products")
    if en:
        c = dict(
            title="Buying Bird’s Nest While Visiting Indonesia | Indonesia Yanwoo",
            desc="A visitor’s guide: how to order cleaned bird’s nest while you are in Indonesia, what to choose for a short stay, how to prepare it, and what to check before you fly.",
            h1="Buying bird’s nest while you are in Indonesia",
            lead="Indonesia is the world’s largest producer of edible bird’s nest. If you are travelling or living here, you can buy close to the source and enjoy it before you leave.",
            o_h2="Order in four steps",
            o_tip="<b>Tell us your travel dates.</b> Delivery time depends on the city. When you order, our admin confirms the shipping cost and whether the parcel can reach your hotel or address before you leave.",
            w_h2="What to choose",
            w=[("For a short stay", f'The <a href="{u_prod}#sachet">sachet pack</a>: five sachets of 5 g. One sachet is one cooking, about two servings, and it is easy to carry.'),
               ("As a gift", f'<a href="{u_prod}#bowl">Whole bowls</a>, or a gift box with a tray of nests and a jar of rock sugar.'),
               ("For the family", f'<a href="{u_prod}#strips">Strips</a> or <a href="{u_prod}#cake">nest cake</a>: the same clean nest at a lower price per pack.')],
            c_h2="Preparing it where you are staying",
            c_steps=["Soak the nest in enough clean water.", "Wait until it has fully expanded.", "Pour the soaking water away.",
                     "Add fresh, clean water.", "Steam for 10 to 15 minutes.", "It is ready to enjoy."],
            r_h3="Three simple ideas",
            r=[("Rock-sugar soup", "5 g bird’s nest, 400 ml water, rock sugar to taste, 2 pandan leaves. About 30 minutes, two servings."),
               ("With milk and dates", "5 g bird’s nest, 300 ml fresh milk, 4 dates, honey to taste. About 25 minutes, two servings."),
               ("Warm ginger drink", "5 g bird’s nest, 2 pieces of roasted ginger, palm sugar to taste, 400 ml water. About 30 minutes, two servings.")],
            st="Keep dry nest in a closed container in a cool, dry place away from direct sunlight. Once cooked, keep it in the fridge and finish it soon.",
            f_h2="Before you fly",
            f_p=f'Rules for carrying bird’s nest across a border differ a lot. <b>Dried bird’s nest may not be carried or mailed into mainland China</b>; only commercially sterilised canned bird’s nest is allowed. Singapore allows 1 kg of cleaned dried bird’s nest per traveller. Read <a href="{u_bring}">the rules by destination</a> before you buy for the journey home.',
            l_h2="Living in Indonesia?",
            l_p="If you live or work in Indonesia, we can send regular orders to your home or office. For Lunar New Year, Eid and other occasions we prepare gift boxes and hampers, including orders for companies with a greeting card in the company’s name.",
            b="Message us on WhatsApp",
        )
    else:
        c = dict(
            title="来印尼旅游买燕窝指南：怎么买、怎么选、怎么吃｜Indonesia Yanwoo",
            desc="来印尼旅游或在印尼工作生活，怎样在产地买到洁净燕窝：订购步骤、短期停留选什么、怎么泡发蒸炖，以及上飞机前要了解的规定。",
            keywords="印尼旅游买燕窝,印尼燕窝,在印尼买燕窝,印尼燕窝能带回国吗,燕窝怎么泡发",
            h1="来印尼旅游，怎么买燕窝",
            lead="印尼是全球最大的燕窝产地。无论您是来旅游，还是在印尼工作生活，都可以在产地就近购买，并在离开前享用。",
            o_h2="四步完成订购",
            o_tip="<b>请告诉我们您的行程日期。</b>配送时间因城市而异。下单时，客服会确认运费，以及包裹能否在您离开前送到酒店或住址。",
            w_h2="选哪一种",
            w=[("短期停留", f'<a href="{u_prod}#sachet">便携小袋装</a>：5 小袋，每袋 5 克。一袋正好炖一次，约两人份，方便携带。'),
               ("送礼", f'<a href="{u_prod}#bowl">燕盏</a>，或内含一盒燕窝和一罐冰糖的礼盒。'),
               ("全家食用", f'<a href="{u_prod}#strips">燕条</a>或<a href="{u_prod}#cake">燕饼</a>：同样洁净的燕窝，每包价格更实惠。')],
            c_h2="在住处怎么做",
            c_steps=["用适量干净的水浸泡燕窝。", "等燕窝完全发开。", "倒掉泡发的水。", "换上干净的清水。", "蒸 10 至 15 分钟。", "即可享用。"],
            r_h3="三种简单做法",
            r=[("冰糖燕窝", "燕窝 5 克、水 400 毫升、冰糖适量、香兰叶 2 片。约 30 分钟，两人份。"),
               ("牛奶椰枣燕窝", "燕窝 5 克、鲜牛奶 300 毫升、椰枣 4 颗、蜂蜜适量。约 25 分钟，两人份。"),
               ("姜茶燕窝", "燕窝 5 克、烤姜 2 块、棕榈糖适量、水 400 毫升。约 30 分钟，两人份。")],
            st="干燕窝请放入密封容器，置于阴凉干燥处，避免阳光直射。炖好的燕窝请放冰箱冷藏，并尽快食用。",
            f_h2="上飞机之前",
            f_p=f'各地对携带燕窝入境的规定差别很大。<b>干燕窝不能随身携带或邮寄进入中国大陆</b>，只有经商业无菌处理的罐头装燕窝可以；新加坡允许每人携带 1 公斤已清洁的干燕窝。打算带回去的话，请先看<a href="{u_bring}">各地入境规定</a>再买。',
            l_h2="长住印尼的朋友",
            l_p="如果您在印尼工作或生活，我们可以定期把燕窝寄到您的住处或办公室。春节、开斋节等节日，我们可以准备礼盒和礼篮，也接受企业订购，并可附上以公司名义署名的贺卡。",
            b="通过 WhatsApp 联系我们",
        )
    w = "".join(f"<li><b>{a}</b><span>{b}</span></li>" for a, b in c["w"])
    cs = "".join(f"<li>{x}</li>" for x in c["c_steps"])
    r = "".join(f"<li><b>{a}</b><span>{b}</span></li>" for a, b in c["r"])
    body = head(lang, "visitors", c["h1"], c["lead"]) + f'''
<section><div class="wrap">
  <h2>{c["o_h2"]}</h2>
  <div style="margin-top:20px">{order_html(lang)}</div>
  <div class="note"><p>{c["o_tip"]}</p></div>
  {pay_note(lang)}
</div></section>
<section class="alt"><div class="wrap">
  <h2>{c["w_h2"]}</h2>
  <ul class="facts" style="margin-top:20px">{w}</ul>
</div></section>
<section><div class="wrap split" style="align-items:start">
  <div class="prose">
    <h2>{c["c_h2"]}</h2>
    <ol>{cs}</ol>
    <p class="small">{c["st"]}</p>
  </div>
  <img class="sq" src="{img("serve-soaked.jpg")}" width="900" height="900" loading="lazy" alt="">
</div>
<div class="wrap" style="margin-top:32px">
  <h3>{c["r_h3"]}</h3>
  <ul class="facts">{r}</ul>
</div></section>
<section class="dark"><div class="wrap">
  <h2>{c["f_h2"]}</h2>
  <p class="lead" style="max-width:48em">{c["f_p"]}</p>
  <div class="btn-row"><a class="btn btn-brand" href="{u_bring}">{label(lang, "bring-home")}</a></div>
</div></section>
<section><div class="wrap prose">
  <h2>{c["l_h2"]}</h2>
  <p>{c["l_p"]}</p>
  <div class="btn-row"><a class="btn btn-green" href="{wa_link(lang)}" rel="noopener">{c["b"]}</a></div>
</div></section>
'''
    return {"title": c["title"], "desc": c["desc"], "keywords": c.get("keywords", ""), "body": body,
            "jsonld": [crumbs_ld(lang, "visitors", label(lang, "visitors"))]}


# ── Aturan membawa pulang ───────────────────────────────────────────────────
SRC = {
    "rmrb": "http://paper.people.com.cn/rmrbhwb/html/2024-08/24/content_26076641.htm",
    "hk_lcq": "https://www.info.gov.hk/gia/general/202509/25/P2025092500581p.htm",
    "sfa": "https://www.sfa.gov.sg/bringing-food-for-personal-use-from-overseas/list-of-food--food-products-allowed",
    "hk_customs": "https://www.customs.gov.hk/en/faqs/passenger_clearance/index.html",
    "au": "https://www.agriculture.gov.au/biosecurity-trade/travelling/bringing-mailing-goods",
}


def bring_home(lang):
    en = lang == "en"
    u_vis, u_con = url(lang, "visitors"), url(lang, "contact")
    if en:
        c = dict(
            title="Can You Take Indonesian Bird’s Nest Home? Rules by Destination",
            desc="Dried bird’s nest may not be carried or mailed into mainland China; only sterilised canned nest is allowed. Singapore allows 1 kg per traveller. With official sources.",
            h1="Can you take Indonesian bird’s nest home?",
            lead=f"It depends on where home is. Dried bird’s nest may not be carried or mailed into mainland China, while Singapore allows 1 kg per traveller. Below are the rules we checked in {RULES_CHECKED['en']}, with the official sources.",
            th=("Destination", "Dried bird’s nest in your luggage", "What the rule says"),
            rows=[
                ("Mainland China", "no", "Not allowed",
                 "Bird’s nest is on China’s list of animal and plant products that may not be carried or mailed into the country. The only exception is commercially sterilised canned bird’s nest. There is no official personal allowance in grams or kilograms."),
                ("Singapore", "ok", "Up to 1 kg per traveller",
                 "The Singapore Food Agency lists cleaned dried bird’s nest from all countries and regions, with a limit of 1 kg per traveller, strictly for personal consumption."),
                ("Hong Kong", "ask", "Confirm first",
                 "We found no published limit specific to bird’s nest. Hong Kong Customs says food carried in personal baggage for personal consumption, in a reasonable quantity, is generally not subject to control. Confirm with the Centre for Food Safety before you travel. Going on from Hong Kong into the mainland, the mainland rule applies."),
                ("Taiwan", "ask", "Confirm first",
                 "Quantity limits and animal-quarantine requirements apply. Check with Taiwan Customs and the animal and plant quarantine authority before you buy."),
                ("Australia", "ask", "Declare it",
                 "Australia’s agriculture department treats bird nests as goods of biosecurity concern. You must declare it on arrival; check the import conditions in BICON before you buy."),
                ("Other destinations", "ask", "Confirm first",
                 "We have not checked every country. Follow the latest notice from the customs and quarantine authorities of your destination."),
            ],
            cn_h2="Mainland China: why dried bird’s nest cannot go in your suitcase",
            cn_li=[
                f'Answering a traveller in the overseas edition of People’s Daily (24 August 2024), Gongbei Customs wrote: “燕窝禁止携带进境。但经商业无菌处理的罐头装燕窝可以携带进境。” In English: bird’s nest may not be carried into the country, but commercially sterilised canned bird’s nest may. ({ext(SRC["rmrb"], "source")})',
                f'In September 2025 the Hong Kong government confirmed to its legislature that bird’s nest, except commercially sterilised canned products, is still on the mainland’s list and cannot be carried or mailed into the mainland. ({ext(SRC["hk_lcq"], "source")})',
                "We could not find any official basis for the “so many grams per person” figures that circulate online.",
                "This applies however small the amount is. Declare what you carry, and do not hide it.",
            ],
            do_h2="If you live in mainland China, what you can do",
            do_li=[
                f'<b>Enjoy it while you are in Indonesia.</b> We deliver to hotels and addresses across the country; a sachet pack is enough for a short stay. See <a href="{u_vis}">our guide for visitors</a>.',
                "<b>Know what is allowed.</b> Only commercially sterilised canned bird’s nest may be carried in. The forms on this site are dried bird’s nest, so they do not fall under that exception.",
                f'<b>Import through the formal channel.</b> China only accepts bird’s nest from Indonesian processing plants registered with China Customs (GACC). If you are an importer, <a href="{u_con}">tell us your destination and volume</a> and we will say plainly what we can supply and which documents we can provide.',
            ],
            id_h2="Leaving Indonesia",
            id_p="Under Indonesia’s quarantine law (Law No. 21 of 2019), animal products leaving the country must be reported to the quarantine officers at the airport or port, and that includes small amounts carried by hand. Ask at the quarantine counter of your departure airport what is needed for your route, and ask us before you buy if you plan to carry bird’s nest out of the country.",
            tip_h2="Practical points",
            tips=["Keep the original packaging and the proof of purchase.", "Declare what you carry.",
                  "Rules change. The latest notice from the destination’s customs and quarantine authorities is what counts."],
            src_h2="Sources",
            src=[(SRC["rmrb"], "People’s Daily overseas edition, 24 August 2024: Gongbei Customs answers a traveller’s question (Chinese)"),
                 (SRC["hk_lcq"], "Hong Kong Government, 25 September 2025: reply on carrying bird’s nest products into the Mainland"),
                 (SRC["sfa"], "Singapore Food Agency: food products travellers may bring in for personal use"),
                 (SRC["hk_customs"], "Hong Kong Customs and Excise Department: passenger clearance FAQ"),
                 (SRC["au"], "Australian Government, Department of Agriculture: bringing or mailing goods to Australia")],
            disc=f"This page is general information checked in {RULES_CHECKED['en']}, not legal advice.",
            faq=[("Can I carry Indonesian bird’s nest into mainland China?",
                  "No. Dried bird’s nest may not be carried or mailed into mainland China. Only commercially sterilised canned bird’s nest is allowed, and there is no official personal allowance in grams."),
                 ("How much bird’s nest can I bring into Singapore?",
                  "The Singapore Food Agency allows up to 1 kg of cleaned dried bird’s nest per traveller, from any country, for personal consumption."),
                 ("Do I need to report bird’s nest when leaving Indonesia?",
                  "Yes. Under Law No. 21 of 2019, animal products leaving Indonesia must be reported to the quarantine officers at the airport or port, including small amounts carried by hand.")],
        )
    else:
        c = dict(
            title="印尼燕窝能带回国吗？中国大陆、新加坡、香港入境规定｜Indonesia Yanwoo",
            desc="干燕窝不能随身携带或邮寄进入中国大陆，只有经商业无菌处理的罐头装燕窝可以；新加坡每人可带 1 公斤已清洁干燕窝。附官方来源。",
            keywords="印尼燕窝能带回国吗,印尼燕窝可以带回中国吗,燕窝能带入境吗,燕窝海关规定,罐头装燕窝",
            h1="印尼燕窝能带回国吗？",
            lead=f"要看您回哪里。干燕窝不能随身携带或邮寄进入中国大陆；回新加坡，每人可带 1 公斤。以下是我们在{RULES_CHECKED['zh']}核对过的各地规定和官方来源。",
            th=("目的地", "干燕窝能否随身携带", "规定内容"),
            rows=[
                ("中国大陆", "no", "不可以",
                 "燕窝列入《中华人民共和国禁止携带、寄递进境的动植物及其产品和其他检疫物名录》，不能携带或邮寄进境。唯一的例外是经商业无菌处理的罐头装燕窝。没有“每人可带多少克”的官方额度。"),
                ("新加坡", "ok", "每人最多 1 公斤",
                 "新加坡食品局（SFA）规定：已清洁的干燕窝，不限来源国家或地区，每位旅客限带 1 公斤，仅供个人食用。"),
                ("香港", "ask", "请先确认",
                 "我们没有找到专门针对燕窝的公开限量。香港海关表示，旅客在随身行李中携带合理数量、供个人食用的食物，一般不受管制。出发前请向食物安全中心确认。从香港再进入内地，适用内地规定。"),
                ("台湾", "ask", "请先确认",
                 "入境有数量限制和动物检疫要求，购买前请向台湾海关和动植物检疫机关确认。"),
                ("澳大利亚", "ask", "必须申报",
                 "澳大利亚农业部门把鸟巢类物品列为生物安全关注物品，入境时必须申报；购买前请在 BICON 查询进口条件。"),
                ("其他国家和地区", "ask", "请先确认",
                 "我们没有逐一核对，请以目的地海关和检疫部门的最新公告为准。"),
            ],
            cn_h2="中国大陆：为什么干燕窝不能放进行李箱",
            cn_li=[
                f'拱北海关在《人民日报海外版》（2024年8月24日）答复旅客提问时写明：“燕窝禁止携带进境。但经商业无菌处理的罐头装燕窝可以携带进境。”（{ext(SRC["rmrb"], "来源")}）',
                f'2025年9月，香港特区政府答复立法会时确认：燕窝（经商业无菌处理的罐头装燕窝产品除外）仍列在内地的名录内，不得携带或邮寄进入内地。（{ext(SRC["hk_lcq"], "来源")}）',
                "网上流传的“每人可带多少克”之类的说法，我们没有找到任何官方依据。",
                "数量再少也一样。携带物品请如实申报，不要藏匿。",
            ],
            do_h2="住在中国大陆的朋友，可以怎么做",
            do_li=[
                f'<b>在印尼期间享用。</b>我们可以寄送到印尼各地的酒店和住址，短期停留选便携小袋装就够了。详见<a href="{u_vis}">来印尼买燕窝指南</a>。',
                "<b>了解哪些可以带。</b>只有经商业无菌处理的罐头装燕窝可以携带进境。本站所列各种形态均为干燕窝，不属于这一例外。",
                f'<b>通过正规渠道进口。</b>中国只接受在中国海关总署（GACC）注册的印尼加工企业出口的燕窝。如果您是进口商，请<a href="{u_con}">告诉我们目的地和数量</a>，我们会如实说明可以供应的形态和能够提供的文件。',
            ],
            id_h2="离开印尼时",
            id_p="按照印尼检疫法（2019年第21号法律），动物产品出境必须在机场或港口向检疫官员申报，随身携带的少量物品也不例外。请向出发机场的检疫柜台询问您这条航线需要办理的手续；如果打算把燕窝带出印尼，也请在购买前先问我们。",
            tip_h2="几点提醒",
            tips=["保留原包装和购买凭证。", "携带物品请如实申报。", "规定会变动，请以目的地海关和检疫部门的最新公告为准。"],
            src_h2="资料来源",
            src=[(SRC["rmrb"], "《人民日报海外版》2024年8月24日：拱北海关答复旅客提问"),
                 (SRC["hk_lcq"], "香港特区政府新闻公报，2025年9月25日：关于携带燕窝产品进入内地的答复"),
                 (SRC["sfa"], "新加坡食品局（SFA）：旅客可携带入境供个人食用的食品清单"),
                 (SRC["hk_customs"], "香港海关：旅客清关常见问题"),
                 (SRC["au"], "澳大利亚农业部门：携带或邮寄物品入境须知")],
            disc=f"本页为{RULES_CHECKED['zh']}核对的一般信息，不构成法律意见。",
            faq=[("印尼燕窝能带回中国大陆吗？",
                  "不能。干燕窝不能随身携带或邮寄进入中国大陆，只有经商业无菌处理的罐头装燕窝可以携带，也没有“每人可带多少克”的官方额度。"),
                 ("带回新加坡可以带多少燕窝？",
                  "新加坡食品局规定，每位旅客最多可携带 1 公斤已清洁的干燕窝，不限来源国家，仅供个人食用。"),
                 ("从印尼带燕窝出境需要申报吗？",
                  "需要。按照印尼 2019 年第 21 号法律，动物产品出境必须在机场或港口向检疫官员申报，随身携带的少量物品也不例外。")],
        )
    th = "".join(f"<th>{x}</th>" for x in c["th"])
    rows = "".join(f'<tr><td>{a}</td><td><span class="pill {k}">{b}</span></td><td>{d}</td></tr>' for a, k, b, d in c["rows"])
    li = lambda xs: "".join(f"<li>{x}</li>" for x in xs)  # noqa: E731
    src = "".join(f"<li>{ext(h, t)}</li>" for h, t in c["src"])
    body = head(lang, "bring-home", c["h1"], c["lead"]) + f'''
<section><div class="wrap">
  <div class="table-scroll"><table class="stack"><thead><tr>{th}</tr></thead><tbody>{rows}</tbody></table></div>
  <p class="small" style="margin-top:14px">{c["disc"]}</p>
</div></section>
<section class="alt"><div class="wrap prose">
  <h2>{c["cn_h2"]}</h2>
  <ul>{li(c["cn_li"])}</ul>
  <h2>{c["do_h2"]}</h2>
  <ul>{li(c["do_li"])}</ul>
</div></section>
<section><div class="wrap prose">
  <h2>{c["id_h2"]}</h2>
  <p>{c["id_p"]}</p>
  <h2>{c["tip_h2"]}</h2>
  <ul>{li(c["tips"])}</ul>
  <h2>{c["src_h2"]}</h2>
  <ol class="sources">{src}</ol>
</div></section>
'''
    return {"title": c["title"], "desc": c["desc"], "keywords": c.get("keywords", ""), "body": body,
            "jsonld": [crumbs_ld(lang, "bring-home", label(lang, "bring-home")), faq_ld(c["faq"])]}


# ── Tentang ─────────────────────────────────────────────────────────────────
def about(lang):
    en = lang == "en"
    addr = f'{esc(SITE["street"])}, {esc(SITE["city"])} {esc(SITE["postal"])}'
    if en:
        c = dict(
            title="About Indonesia Yanwoo | PT Lentera Alam Nusantara, Surabaya",
            desc="Indonesia Yanwoo is the bird’s nest site of PT Lentera Alam Nusantara (Markaswalet), Surabaya: nests bought directly from partner swiftlet farmers in Kalimantan.",
            h1="It began in the farmers’ swiftlet houses",
            lead="Our bird’s nest grew out of Markaswalet, a platform that works with Indonesian swiftlet farmers every day. We want the farmers’ best nests to reach family tables clean and honestly described.",
            v_h2="What we stand for",
            v=[("Fair to farmers", "We buy directly from partner farmers, without a long chain of middlemen."),
               ("Clean without chemicals", "Nests are cleaned by hand. No bleach, no colouring, no additives."),
               ("Clear origin", "Every pack comes from a swiftlet house that can be traced through the Markaswalet ecosystem.")],
            m_h2="Part of Markaswalet",
            m_p="Markaswalet is a platform owned by PT Lentera Alam Nusantara. It helps swiftlet farmers look after their swiftlet houses, monitor their bird populations and sell their nests at fairer prices. Selling cleaned nests under the Nestsensials brand is how we bring their harvest straight to the people who eat it.",
            n_h2="The name",
            n_p="“Yanwoo” is our spelling of 燕窝 (yànwō), the Chinese word for bird’s nest. This site is where buyers and visitors from abroad can read about our nests in English and Chinese.",
            f_h2="Company details",
            f=[("Company", esc(SITE["company"])), ("Site", "Indonesia Yanwoo (indonesiayanwoo.com)"),
               ("Pack brand", "Nestsensials"), ("Platform", "Markaswalet"),
               ("Office", addr + ", East Java, Indonesia"), ("Origin of nests", "Partner farmers’ swiftlet houses, Kalimantan"),
               ("Email", f'<a href="mailto:{esc(SITE["email"])}">{esc(SITE["email"])}</a>')],
            alt_house="A swiftlet house in Indonesia", alt_team="The Markaswalet team",
            b="Contact us",
        )
    else:
        c = dict(
            title="关于我们｜Indonesia Yanwoo 印尼燕窝（PT Lentera Alam Nusantara，泗水）",
            desc="Indonesia Yanwoo 是泗水 PT Lentera Alam Nusantara（Markaswalet）的燕窝网站：直接向加里曼丹合作燕农收购，人工清洁。",
            keywords="印尼燕窝公司,印尼燕窝厂家,泗水燕窝,Markaswalet,PT Lentera Alam Nusantara",
            h1="从燕农的燕屋开始",
            lead="我们的燕窝源于 Markaswalet，一个每天与印尼燕农打交道的平台。我们希望把燕农最好的燕窝，干干净净、如实地送到每个家庭的餐桌上。",
            v_h2="我们的坚持",
            v=[("善待燕农", "直接向合作燕农收购，不经层层中间商。"),
               ("洁净无化学物质", "人工挑毛，不漂白、不染色、无添加。"),
               ("来源清楚", "每一包都来自一间可以通过 Markaswalet 体系追溯的燕屋。")],
            m_h2="Markaswalet 旗下",
            m_p="Markaswalet 是 PT Lentera Alam Nusantara 旗下的平台，帮助燕农管理燕屋、监测燕群数量，并以更公道的价格出售燕窝。以 Nestsensials 品牌销售洁净燕窝，是我们把燕农的收成直接送到食用者手中的方式。",
            n_h2="名字的由来",
            n_p="“Yanwoo”就是“燕窝”（yànwō）的拼写。这个网站用中文和英文向海外买家和来印尼的朋友介绍我们的燕窝。",
            f_h2="公司信息",
            f=[("公司", esc(SITE["company"])), ("网站", "Indonesia Yanwoo（indonesiayanwoo.com）"),
               ("包装品牌", "Nestsensials"), ("平台", "Markaswalet"),
               ("办公地址", addr + "，印度尼西亚东爪哇省"), ("燕窝产地", "加里曼丹，合作燕农的燕屋"),
               ("电子邮箱", f'<a href="mailto:{esc(SITE["email"])}">{esc(SITE["email"])}</a>')],
            alt_house="印尼的一间燕屋", alt_team="Markaswalet 团队",
            b="联系我们",
        )
    v = "".join(f"<li><b>{a}</b><span>{b}</span></li>" for a, b in c["v"])
    f = "".join(f"<dt>{a}</dt><dd>{b}</dd>" for a, b in c["f"])
    certs = certs_block(lang)
    body = head(lang, "about", c["h1"], c["lead"]) + f'''
<section><div class="wrap">
  <h2>{c["v_h2"]}</h2>
  <ul class="facts" style="margin-top:20px">{v}</ul>
</div></section>
<section class="alt"><div class="wrap split">
  <img src="{img("team.jpg")}" width="1200" height="600" loading="lazy" alt="{esc(c["alt_team"])}">
  <div>
    <h2>{c["m_h2"]}</h2>
    <p>{c["m_p"]}</p>
  </div>
</div></section>
<section><div class="wrap split" style="align-items:start">
  <div class="prose">
    <h2>{c["n_h2"]}</h2>
    <p>{c["n_p"]}</p>
    <h2>{c["f_h2"]}</h2>
    <dl class="spec">{f}</dl>
    {certs}
    <div class="btn-row"><a class="btn btn-green" href="{url(lang, "contact")}">{c["b"]}</a></div>
  </div>
  <img src="{img("swiftlet-house.jpg")}" width="900" height="1000" loading="lazy" alt="{esc(c["alt_house"])}" style="max-width:420px;justify-self:center">
</div></section>
'''
    return {"title": c["title"], "desc": c["desc"], "keywords": c.get("keywords", ""), "body": body,
            "jsonld": [crumbs_ld(lang, "about", label(lang, "about"))]}


# ── FAQ ─────────────────────────────────────────────────────────────────────
def faq(lang):
    en = lang == "en"
    u_bring, u_con, u_prod = url(lang, "bring-home"), url(lang, "contact"), url(lang, "products")
    if en:
        title = "Bird’s Nest FAQ: Cleaning, Cooking, Storage | Indonesia Yanwoo"
        desc = "Answers about our Kalimantan bird’s nest: is it clean, why it is not pure white, how to soak and steam it, storage, delivery, payment and taking it home."
        kw = ""
        h1, lead = "Frequently asked questions", "Did not find your answer? Ask our admin directly on WhatsApp."
        items = [
            ("Is the bird’s nest already clean?",
             "<p>Yes. Feathers and dirt are lifted out by hand, without chemicals, so all you need to do is soak it and steam it.</p>"),
            ("Is anything added to it?",
             "<p>No. It is bird’s nest and nothing else: no bleach, no colouring and no additives.</p>"),
            ("Why is it not pure white?",
             "<p>Natural bird’s nest is ivory to off-white. We do not bleach it, so the colour can differ a little from one harvest to the next.</p>"),
            ("How do I prepare it?",
             "<ol><li>Soak the nest in enough clean water.</li><li>Wait until it has fully expanded.</li><li>Pour the soaking water away.</li><li>Add fresh, clean water.</li><li>Steam for 10 to 15 minutes.</li></ol><p>Enjoy it with rock sugar, dates or milk.</p>"),
            ("How much do I need for one cooking?",
             "<p>About 5 g of dry nest makes two servings. One sachet in our sachet pack is 5 g.</p>"),
            ("How should I store it?",
             "<p>Keep it in a tightly closed container in a cool, dry place, away from direct sunlight. Cooked bird’s nest should be kept in the fridge and finished soon.</p>"),
            ("How much does it cost?",
             f'<p>Prices are per pack, in Indonesian rupiah, and are listed on the <a href="{u_prod}">products page</a>. Please confirm today’s price and stock on WhatsApp before paying.</p>'),
            ("How long does delivery take?",
             "<p>We ship to addresses across Indonesia, including hotels. Delivery time depends on the city. When you order, our admin confirms the shipping cost, and once the parcel is on its way we send you the tracking number.</p>"),
            ("How do I pay?",
             f'<p>By bank transfer to the company account of {esc(SITE["company"])}. We never ask you to transfer to a personal account.</p>'),
            ("Can I order for an event or for my company?",
             "<p>Yes. We prepare gift boxes and hampers, including seasonal editions for Lunar New Year and Eid, and larger orders for companies. Tell us the quantity, the budget and the delivery date.</p>"),
            ("Can I take it home on the plane?",
             f'<p>It depends on your destination. Dried bird’s nest may not be carried or mailed into mainland China; Singapore allows 1 kg per traveller. See <a href="{u_bring}">the rules by destination</a>.</p>'),
            ("Do you ship abroad?",
             f'<p>We deliver within Indonesia. Sending bird’s nest across a border depends on the import rules of the destination country. <a href="{u_con}">Write to us</a> with the country and the quantity and we will tell you plainly what is possible.</p>'),
            ("Is Indonesian bird’s nest different from Malaysian bird’s nest?",
             "<p>Both countries produce nests in swiftlet houses, and the island of Borneo, called Kalimantan on the Indonesian side, is shared by both. What you can check matters more than the country name: how the nest was cleaned, whether anything was added, and its shape. Ours comes from Kalimantan and is cleaned by hand without chemicals.</p>"),
            ("Do you supply importers and wholesalers?",
             f'<p>Import rules differ from country to country. Mainland China, for example, only accepts bird’s nest from Indonesian processing plants registered with China Customs (GACC). <a href="{u_con}">Tell us your destination and volume</a>, and we will say plainly which forms we can supply and which documents we can provide.</p>'),
        ]
    else:
        title = "印尼燕窝常见问题：清洁、泡发、蒸炖、保存、订购｜Indonesia Yanwoo"
        desc = "关于加里曼丹燕窝的常见问题：是否已清洁、为什么不是纯白、怎么泡发蒸炖、怎么保存、配送与付款，以及能否带回国。"
        kw = "燕窝怎么泡发,燕窝怎么炖,燕窝怎么保存,印尼燕窝和马来燕窝有什么区别,印尼燕窝多少钱"
        h1, lead = "常见问题", "没有找到答案？请直接通过 WhatsApp 询问客服。"
        items = [
            ("燕窝已经清洁干净了吗？",
             "<p>是的。羽毛和杂质都是人工挑出的，不使用化学物质，您只需泡发后蒸炖即可。</p>"),
            ("有没有添加任何东西？",
             "<p>没有。就是燕窝本身：不漂白、不染色、无添加。</p>"),
            ("为什么不是纯白色？",
             "<p>天然燕窝本来就是象牙白或米白色。我们不漂白，所以不同批次的颜色可能略有差别。</p>"),
            ("怎么泡发和蒸炖？",
             "<ol><li>用适量干净的水浸泡燕窝。</li><li>等燕窝完全发开。</li><li>倒掉泡发的水。</li><li>换上干净的清水。</li><li>蒸 10 至 15 分钟。</li></ol><p>可搭配冰糖、椰枣或牛奶享用。</p>"),
            ("一次用多少？",
             "<p>约 5 克干燕窝可做两人份。便携小袋装每袋正好 5 克。</p>"),
            ("怎么保存？",
             "<p>放入密封容器，置于阴凉干燥处，避免阳光直射。炖好的燕窝请放冰箱冷藏，并尽快食用。</p>"),
            ("印尼燕窝多少钱？",
             f'<p>价格按每包计算，单位为印尼盾，详见<a href="{u_prod}">产品与价格</a>。每包 50 克即一两。付款前请通过 WhatsApp 确认当日价格和库存。</p>'),
            ("多久能收到？",
             "<p>我们可寄送到印尼各地的地址，包括酒店。配送时间因城市而异。下单时客服会确认运费；发货后，我们会把快递单号发给您。</p>"),
            ("怎么付款？",
             f'<p>银行转账至户名为 {esc(SITE["company"])} 的公司账户。我们从不要求转账到个人账户。</p>'),
            ("可以为活动或公司订购吗？",
             "<p>可以。我们可以准备礼盒和礼篮，包括春节、开斋节等节庆款，也接受企业批量订购。请告诉我们数量、预算和送达日期。</p>"),
            ("可以带上飞机带回国吗？",
             f'<p>要看目的地。干燕窝不能随身携带或邮寄进入中国大陆；新加坡允许每人携带 1 公斤。详见<a href="{u_bring}">各地入境规定</a>。</p>'),
            ("可以寄到国外吗？",
             f'<p>我们在印尼境内配送。把燕窝寄往国外，取决于目的地国家的进口规定。请<a href="{u_con}">来信</a>告知国家和数量，我们会如实告诉您是否可行。</p>'),
            ("印尼燕窝和马来燕窝有什么区别？",
             "<p>两国都出产燕屋里的屋燕，而婆罗洲岛（印尼一侧称加里曼丹）本就由两国共有。比起产地国名，更值得看的是：怎么清洁的、有没有添加、是什么形态。我们的燕窝来自加里曼丹，人工挑毛，不使用化学物质。</p>"),
            ("可以供货给进口商和批发商吗？",
             f'<p>各国进口要求不同。例如中国大陆只接受在中国海关总署（GACC）注册的印尼加工企业出口的燕窝。请<a href="{u_con}">告诉我们目的地和数量</a>，我们会如实说明可以供应的形态和能够提供的文件。</p>'),
        ]
    body = head(lang, "faq", h1, lead) + f'''
<section><div class="wrap" style="max-width:860px">
  {qa_html(items)}
  <div class="btn-row"><a class="btn btn-green" href="{wa_link(lang)}" rel="noopener">WhatsApp {esc(SITE["phone"])}</a></div>
</div></section>
'''
    return {"title": title, "desc": desc, "keywords": kw, "body": body,
            "jsonld": [crumbs_ld(lang, "faq", label(lang, "faq")), faq_ld(items)]}


# ── Kontak ──────────────────────────────────────────────────────────────────
def contact(lang):
    en = lang == "en"
    addr = f'{esc(SITE["street"])}<br>{esc(SITE["city"])} {esc(SITE["postal"])}'
    if en:
        c = dict(
            title="Contact Indonesia Yanwoo | WhatsApp, Email, Surabaya Office",
            desc="Contact Indonesia Yanwoo (PT Lentera Alam Nusantara) in Surabaya, Indonesia, by WhatsApp or email for orders, hampers, wholesale and import enquiries.",
            h1="Contact us", lead="The quickest way to reach us is WhatsApp. Tell us where you are and what you need, and our admin will reply.",
            k_wa="WhatsApp", k_mail="Email", k_office="Office", k_ig="Instagram", k_wx="WeChat",
            country="East Java, Indonesia",
            t_h2="What to tell us",
            t=["Which form you want, and how many packs.", "The city in Indonesia where it should be delivered.",
               "Your travel dates, if you are visiting.", "For hampers: the quantity, the budget and the delivery date."],
            i_h2="Importers and wholesalers",
            i_p="Import rules differ from country to country. Tell us your destination and volume, and we will say plainly which forms we can supply and which documents we can provide.",
            b="Message us on WhatsApp",
        )
    else:
        c = dict(
            title="联系我们｜Indonesia Yanwoo 印尼燕窝（WhatsApp、电子邮箱、泗水办公室）",
            desc="联系印尼泗水 Indonesia Yanwoo（PT Lentera Alam Nusantara）：可通过 WhatsApp 或电子邮件咨询订购、礼盒、批发和进口事宜。",
            keywords="印尼燕窝联系方式,印尼燕窝批发,印尼燕窝供应商,泗水燕窝",
            h1="联系我们", lead="最快的联系方式是 WhatsApp。请告诉我们您所在的城市和需要的产品，客服会回复您。",
            k_wa="WhatsApp", k_mail="电子邮箱", k_office="办公地址", k_ig="Instagram", k_wx="微信",
            country="印度尼西亚东爪哇省",
            t_h2="请告诉我们",
            t=["需要哪种形态、多少包。", "收货的印尼城市。", "如果您是来旅游的，请告知行程日期。", "订购礼盒：数量、预算和送达日期。"],
            i_h2="进口商和批发商",
            i_p="各国进口要求不同。请告诉我们目的地和数量，我们会如实说明可以供应的形态和能够提供的文件。",
            b="通过 WhatsApp 联系我们",
        )
    wx = ""
    if SITE["wechat_id"]:
        qr = f'<img class="qr" src="{esc(SITE["wechat_qr"])}" alt="WeChat QR">' if SITE["wechat_qr"] else ""
        wx = f'<li id="wechat"><small>{c["k_wx"]}</small><b>{esc(SITE["wechat_id"])}</b>{qr}</li>'
    ig = (f'<li><small>{c["k_ig"]}</small>{ext("https://www.instagram.com/" + SITE["instagram"] + "/", "@" + esc(SITE["instagram"]))}</li>'
          if SITE["instagram"] else "")
    t = "".join(f"<li>{x}</li>" for x in c["t"])
    body = head(lang, "contact", c["h1"], c["lead"]) + f'''
<section><div class="wrap split" style="align-items:start">
  <ul class="contact-list">
    <li><small>{c["k_wa"]}</small><a href="{wa_link(lang)}" rel="noopener">{esc(SITE["phone"])}</a></li>
    {wx}
    <li><small>{c["k_mail"]}</small><a href="mailto:{esc(SITE["email"])}">{esc(SITE["email"])}</a></li>
    <li><small>{c["k_office"]}</small>{esc(SITE["company"])}<br>{addr}<br>{c["country"]}</li>
    {ig}
  </ul>
  <div class="prose">
    <h2>{c["t_h2"]}</h2>
    <ul>{t}</ul>
    {pay_note(lang)}
    <h2>{c["i_h2"]}</h2>
    <p>{c["i_p"]}</p>
    <div class="btn-row"><a class="btn btn-green" href="{wa_link(lang)}" rel="noopener">{c["b"]}</a></div>
  </div>
</div></section>
'''
    return {"title": c["title"], "desc": c["desc"], "keywords": c.get("keywords", ""), "body": body,
            "jsonld": [crumbs_ld(lang, "contact", label(lang, "contact"))]}


PAGES = {"": home, "products": products, "process": process, "visitors": visitors,
         "bring-home": bring_home, "about": about, "faq": faq, "contact": contact}
