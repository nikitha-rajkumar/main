import json

with open(r'D:\nikitha-portfolio\image_manifest.json') as f:
    images = json.load(f)

# === Remove entire totes category + specific images + duplicates ===
remove_files = {
    'dsc09459.jpg',      # Leather Accessory (slg)
    'dsc08723.jpg',      # Woven Accessory (woven)
    'dsc08514.jpg',      # Embroidered Art Tote (woven)
    'dsc02657-copy.jpg', # Duplicate
    'dsc05754.jpg',      # Leather Messenger (crossbody)
    'dsc05755.jpg',      # Messenger Detail (crossbody)
    'new-folder_dsc09302.jpg',  # Accessory 20 (pouches)
    'new-folder_dsc09303.jpg',  # Accessory 21 (pouches)
    'new-folder_dsc09309.jpg',  # Accessory 22 (pouches)
    'new-folder_dsc09670.jpg',  # Accessory 24 (pouches)
    'new-folder_dsc09672.jpg',  # Accessory 25 (pouches)
    'new-folder_dsc09673.jpg',  # Accessory 26 (pouches)
    'dsc01663.jpg',      # Classic Belt (slg) - removed per merge
    'dsc09843.jpg',      # Travel Bag (utility)
    'dsc07978.jpg',      # Travel Accessory (utility)
    'dsc04361.jpg',      # Organizer Interior (pocket)
}
remove_cats = {'totes'}

# === Reassign to 'lightweight' ===
lightweight_files = {
    'dsc05797.jpg',           # Military Utility Bag (nylon)
    'dsc06126.jpg',           # Tactical Belt Bag (nylon)
    'dsc06128.jpg',           # Belt Bag Detail (nylon)
    'new-folder_dsc06040.jpg',  # Utility Design 10
    'new-folder_dsc06042.jpg',  # Utility Design 11
    'new-folder_dsc06046.jpg',  # Utility Design 12
    'new-folder_dsc06123.jpg',  # Utility Design 13
    'new-folder_dsc06127.jpg',  # Utility Design 14
    'new-folder_dsc06131.jpg',  # Utility Design 15
    'dsc09669.jpg',           # Leather Goods Set
    'new-folder_dsc05667.jpg',  # Shoulder Bag 1
    'new-folder_dsc05670.jpg',  # Shoulder Bag 2
    'new-folder_dsc05682.jpg',  # Shoulder Bag 3
    'new-folder_dsc05684.jpg',  # Shoulder Bag 4
    'new-folder_dsc05746.jpg',  # Shoulder Bag 5
    'new-folder_dsc05747.jpg',  # Shoulder Bag 6
    'new-folder_dsc05756.jpg',  # Shoulder Bag 7
    'new-folder_dsc05799.jpg',  # Shoulder Bag 8
    'new-folder_dsc05800.jpg',  # Shoulder Bag 9
}

# === Reassign to 'pocket' ===
pocket_files = {
    'dsc09630.jpg',   # Mini Crossbody
    'dsc09631.jpg',   # Mini Crossbody Alt
    'dsc09632.jpg',   # Mini Crossbody Detail
    'dsc09633.jpg',   # Mini Crossbody Back
    'dsc02627.jpg',   # Leather Keychain
    'dsc03007.jpg',   # Card Holder
    'dsc02693.jpg',   # Leather Wristlet
    'dsc04356.jpg',   # Leather Organizer (merged from SLG)
}

# === Reassign to 'backpacks' ===
backpack_add_files = {
    'dsc08089.jpg',   # Canvas Pouch Detail
}

# === Reassign to 'pouches' ===
pouches_add_files = {
    'dsc06862.jpg',   # Nylon Duffle
    'dsc08083.jpg',   # Striped Canvas Pouch
}

# === Reassign to 'crossbody' ===
crossbody_add_files = {
    'dsc04373.jpg',   # Compact Wallet
    'dsc07631.jpg',   # Handwoven Piece
    'dsc08167.jpg',   # Textile Tote
    'dsc08194.jpg',   # Craft Bag Detail
}

# === Reassign to 'woven' ===
woven_add_files = {
    'dsc06585.jpg',   # Utility Crossbody
    'dsc07946.jpg',   # Utility Piece
    'dsc07959.jpg',   # Utility Detail
}

