import os

for filename in ["support.html", "mid.html", "jungle.html", "adcarry.html"]:
    filepath = f"/workspace/{filename}"
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Replace the incorrectly indented nav with proper indentation
    old_nav = '        <nav>\n        <div class="logo">🎮 荣耀<span>教学</span></div>\n        <ul class="nav-links">'
    new_nav = '    <nav>\n        <div class="logo">🎮 荣耀<span>教学</span></div>\n        <ul class="nav-links">'
    content = content.replace(old_nav, new_nav)
    
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    
    print(f"Fixed whitespace in {filename}")
