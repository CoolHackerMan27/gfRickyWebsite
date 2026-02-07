from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
import ijson  # Streaming JSON parser - memory efficient
import json
import asyncio
from concurrent.futures import ProcessPoolExecutor
from typing import List
import tempfile
import os
from pathlib import Path

app = FastAPI(title="Rickify JSON Processor")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:4173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Process pool for CPU-bound JSON processing
executor = ProcessPoolExecutor(max_workers=4)


def process_json_file(file_path: str) -> dict:
    """
    Process a single JSON file using streaming parser.
    Modify this function with your 'rickify' logic.
    """
    results = []

    with open(file_path, 'rb') as f:

        parser = ijson.items(f, 'item')  # Assumes root is an array

        for item in parser:

            processed = rickify_item(item)
            results.append(processed)

    return {"file": os.path.basename(file_path), "count": len(results), "data": results}


def rickify_item(item: dict) -> dict:

    return item


@app.post("/process")
async def process_single_file(file: UploadFile = File(...)):
    """Process a single JSON file."""
    if not file.filename.endswith('.json'):
        raise HTTPException(400, "File must be JSON")

    # Save to temp file for streaming
    with tempfile.NamedTemporaryFile(delete=False, suffix='.json') as tmp:
        while chunk := await file.read(1024 * 1024):  # 1MB chunks
            tmp.write(chunk)
        tmp_path = tmp.name

    try:
        # Process in separate process to not block event loop
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(executor, process_json_file, tmp_path)
        return result
    finally:
        os.unlink(tmp_path)  # Clean up temp file


@app.post("/process-batch")
async def process_multiple_files(files: List[UploadFile] = File(...)):
    """Process multiple JSON files in parallel."""
    temp_paths = []

    # Save all files to temp storage
    for file in files:
        if not file.filename.endswith('.json'):
            continue
        with tempfile.NamedTemporaryFile(delete=False, suffix='.json') as tmp:
            while chunk := await file.read(1024 * 1024):
                tmp.write(chunk)
            temp_paths.append((file.filename, tmp.name))

    try:
        # Process all files in parallel using process pool
        loop = asyncio.get_event_loop()
        tasks = [
            loop.run_in_executor(executor, process_json_file, path)
            for _, path in temp_paths
        ]
        results = await asyncio.gather(*tasks)

        return {
            "total_files": len(results),
            "results": results
        }
    finally:
        # Clean up all temp files
        for _, path in temp_paths:
            os.unlink(path)


@app.get("/health")
async def health():
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
