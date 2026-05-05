#!/usr/bin/env python3
from pathlib import Path

def main():
    pages = [
        {
            'file': 'support.html',
            'logo': '王者<span>辅助</span>教学',
            'hero_class': 'hero-support',
            'theme': 'support'
        },
        {
            'file': 'mid.html',
            'logo': '🎮 荣耀<span>教学</span>',
            'hero_class': 'hero-mid',
            'theme': 'mid'
        },
        {
            'file': 'jungle.html',
            'logo': '🎮 荣耀<span>教学</span>',
            'hero_class': 'hero-jungle',
            'theme': 'jungle'
        },
        {
            'file': 'adcarry.html',
            'logo': '🎮 荣耀<span>教学</span>',
            'hero_class': 'hero-adc',
            'theme': 'adc'
        }
    ]
    
    for page in pages:
        file_path = Path('/workspace') / page['file']
        print(f"Processing {page['file']}...")
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Step 1: Replace <style>...</style> with the stylesheet link
        style_start = content.find('<style>')
        style_end = content.find('</style>')
        if style_start != -1 and style_end != -1:
            before_style = content[:style_start]
            after_style = content[style_end + 8:]
            content = before_style + '    <link rel="stylesheet" href="css/styles.css">\n' + after_style
        
        # Step 2: Update the nav
        nav_start = content.find('<nav>')
        nav_end = content.find('</nav>', nav_start) + 6
        if nav_start != -1:
            # Extract the original nav links
            original_nav = content[nav_start:nav_end]
            # Find the nav-links ul
            nav_links_start = original_nav.find('<ul class="nav-links">')
            nav_links_end = original_nav.find('</ul>', nav_links_start) + 5
            original_nav_links = original_nav[nav_links_start:nav_links_end]
            
            # For support.html, we keep the original links; for others, add the index link if not present
            if page['file'] != 'support.html' and 'index.html' not in original_nav_links:
                # Prepend the index link to the existing links
                original_nav_links = original_nav_links.replace('<ul class="nav-links">', '<ul class="nav-links">\n            <li><a href="index.html">← 返回首页</a></li>')
            
            # Build the new nav
            new_nav = f'''    <nav>
        <div class="logo" onclick="window.scrollTo({{top: 0, behavior: 'smooth'}})">
            {page['logo']}
        </div>
        {original_nav_links}
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
                back_to_top = '''

    <button class="back-to-top" id="backToTop" aria-label="回到顶部">
        ↑
    </button>'''
                footer_end = content.find('</footer>', footer_start) + 9
                content = content[:footer_end] + back_to_top + content[footer_end:]
        
        # Step 5: Replace inline script with script.js link
        script_start = content.find('<script>')
        if script_start != -1:
            script_end = content.find('</script>', script_start) + 9
            content = content[:script_start] + '    <script src="js/script.js"></script>\n' + content[script_end:]
        else:
            body_end = content.find('</body>')
            if body_end != -1:
                content = content[:body_end] + '    <script src="js/script.js"></script>\n' + content[body_end:]
        
        # Step 6: Fix indentation
        # Simple indentation fix: remove extra leading spaces but keep structure
        lines = content.split('\n')
        fixed_lines = []
        for line in lines:
            # If line starts with too many spaces, normalize
            if line.startswith('        '):
                fixed_lines.append(line[4:])
            elif line.startswith('    '):
                fixed_lines.append(line)
            else:
                fixed_lines.append(line)
        content = '\n'.join(fixed_lines)
        
        # Write back
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✓ Done with {page['file']}")

if __name__ == "__main__":
    main()
