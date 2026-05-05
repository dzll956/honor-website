#!/usr/bin/env python3
import re
from pathlib import Path

def main():
    pages = [
        {
            'file': 'support.html',
            'accent': 'var(--accent)',
            'hero_class': 'hero-support',
            'theme': 'support'
        },
        {
            'file': 'mid.html',
            'accent': 'var(--blue)',
            'hero_class': 'hero-mid',
            'theme': 'mid'
        },
        {
            'file': 'jungle.html',
            'accent': 'var(--purple)',
            'hero_class': 'hero-jungle',
            'theme': 'jungle'
        },
        {
            'file': 'adcarry.html',
            'accent': 'var(--gold)',
            'hero_class': 'hero-adc',
            'theme': 'adc'
        }
    ]
    
    for page in pages:
        file_path = Path('/workspace') / page['file']
        print(f"Processing {page['file']}...")
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Step 1: Replace <style>...</style> with <link rel="stylesheet" href="css/styles.css">
        # Keep the Google Font link
        style_start = content.find('<style>')
        style_end = content.find('</style>')
        if style_start != -1 and style_end != -1:
            # Find the position after the Google Font link
            google_font_end = content.find('</link>', style_start - 200)
            if google_font_end == -1:
                google_font_end = content.find('">', style_start - 100) + 2
            before_style = content[:style_start]
            after_style = content[style_end + 8:]
            # Insert the stylesheet link
            content = before_style + '    <link rel="stylesheet" href="css/styles.css">\n' + after_style
        
        # Step 2: Update the navigation
        # Replace the old nav with the new one that has mobile menu
        nav_start = content.find('<nav>')
        nav_end = content.find('</nav>', nav_start) + 6
        if nav_start != -1:
            # For support.html, keep the logo text "王者辅助教学"
            if page['file'] == 'support.html':
                logo_text = '王者<span>辅助</span>教学'
            else:
                logo_text = '🎮 荣耀<span>教学</span>'
            
            new_nav = f'''    <nav>
        <div class="logo" onclick="window.scrollTo({{top: 0, behavior: 'smooth'}})">
            {logo_text}
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
        
        # Step 3: Update hero class
        content = content.replace('<section class="hero">', f'<section class="hero {page["hero_class"]}">')
        
        # Step 4: Add back-to-top button if not present
        if 'back-to-top' not in content:
            footer_start = content.find('<footer>')
            if footer_start != -1:
                back_to_top_btn = '''

    <button class="back-to-top" id="backToTop" aria-label="回到顶部">
        ↑
    </button>'''
                footer_end = content.find('</footer>', footer_start) + 9
                content = content[:footer_end] + back_to_top_btn + content[footer_end:]
        
        # Step 5: Replace inline script with <script src="js/script.js"></script>
        script_start = content.find('<script>')
        if script_start != -1:
            script_end = content.find('</script>', script_start) + 9
            content = content[:script_start] + '    <script src="js/script.js"></script>\n' + content[script_end:]
        else:
            # Add script before </body>
            body_end = content.find('</body>')
            if body_end != -1:
                content = content[:body_end] + '    <script src="js/script.js"></script>\n' + content[body_end:]
        
        # Write back
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✓ Done processing {page['file']}")

if __name__ == "__main__":
    main()