# Filter, reassign, and deduplicate
seen_files = set()
filtered = []
for img in images:
    if img['file'] in remove_files:
        continue
    if img['cat'] in remove_cats:
        continue
    if img['file'] in seen_files:
        continue
    seen_files.add(img['file'])
    if img['file'] in lightweight_files:
        img['cat'] = 'lightweight'
    elif img['file'] in pocket_files:
        img['cat'] = 'pocket'
    elif img['file'] in backpack_add_files:
        img['cat'] = 'backpacks'
    elif img['file'] in pouches_add_files:
        img['cat'] = 'pouches'
    elif img['file'] in crossbody_add_files:
        img['cat'] = 'crossbody'
    elif img['file'] in woven_add_files:
        img['cat'] = 'woven'
    filtered.append(img)

images = filtered

# Group by category
cats = {}
for img in images:
    cats.setdefault(img['cat'], []).append(img)

# Swap backpack positions
if 'backpacks' in cats:
    bp = cats['backpacks']
    leather_idx = next((i for i, x in enumerate(bp) if x['file'] == 'dsc04864.jpg'), None)
    black_idx = next((i for i, x in enumerate(bp) if x['file'] == 'dsc06419.jpg'), None)
    if leather_idx is not None and black_idx is not None:
        bp[leather_idx], bp[black_idx] = bp[black_idx], bp[leather_idx]

# Collection configs
collections = [
    ('lightweight', 'Lightweight Styles', '01', 'gallery-grid-3',
     'Effortless ease in every carry. Crafted from technical nylons and organic canvases, these lightweight pieces prove that less weight never means less style.'),
    ('crossbody', 'Crossbody & Shoulder Bags', '02', 'gallery-grid-3',
     'Effortless versatility meets refined craft. These crossbody and shoulder bags are designed for the woman who moves through life with purpose and grace.'),
    ('backpacks', 'Backpacks', '03', 'gallery-editorial',
     'Where utility meets luxury. These backpacks redefine what it means to carry your world, with premium leathers and hardware that age beautifully.'),
    ('pouches', 'Pouches & Clutches', '04', 'gallery-grid-3',
     'The art of restraint. Minimal forms, maximum impact. Each pouch and clutch is crafted to hold what matters most, nothing more.'),
    ('pocket', 'Pocket Accessories & Small Leather Goods', '05', 'gallery-grid-2',
     'Small in scale, bold in detail. From card holders to compact wallets and leather organizers, these pocket-sized essentials are designed with the same precision and craft as our signature pieces.'),
    ('woven', 'Woven & Textile', '06', 'gallery-artisan',
     'Hands that weave stories. Celebrating traditional textile craft through contemporary design, each piece bridges cultures and generations.'),
    ('utility', 'Utility & Travel', '07', 'gallery-bold',
     'Function at its finest. Military-inspired utility meets contemporary design in this collection of bags built for modern life on the move.'),
]

def gallery_items(cat_key):
    items = cats.get(cat_key, [])
    html = ''
    for img in items:
        html += f'''                <div class="gallery-item" data-cat="{img['cat']}">
                    <img src="images/projects/{img['file']}" alt="{img['name']}" loading="lazy">
                    <div class="item-overlay">
                        <h4>{img['name']}</h4>
                        <p>{img['desc']}</p>
                    </div>
                </div>
'''
    return html

def collection_section(cat_key, title, num, layout, intro):
    items_html = gallery_items(cat_key)
    count = len(cats.get(cat_key, []))
    return f'''
    <!-- Collection: {title} -->
    <section class="collection-section" id="collection-{cat_key}" style="overflow:visible">
        <div class="collection-header reveal">
            <span class="collection-number">{num}</span>
            <h2 class="collection-title">{title}</h2>
            <p class="collection-intro">{intro}</p>
            <span class="collection-count">{count} pieces</span>
        </div>
        <div class="{layout}">
{items_html}        </div>
    </section>
'''

collections_html = ''
for c in collections:
    collections_html += collection_section(*c)

