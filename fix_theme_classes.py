import os

def fix_file(filename, theme):
    with open(f"/workspace/{filename}", "r", encoding="utf-8") as f:
        content = f.read()
    
    # Fix hero class
    content = content.replace(f'class="hero" hero-{theme}', f'class="hero hero-{theme}"')
    
    # Fix badge (there was a bug where it was "@ badge-mid橘落")
    content = content.replace(f'@ badge-{theme}橘落', f'@归橘落')
    
    # Fix badge class if needed
    content = content.replace(f'class="hero-badge" badge-{theme}', f'class="hero-badge badge-{theme}"')
    
    # Fix back-to-top button
    content = content.replace(f'class="back-to-top" back-{theme}', f'class="back-to-top back-{theme}"')
    
    # Fix section-intro
    content = content.replace(f'class="section-intro" intro-{theme}', f'class="section-intro intro-{theme}"')
    
    with open(f"/workspace/{filename}", "w", encoding="utf-8") as f:
        f.write(content)
    
    print(f"Fixed {filename}")

fix_file("mid.html", "mid")
fix_file("jungle.html", "jungle")
fix_file("adcarry.html", "adcarry")
