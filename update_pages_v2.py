import os

# Read reference index.html
with open("/workspace/index.html", "r", encoding="utf-8") as f:
    index_html = f.read()


def process_page(filename, theme_accent):
    print(f"Processing {filename}...")

    # Read original file
    with open(f"/workspace/{filename}", "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Replace inline styles with link to styles.css
    # Remove entire <style>...</style> block
    import re
    content = re.sub(r"<style>.*?</style>", "", content, flags=re.DOTALL)
    # Insert styles.css link after font link
    font_link = '<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@300;400;500;700;900&display=swap" rel="stylesheet">'
    content = content.replace(
        font_link,
        font_link + '\n    <link rel="stylesheet" href="css/styles.css">',
    )

    # 2. Replace the entire nav/mobile-nav section with the correct one
    # First, find where the nav ends and mobile nav is
    # We'll just replace everything from <nav> to after </div> (mobile nav)
    # Wait, better to build the new content properly
    new_nav_section = '''    <nav>
        <div class="logo">🎮 荣耀<span>教学</span></div>
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

    # Replace old nav with new one
    # First, remove the old nav by finding from <nav> to first <main>
    nav_start = content.find("<nav>")
    main_start = content.find("<main>")
    if nav_start != -1 and main_start != -1:
        content = content[:nav_start] + new_nav_section + content[main_start:]

    # 3. Add/ensure back-to-top button and script.js
    # Ensure back-to-top button is before </body>
    back_to_top_btn = f'''    <button class="back-to-top{' back-' + theme_accent if theme_accent != 'support' else ''}" id="backToTop" aria-label="回到顶部">
        ↑
    </button>'''

    if "back-to-top" in content:
        # Replace existing back-to-top
        content = re.sub(
            r'<button class="back-to-top.*?</button>',
            back_to_top_btn,
            content,
            flags=re.DOTALL,
        )
    else:
        # Insert before </body>
        content = content.replace("</body>", back_to_top_btn + "\n</body>")

    # Ensure script.js is included
    script_tag = '    <script src="js/script.js"></script>'
    if "script.js" not in content:
        content = content.replace("</body>", script_tag + "\n</body>")
    else:
        # Remove any inline scripts
        content = re.sub(r"<script>(?!.*script\.js).*?</script>", "", content, flags=re.DOTALL)

    # 4. Add theme-specific classes (hero, badge, section-intro)
    if theme_accent != "support":
        # Update hero class
        content = content.replace('class="hero"', f'class="hero hero-{theme_accent}"')
        # Update badge class
        content = content.replace(
            'class="hero-badge"', f'class="hero-badge badge-{theme_accent}"'
        )
        # Update section-intro
        content = content.replace(
            'class="section-intro"', f'class="section-intro intro-{theme_accent}"'
        )

    # Write updated content back
    with open(f"/workspace/{filename}", "w", encoding="utf-8") as f:
        f.write(content)

    print(f"Successfully processed {filename}")


# Process all four pages!
process_page("support.html", "support")
process_page("mid.html", "mid")
process_page("jungle.html", "jungle")
process_page("adcarry.html", "adcarry")

print("All pages updated perfectly!")