html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Nikitha Rajkumar | Bag, Accessory & Apparel Designer</title>
    <meta name="description" content="Portfolio of Nikitha Rajkumar - Bag, Accessory & Apparel Designer. NIFT Chennai graduate specializing in leather goods, bags, and textile accessories.">
    <link rel="stylesheet" href="css/style.css">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@300;400;500;600;700&family=Playfair+Display:ital,wght@0,400;0,500;0,600;0,700;0,800;1,400;1,500;1,600&family=Outfit:wght@200;300;400;500;600;700&family=Space+Grotesk:wght@300;400;500;600;700&display=swap" rel="stylesheet">
</head>
<body>
    <!-- Grain Overlay -->
    <div class="grain-overlay"></div>

    <!-- Navigation -->
    <nav class="nav" id="nav">
        <a href="#hero" class="nav-brand">NR</a>
        <div class="nav-links" id="navLinks">
            <a href="#hero" class="nav-link">Home</a>
            <a href="#about" class="nav-link">About</a>
            <a href="#experience" class="nav-link">Experience</a>
            <a href="#collections" class="nav-link">Collections</a>
            <a href="#contact" class="nav-link">Contact</a>
        </div>
        <button class="nav-toggle" id="navToggle" aria-label="Menu">
            <span></span><span></span><span></span>
        </button>
    </nav>

    <!-- Hero -->
    <section class="hero" id="hero">
        <div class="hero-content">
            <div class="hero-text">
                <h1 class="hero-name reveal">Nikitha<br>Rajkumar</h1>
                <p class="hero-designer-title reveal">Fashion & Lifestyle Accessory Designer</p>
                <div class="hero-cta reveal">
                    <a href="#collections" class="btn-primary">View Collection</a>
                    <a href="#contact" class="btn-outline">Get in Touch</a>
                </div>
            </div>
            <div class="hero-profile reveal">
                <img src="images/profile/photo_Nikki.jpeg" alt="Nikitha Rajkumar">
            </div>
        </div>
        <div class="hero-stats">
            <div class="stat reveal">
                <span class="stat-number" data-count="3.5">0</span><span class="stat-plus">+</span>
                <span class="stat-label">Years Experience</span>
            </div>
            <div class="stat reveal">
                <span class="stat-number" data-count="15">0</span><span class="stat-plus">+</span>
                <span class="stat-label">Brands Collaborated</span>
            </div>
            <div class="stat reveal">
                <span class="stat-number" data-count="100">0</span><span class="stat-plus">+</span>
                <span class="stat-label">Products Designed & Developed</span>
            </div>
        </div>
        <div class="scroll-arrow">
            <span>Scroll to explore</span>
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M12 5v14M5 12l7 7 7-7"/></svg>
        </div>
    </section>

    <!-- About -->
    <section class="about-section" id="about" style="overflow:visible">
        <div class="about-grid">
            <div class="about-text">
                <p class="about-intro reveal">"Design, for me, begins where function meets form."</p>
                <p class="reveal">With a foundation in product development, I translate ideas into thoughtfully engineered products that are not only visually compelling but also built for real use. My work is driven by material exploration, construction detailing, and a constant pursuit of balance between performance, durability, and aesthetics.</p>
                <p class="reveal">Inspired by movement, travel, and everyday utility &mdash; I create products that are purposeful, user-centric, and commercially relevant. With a Bachelor&rsquo;s in Design from the National Institute of Fashion Technology, Chennai, I specialize in creating accessories that tell stories through material, form, and function.</p>
            </div>
            <div class="about-skills">
                <h3 class="reveal">Expertise</h3>
                <div class="skills-list">
                    <span class="skill-tag reveal">Product Development</span>
                    <span class="skill-tag reveal">Trend Forecasting</span>
                    <span class="skill-tag reveal">3D Modeling (CLO)</span>
                    <span class="skill-tag reveal">Tech Pack Creation</span>
                    <span class="skill-tag reveal">WGSN Analytics</span>
                    <span class="skill-tag reveal">Adobe Illustrator</span>
                    <span class="skill-tag reveal">Adobe Photoshop</span>
                    <span class="skill-tag reveal">Material Research</span>
                    <span class="skill-tag reveal">Cross-functional Coordination</span>
                    <span class="skill-tag reveal">Collection Development</span>
                </div>
            </div>
        </div>
    </section>

    <!-- Experience -->
    <section class="experience-section" id="experience" style="overflow:visible">
        <div class="section-inner">
            <h2 class="section-heading reveal">Experience</h2>
            <div class="timeline">
                <div class="timeline-item reveal">
                    <div class="timeline-dot"></div>
                    <div class="timeline-content">
                        <span class="timeline-period">2023 &mdash; Present</span>
                        <h3 class="timeline-role">Brand Product Developer</h3>
                        <p class="timeline-company">Bhartiya Fashion International</p>
                        <ul class="timeline-details">
                            <li>Decode tech packs and comprehend client design expectations and material/functionality requirements</li>
                            <li>Skilled in trend tracking to offer client-relevant and market-aligned collections</li>
                            <li>Cross-functionally coordinate with multiple teams to maintain timely deliveries</li>
                            <li>Leverage WGSN trend forecasting tools to analyze market movements</li>
                            <li>Experience in 3D modeling for lifestyle and consumer products</li>
                        </ul>
                    </div>
                </div>
                <div class="timeline-item reveal">
                    <div class="timeline-dot"></div>
                    <div class="timeline-content">
                        <span class="timeline-period">2022 &mdash; 2023</span>
                        <h3 class="timeline-role">Product Designer</h3>
                        <p class="timeline-company">Corvo</p>
                        <ul class="timeline-details">
                            <li>Designed and developed lifestyle accessory collections from concept to production</li>
                            <li>Created detailed tech packs and material specifications for manufacturing</li>
                            <li>Collaborated with artisans and production teams to ensure design integrity</li>
                        </ul>
                    </div>
                </div>
                <div class="timeline-item reveal">
                    <div class="timeline-dot"></div>
                    <div class="timeline-content">
                        <span class="timeline-period">Internship</span>
                        <h3 class="timeline-role">Design Intern</h3>
                        <p class="timeline-company">Ciel Groups (Apparel)</p>
                        <ul class="timeline-details">
                            <li>Gained hands-on experience in apparel design and production workflows</li>
                            <li>Assisted senior designers in collection development and trend research</li>
                        </ul>
                    </div>
                </div>
            </div>
            <div class="education-row reveal">
                <div class="edu-card">
                    <h4>Bachelor of Design (B.Des)</h4>
                    <p>National Institute of Fashion Technology, Chennai</p>
                    <p><strong>Major:</strong> Fashion & Lifestyle Accessory Design &bull; <strong>Minor:</strong> Fashion Design</p>
                    <span class="timeline-period">2018 &mdash; 2022</span>
                </div>
                <div class="edu-card">
                    <h4>Higher Secondary (12th)</h4>
                    <p>Equitas School</p>
                    <span class="timeline-period">2018</span>
                </div>
                <div class="edu-card">
                    <h4>Secondary School (10th)</h4>
                    <p>R. S. Krishnan Higher Secondary School</p>
                    <span class="timeline-period">2015</span>
                </div>
            </div>
        </div>
    </section>

    <!-- Collections Anchor -->
    <div id="collections"></div>
{collections_html}
    <!-- Project: Travel & Outdoor Gear -->
    <section class="project-showcase" id="project-travel" style="overflow:visible">
        <div class="collection-header reveal">
            <span class="collection-number">P1</span>
            <h2 class="collection-title">Travel & Outdoor Gear</h2>
            <p class="collection-intro">A comprehensive design exploration of travel and outdoor gear &mdash; from concept sketches to material specifications. Swipe through the presentation to see the full design process.</p>
            <span class="collection-count">69 pages</span>
        </div>
        <div class="pdf-carousel" id="pdfCarousel">
            <div class="pdf-carousel-track" id="pdfTrack">
