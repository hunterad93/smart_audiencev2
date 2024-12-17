import csv
import json
from pathlib import Path

def ensure_data_directory():
    Path("data/demo_segments").mkdir(parents=True, exist_ok=True)

def clean_filename(text):
    return text.lower().replace(' ', '_').replace('/', '_')

def save_segment(segment):
    segment_id = segment['id']
    print(f"Saving segment {segment_id}")
    filepath = Path(f"data/demo_segments/{segment_id}.json")
    filepath.write_text(json.dumps(segment, indent=2), encoding='utf-8')

def process_segments(csv_path):
    ensure_data_directory()
    print(f"Processing CSV: {csv_path}")
    
    with open(csv_path, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        row_count = 0
        
        for row in reader:
            path_parts = row['FullPath'].split(' > ')[3:]
            if len(path_parts) < 2:
                continue
            
            row_count += 1
            print(f"Processing row {row_count}: {row['ThirdPartyDataId']}")
            
            segment = {
                "full_path": row['FullPath'],
                "description": row['Description'],
                "id": row['ThirdPartyDataId'],
                "category": path_parts[0],
                "subcategory": path_parts[-2]
            }
            
            save_segment(segment)

process_segments('/Users/adamhunter/Documents/smart_audiencev2/data/age-gender_segments.csv')