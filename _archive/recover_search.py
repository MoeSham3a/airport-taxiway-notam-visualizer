import json
transcript_path = r'C:\Users\mo7am\.gemini\antigravity-ide\brain\92dd415f-5502-4c5e-9005-51dc2892a974\.system_generated\logs\transcript.jsonl'
count = 0
with open(transcript_path, 'r', encoding='utf-8') as f:
    for line in f:
        if 'CHART_IMAGES' in line:
            count += 1
            with open(f'found_{count}.txt', 'w', encoding='utf-8') as out:
                out.write(line)
print(f"Found {count} occurrences")