''' + ''.join([f'                <div class="pdf-slide"><img src="assets/travel-page-{i:02d}.jpg" alt="Travel & Outdoor Gear - Page {i}" loading="lazy"></div>\n' for i in range(1, 70)]) + f'''            </div>
            <button class="pdf-nav pdf-prev" id="pdfPrev">&#8249;</button>
            <button class="pdf-nav pdf-next" id="pdfNext">&#8250;</button>
            <div class="pdf-counter">
                <span id="pdfCurrent">1</span> / 69
            </div>
        </div>
    </section>

    <!-- Lightbox -->
    <div class="lightbox" id="lightbox">
        <button class="lightbox-close" id="lightboxClose">&times;</button>
        <button class="lightbox-nav lightbox-prev" id="lightboxPrev">&#8249;</button>
        <button class="lightbox-nav lightbox-next" id="lightboxNext">&#8250;</button>
        <div class="lightbox-content">
            <img src="" alt="" class="lightbox-img" id="lightboxImg">
            <div class="lightbox-info">
                <h4 id="lightboxTitle"></h4>
                <p id="lightboxDesc"></p>
                <span class="lightbox-counter" id="lightboxCounter"></span>
            </div>
        </div>
    </div>

    <!-- Contact -->
    <section class="contact-section" id="contact" style="overflow:visible">
        <div class="section-inner">
            <h2 class="section-heading reveal">Let's Connect</h2>
            <p class="contact-intro reveal">Interested in collaborating or discussing a project? Let's create something extraordinary together.</p>
            <div class="contact-grid">
                <a href="mailto:nikitharahul1519@gmail.com" class="contact-card reveal">
                    <div class="contact-icon">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/><polyline points="22,6 12,13 2,6"/></svg>
                    </div>
                    <span class="contact-label">Email</span>
                    <span class="contact-value">nikitharahul1519@gmail.com</span>
                </a>
                <a href="tel:+919500977949" class="contact-card reveal">
                    <div class="contact-icon">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.13.88.37 1.73.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c1.08.33 1.93.57 2.81.7A2 2 0 0 1 22 16.92z"/></svg>
                    </div>
                    <span class="contact-label">Phone</span>
                    <span class="contact-value">+91 9500977949</span>
                </a>
                <a href="https://www.linkedin.com/in/nikitha-rajkumar-326317208" target="_blank" rel="noopener" class="contact-card reveal">
                    <div class="contact-icon">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M16 8a6 6 0 0 1 6 6v7h-4v-7a2 2 0 0 0-4 0v7h-4v-7a6 6 0 0 1 6-6z"/><rect x="2" y="9" width="4" height="12"/><circle cx="4" cy="4" r="2"/></svg>
                    </div>
                    <span class="contact-label">LinkedIn</span>
                    <span class="contact-value">Connect on LinkedIn</span>
                </a>
                <div class="contact-card reveal">
                    <div class="contact-icon">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg>
                    </div>
                    <span class="contact-label">Location</span>
                    <span class="contact-value">Chennai, India</span>
                </div>
                <a href="assets/Nikitha-Rajkumar-Resume.pdf" target="_blank" class="contact-card reveal">
                    <div class="contact-icon">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/><polyline points="10 9 9 9 8 9"/></svg>
                    </div>
                    <span class="contact-label">Resume</span>
                    <span class="contact-value">Preview Resume</span>
                </a>
                <a href="assets/Nikitha-Rajkumar-Resume.pdf" download class="contact-card reveal">
                    <div class="contact-icon">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>
                    </div>
                    <span class="contact-label">Resume</span>
                    <span class="contact-value">Download PDF</span>
                </a>
            </div>
        </div>
    </section>

    <!-- Footer -->
    <footer class="footer">
        <div class="footer-content">
            <span class="footer-name">Nikitha Rajkumar</span>
            <span class="footer-tagline">Fashion & Lifestyle Accessory Designer</span>
            <p>&copy; 2026 Nikitha Rajkumar. All rights reserved.</p>
        </div>
    </footer>

    <!-- Back to Top -->
    <button class="back-to-top" id="backToTop" aria-label="Back to top">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 19V5M5 12l7-7 7 7"/></svg>
    </button>

    <script src="js/main.js"></script>
</body>
</html>'''

with open(r'D:\nikitha-portfolio\index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print(f'HTML written: {len(html)} chars, {html.count(chr(10))} lines')
print(f'Collections: {len(collections)}')
for cat_key, title, *_ in collections:
    print(f'  {title}: {len(cats.get(cat_key, []))} images')
print(f'Total images: {len(images)}')
