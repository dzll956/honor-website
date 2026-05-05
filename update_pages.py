#!/usr/bin/env python3
import os
from pathlib import Path

def update_html_file(file_path, accent_color, light_accent, theme_class, page_title, hero_text):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace the <style> section with link to css/styles.css
    start_style = content.find('<style>')
    end_style = content.find('</style>') + 8
    new_head = content[:start_style] + '    <link rel="stylesheet" href="css/styles.css">'
    content = new_head + content[end_style:]
    
    # Update the navigation
    if '<nav>' in content:
            # Replace logo and add mobile menu
            nav_start = content.find('<nav>')
            nav_end = content.find('</nav>', nav_start) + 7
            new_nav = '''    <nav>
        <div class="logo" onclick="window.scrollTo({top: 0, behavior: 'smooth'})">
            🎮 荣耀<span>教学</span>
        </div>
        <ul class="nav-links">
            <li><a href="index.html">← 返回首页</a></li>
        </ul>
        <button class="mobile-menu-btn" id="mobileMenuBtn" aria-label="菜单">
            <span></span>
            <span></span>
            <span></span>
        </button>
    </nav>

    <div class="mobile-nav" id="mobileNav">
        <a href="index.html">← 返回首页</a>
    </div>'''
            content = content[:nav_start] + new_nav + content[nav_end:]
    
    # Update hero section with theme class
    content = content.replace('<section class="hero">', f'<section class="hero hero-{theme_class}">')
    
    # Add back-to-top button if not present
    if 'back-to-top' not in content:
        footer_end = content.find('</footer>') + 9
        back_to_top = '''

    <button class="back-to-top" id="backToTop" aria-label="回到顶部">
        ↑
    </button>'''
        content = content[:footer_end] + back_to_top + content[footer_end:]
    
    # Replace inline script with link to js/script.js
    if '<script>' in content:
        script_start = content.find('<script>')
        script_end = content.find('</script>', script_start) + 9
        content = content[:script_start] + '    <script src="js/script.js"></script>' + content[script_end:]
    else:
        # If no script, add it before </body>
        body_end = content.find('</body>')
        content = content[:body_end] + '    <script src="js/script.js"></script>\n' + content[body_end:]
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

def main():
    pages = [
        {
            'file': 'support.html',
            'accent': 'var(--accent)',
            'light_accent': 'var(--accent-light)',
            'theme_class': 'support',
            'page_title': '王者荣耀 - 辅助意识教学',
            'hero_text': '王者荣耀\n                    <span class="highlight">辅助意识教学</span>'
        },
        {
            'file': 'mid.html',
            'accent': 'var(--blue)',
            'light_accent': 'var(--blue-light)',
            'theme_class': 'mid',
            'page_title': '王者荣耀 - 中路法师教学',
            'hero_text': '中路<span class="highlight">法师</span>教学'
        },
        {
            'file': 'jungle.html',
            'accent': 'var(--purple)',
            'light_accent': 'var(--purple-light)',
            'theme_class': 'jungle',
            'page_title': '王者荣耀 - 打野节奏教学',
            'hero_text': '王者荣耀\n                    <span class="highlight">打野教学</span>'
        },
        {
            'file': 'adcarry.html',
            'accent': 'var(--gold)',
            'light_accent': 'var(--gold-light)',
            'theme_class': 'adc',
            'page_title': '王者荣耀 - 射手输出教学',
            'hero_text': '王者荣耀\n                    <span class="highlight">射手教学</span>'
        }
    ]
    
    for page in pages:
        file_path = Path('/workspace') / page['file']
        if file_path.exists():
            print(f"Updating {page['file']}...")
            update_html_file(str(file_path), page['accent'], page['light_accent'], page['theme_class'], page['page_title'], page['hero_text'])
            print(f"Done updating {page['file']}")
        else:
            print(f"Warning: {page['file']} not found!")

if __name__ == "__main__":
    main()
