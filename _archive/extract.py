import re
import json
import base64
import os

html_file = 'index.html'
with open(html_file, 'r', encoding='utf-8') as f:
    content = f.read()

# Extract chart image
img_match = re.search(r'window\.CHART_IMAGES\s*=\s*\{\s*OMDB:\s*\'([^\']+)\'\s*\}', content)
if img_match:
    img_data = img_match.group(1)
    if ',' in img_data:
        img_data = img_data.split(',', 1)[-1]
    os.makedirs('airports/OMDB', exist_ok=True)
    with open('airports/OMDB/chart.jpg', 'wb') as f:
        f.write(base64.b64decode(img_data))
    print("Chart extracted")

# Extract taxiways. We know window.AIRPORTS contains valid JS which may not be strict JSON.
# Instead of regex parsing JS to JSON (which is fragile due to missing quotes on keys), 
# let's just run a tiny node script to stringify it.
