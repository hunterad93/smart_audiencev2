import csv
import json
from pathlib import Path

def ensure_data_directory():
    Path("data/segments").mkdir(parents=True, exist_ok=True)

def clean_filename(text):
    return text.lower().replace(' ', '_').replace('/', '_')

def save_segment(segment):
    segment_id = segment['id']
    filepath = Path(f"data/segments/{segment_id}.json")
    filepath.write_text(json.dumps(segment, indent=2), encoding='utf-8')

def process_segments(csv_path):
    ensure_data_directory()
    
    with open(csv_path, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        
        for row in reader:
            path_parts = row['FullPath'].split(' > ')[3:]
            if len(path_parts) < 2:
                continue
                
            segment = {
                "full_path": row['FullPath'],
                "description": row['Description'],
                "id": row['ThirdPartyDataId'],
                "category": path_parts[0],
                "subcategory": path_parts[-2]
            }
            
            save_segment(segment)

process_segments('pinecone_records_20241216_143114.csv')