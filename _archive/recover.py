import json
import re

transcript_path = r'C:\Users\mo7am\.gemini\antigravity-ide\brain\92dd415f-5502-4c5e-9005-51dc2892a974\.system_generated\logs\transcript.jsonl'
with open(transcript_path, 'r', encoding='utf-8') as f:
    for line in f:
        try:
            data = json.loads(line)
            # Check content
            content = data.get('content', '')
            if 'window.CHART_IMAGES' in content and 'window.AIRPORTS' in content:
                # We found a big string containing the data. 
                # Let's see if we can extract the whole HTML
                html_match = re.search(r'(<!DOCTYPE html>.*?</html>)', content, re.DOTALL | re.IGNORECASE)
                if html_match:
                    with open('recovered.html', 'w', encoding='utf-8') as out:
                        out.write(html_match.group(1))
                    print("Recovered from content!")
                    break
        except Exception as e:
            pass
