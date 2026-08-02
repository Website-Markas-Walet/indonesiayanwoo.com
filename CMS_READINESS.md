---
site: indonesiayanwoo.com
deploy: { host: github_pages, cf_account: null, branch: master, deploy_hook: absent }
url_patterns: { artikel: "/{slug}.html", kota: "/kota/jual-sarang-walet-di-{kota}.html", page: "/{path}/ (folder, no .html)", desain: "/desain/{slug} (folder, no .html)" }
chrome: { header_lines: "~4360-5030 (~670 lines, before id=content)", footer_lines: "~5472-5643 (~171 lines, footer id=colophon)", byte_identical: "header:true, footer:variants (per-page trailing scripts)" }
analytics: { gtm: "GTM-PD93KSR", ga4_property_id: "", tiktok: "CJA4IDBC77U5K7SPBH0G", fb_verify: "", adsense: "" }
brand: { primary: "#ffd936", font: "DM Sans (400,700) + Forum (400)", logo: "/wp-content/uploads/2023/03/LOGO-INDONESIA-YANWOO-HITAM-*", favicon: "LOGO-INDONESIA-YANWOO-HITAM-FAVICON-Copy-{32,180,192}.png" }
ecosystem_menu: absent
contact: { wa: "6287725260196", email: "" }
media: { local_mb: 88, hotlink: "blogspot:392, hatena:159, other:24, self:11" }
content: { articles: 194, kota_unique: 489, kota_admin_level: kota }
cleanup: ["nojekyll_missing", "hotlink_images_551_external", "mixed_url_scheme", "inline_css_bloat_60pct", "footer_not_pure_chrome"]
blockers: ["write_access_denied_403", "header_menu_scope_3_vs_5", "contact_incomplete"]
---

## Catatan — indonesiayanwoo.com

**Deploy:** GitHub Pages murni. Push ke `master` (root) = langsung live, Pages auto-rebuild, tanpa Action/Deploy Hook. Branch produksi = `master` (bukan `main`). Wajib tambah `.nojekyll` sebelum CMS commit.

**Akses tulis (blocker utama):** git push proxy dan GitHub App API keduanya balas 403. Baca OK, tulis DITOLAK. CMS butuh GitHub App org-level, Contents:write, installation token pendek. Commit ke `master` -> Pages rebuild sendiri.

**Chrome:** header byte-identik di seluruh halaman (aman jadi 1 template). Footer visual konsisten, tapi region setelah </footer> berisi script per-halaman. Potong slot di id=content dan footer id=colophon, sisipkan CONTENT. Menu header 3 item (Home/Produk/Blog), footer 5 item.

**Konten:** 194 artikel + 489 kota (level kota) + 10 page + 5 desain. Kota = 1 template + dataset 489 kota. Total ~698 halaman SEO.

**Media:** 88 MB lokal. Gambar artikel mayoritas hotlink eksternal (blogspot 392, hatena 159). Prioritas rehome ke R2.

**URL sakral:** jangan ubah slug/skema tanpa 301.
