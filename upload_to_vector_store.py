from openai import OpenAI
from pathlib import Path
from typing import List, Optional
import os
from dotenv import load_dotenv

def upload_files_to_vectorstore(
    directory_path: str,
    vector_store_id: str,
    file_extensions: List[str] = [".json"],
    batch_size: int = 100,
    env_path: Optional[str] = None
) -> None:
    if env_path:
        load_dotenv(env_path)
    
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    
    file_paths = [
        path for path in Path(directory_path).glob("**/*")
        if path.suffix in file_extensions and path.stat().st_size > 0
    ]
    
    total_files = len(file_paths)
    print(f"Found {total_files} files to process")
    
    for i in range(0, total_files, batch_size):
        batch_paths = file_paths[i:i + batch_size]
        file_streams = [open(path, "rb") for path in batch_paths]
        
        try:
            file_batch = client.beta.vector_stores.file_batches.upload_and_poll(
                vector_store_id=vector_store_id,
                files=file_streams
            )
            
            print(f"Batch {i//batch_size + 1} status: {file_batch.status}")
            print(f"File counts: {file_batch.file_counts}")
            
        finally:
            for file in file_streams:
                file.close()

if __name__ == "__main__":
    # Example usage
    upload_files_to_vectorstore(
        directory_path="/Users/adamhunter/Documents/smart_audiencev2/data/segments",
        vector_store_id="vs_vWTUDyouIoHU0zKz7AaZe4uu",
        env_path="/Users/adamhunter/miniconda3/envs/ragdev/ragdev.env"
    )