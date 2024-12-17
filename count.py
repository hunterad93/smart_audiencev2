import json
from pathlib import Path
import tiktoken
from prettytable import PrettyTable

def count_tokens_in_text(text, encoding_name="cl100k_base"):
    encoding = tiktoken.get_encoding(encoding_name)
    return len(encoding.encode(text))

def analyze_json_files():
    data_dir = Path("data")
    if not data_dir.exists():
        print("No data directory found")
        return
    
    results = []
    total_tokens = 0
    
    for json_file in data_dir.glob("*.json"):
        file_content = json_file.read_text(encoding='utf-8')
        token_count = count_tokens_in_text(file_content)
        file_size_kb = json_file.stat().st_size / 1024
        segment_count = count_segments(json.loads(file_content))
        
        results.append({
            "filename": json_file.name,
            "tokens": token_count,
            "size_kb": round(file_size_kb, 2),
            "segments": segment_count
        })
        total_tokens += token_count
    
    table = PrettyTable()
    table.field_names = ["Filename", "Tokens", "Size (KB)", "Segments"]
    
    for result in sorted(results, key=lambda x: x["tokens"], reverse=True):
        table.add_row([
            result["filename"],
            result["tokens"],
            result["size_kb"],
            result["segments"]
        ])
    
    print(table)
    print(f"\nTotal tokens across all files: {total_tokens:,}")

def count_segments(data):
    return sum(len(segments) for segments in data["categories"].values())

if __name__ == "__main__":
    analyze_json_files()