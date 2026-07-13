import re, json, os

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Extract taxiways string
match = re.search(r"window\.AIRPORTS\s*=\s*\{\s*OMDB:\s*\{\s*taxiways:\s*(\{.*?\})\s*\}\s*\};", content, re.DOTALL)
if match:
    twy_str = match.group(1)
    
    # Parse twy_str manually into dictionary
    taxiways = {}
    # Find all 'key': { x: 123, y: 456, label: 'key' } lines
    # or 'key': { points: [[x,y],...], label: 'key', intersects: [...] }
    # Let's just use a simple regex to replace keys to make it valid JSON
    
    # Remove comments
    twy_str = re.sub(r'//.*?\n', '\n', twy_str)
    
    # Quote keys
    twy_str = re.sub(r'([{,]\s*)([a-zA-Z0-9_]+)\s*:', r'\1"\2":', twy_str)
    # Replace single quotes with double quotes
    twy_str = twy_str.replace("'", '"')
    
    # Remove trailing commas
    twy_str = re.sub(r',\s*\}', '}', twy_str)
    twy_str = re.sub(r',\s*\]', ']', twy_str)
    
    try:
        twy_data = json.loads(twy_str)
        os.makedirs('airports/OMDB', exist_ok=True)
        with open('airports/OMDB/taxiways.json', 'w', encoding='utf-8') as f:
            json.dump(twy_data, f, indent=2)
        print("Successfully extracted taxiways.json")
    except Exception as e:
        print("Failed to parse taxiways JSON:", e)

# Now remove from index.html
new_content = re.sub(r"window\.CHART_IMAGES\s*=\s*\{.*?\};\n*", "", content, flags=re.DOTALL)
new_content = re.sub(r"window\.AIRPORTS\s*=\s*\{.*?\};\n*", "", new_content, flags=re.DOTALL)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(new_content)
    
print("Updated index.html")
