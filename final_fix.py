#!/usr/bin/env python3
import os

pages = [
    {
        "file": "support.html",
        "nav_links": [
            ("#intro", "辅助干啥"),
            ("#opening", "开局咋玩"),
            ("#roam", "游走支援"),
            ("#teamfight", "团战站位"),
            ("#priority", "保护谁"),
            ("#vision", "做视野"),
            ("#types", "辅助类型"),
            ("#mistakes", "常见坑"),
            ("#growth", "怎么变强"),
        ],
        "badge_class": "",
        "btn_class": "",
        "back_class": "",
        "hero_class": "hero-support"
    },
    {
        "file": "mid.html",
        "nav_links": [],
        "badge_class": "badge-mid",
        "btn_class": "btn-mid",
        "back_class": "back-mid",
        "hero_class": "hero-mid"
    },
    {
        "file": "jungle.html",
        "nav_links": [],
        "badge_class": "badge-jungle",
        "btn_class": "btn-jungle",
        "back_class": "back-jungle",
        "hero_class": "hero-jungle"
    },
    {
        "file": "adcarry.html",
        "nav_links": [],
        "badge_class": "badge-adcarry",
        "btn_class": "btn-adcarry",
        "back_class": "back-adcarry",
        "hero_class": "hero-adcarry"
    }
]

for page in pages:
    file_path = os.path.join("/workspace", page["file"])
    print(f"Processing {page['file']}...")
    
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Fix adcarry hero class (just in case)
    if page["file"] == "adcarry.html":
        content = content.replace("hero-adc", "hero-adcarry")
    
    # Ensure hero has correct class
    hero_class = page["hero_class"]
    if hero_class and hero_class not in content:
        content = content.replace('class="hero"', f'class="hero {hero_class}"')
    
    # Add badge class
    if page["badge_class"]:
        content = content.replace('class="hero-badge"', f'class="hero-badge {page["badge_class"]}"')
    # Special case for support.html, no badge class but let's add hero-support theme
    if page["file"] == "support.html":
        content = content.replace('class="hero-badge"', 'class="hero-badge"')
    
    # Add btn class
    if page["btn_class"]:
        content = content.replace('class="btn btn-primary"', f'class="btn btn-primary {page["btn_class"]}"')
    
    # Add back-to-top class
    if page["back_class"]:
        content = content.replace('class="back-to-top"', f'class="back-to-top {page["back_class"]}"')
    
    # Update mobile-nav with all nav links
    nav_html = '<a href="index.html">← 返回首页</a>'
    if page["nav_links"]:
        for href, text in page["nav_links"]:
            nav_html += f'\n    <a href="{href}">{text}</a>'
    
    # Find and replace mobile-nav
    import re
    mobile_nav_pattern = r'<div class="mobile-nav" id="mobileNav">.*?</div>'
    replacement = f'<div class="mobile-nav" id="mobileNav">\n    {nav_html}\n    </div>'
    content = re.sub(mobile_nav_pattern, replacement, content, flags=re.DOTALL)
    
    # Fix support.html nav-links indentation and add home link
    if page["file"] == "support.html":
        # Ensure nav-links has home link at start
        nav_links_pattern = r'<ul class="nav-links">.*?</ul>'
        nav_links_content = '<li><a href="index.html">← 返回首页</a></li>\n        '
        for href, text in page["nav_links"]:
            nav_links_content += f'<li><a href="{href}">{text}</a></li>\n        '
        nav_links_content = nav_links_content.rstrip()
        
        replacement_nav_links = f'<ul class="nav-links">{nav_links_content}</ul>'
        content = re.sub(nav_links_pattern, replacement_nav_links, content, flags=re.DOTALL)
    
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    
    print(f"✓ Done with {page['file']}")

print("\nAll files processed successfully!")
