import re
import shutil

with open('index-original.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Remove window.CHART_IMAGES
content = re.sub(r"window\.CHART_IMAGES\s*=\s*\{\s*OMDB:\s*'[^']+'\s*\};\n*", "", content)

# 2. Remove const AIRPORTS
content = re.sub(r"const AIRPORTS\s*=\s*\{.*?\};\n*(?=(// ====))", "", content, flags=re.DOTALL)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Restored and cleaned index.html")
