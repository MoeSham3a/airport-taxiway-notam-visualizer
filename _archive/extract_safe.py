import re, json, base64, os

with open('index-original.html', 'r', encoding='utf-8') as f:
    content = f.read()

os.makedirs('airports/OMDB', exist_ok=True)

# 1. Extract Chart
img_match = re.search(r"window\.CHART_IMAGES\s*=\s*\{\s*OMDB:\s*'([^']+)'\s*\}", content)
if img_match:
    img_data = img_match.group(1)
    if ',' in img_data:
        img_data = img_data.split(',', 1)[-1]
    with open('airports/OMDB/chart.jpg', 'wb') as f:
        f.write(base64.b64decode(img_data))
    print("Extracted chart.jpg")

# 2. Extract Taxiways
# window.AIRPORTS = { ... };
twy_match = re.search(r"window\.AIRPORTS\s*=\s*(\{.*?\});\s*// ====", content, re.DOTALL)
if twy_match:
    twy_str = twy_match.group(1)
    # the string is: { OMDB: { taxiways: { ... } } }
    # clean comments
    twy_str = re.sub(r'//.*?\n', '\n', twy_str)
    # quote unquoted keys
    twy_str = re.sub(r'([{,]\s*)([a-zA-Z0-9_]+)\s*:', r'\1"\2":', twy_str)
    # replace single quotes with double
    twy_str = twy_str.replace("'", '"')
    # remove trailing commas
    twy_str = re.sub(r',\s*\}', '}', twy_str)
    twy_str = re.sub(r',\s*\]', ']', twy_str)
    
    try:
        twy_json = json.loads(twy_str)
        with open('airports/OMDB/taxiways.json', 'w', encoding='utf-8') as f:
            json.dump(twy_json['OMDB']['taxiways'], f, indent=2)
        print("Extracted taxiways.json")
    except Exception as e:
        print("Failed to parse taxiways:", e)
        # write the raw string to inspect
        with open('airports/OMDB/taxiways_raw.txt', 'w', encoding='utf-8') as f:
            f.write(twy_str)
else:
    print("Could not find window.AIRPORTS")

# 3. Create registry.json
registry = {
  "OMDB": {
    "name": "Dubai International",
    "iata": "DXB",
    "badge": "AE · UAE · IATA: DXB",
    "chart": "airports/OMDB/chart.jpg",
    "taxiways": "airports/OMDB/taxiways.json"
  }
}
with open('airports/registry.json', 'w', encoding='utf-8') as f:
    json.dump(registry, f, indent=2)
print("Created registry.json")
