from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import ijson
import asyncio
from concurrent.futures import ProcessPoolExecutor
from typing import List
import tempfile
import os

# hardcoded lists of songs and albums to check against
rickySongs = [
    "Line Without A Hook", "Mr Loverman", "Boy Toy", "Nobody Likes Me",
    "Black Fins", "Sorry for Me", "Talk to you", "Out like a Light",
    "My Heart is Buried in Venice", "I Dont't Love You Anymore",
    "Get to You", "Out Like a Light 2", "Snow", "Cabo", "Dont Know How",
    "Last Night", "California", "Get Used To It", "Cars", "Better",
    "Don't Say That", "Eraser", "Sunday Best",
]

rickyAlbums = [
    "Montgomery Ricky", "Edits", "Rick", "Ricky(y)", "The Honeysticks"
]


def _normalize_key(s: str) -> str:
    """Standardizes strings for comparison (lowercase, stripped)."""
    if not s:
        return ""
    try:
        return " ".join(str(s).split()).strip().lower()
    except Exception:
        return str(s).strip().lower()


NORMALIZED_SONGS = {_normalize_key(s): s for s in rickySongs}
NORMALIZED_ALBUMS = {_normalize_key(a): a for a in rickyAlbums}
TARGET_ARTISTS = ["ricky montgomery", "the honeysticks"]

app = FastAPI(title="Rickify JSON Processor")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:4173",
                   "https://gf-ricky-website-2t900e5r8-coolhackerman27s-projects.vercel.app",
                   "https://gf-ricky-website.vercel.app", "https://rickyif.vercel.app"],
    allow_methods=["*"],
    allow_headers=["*"],
)

executor = ProcessPoolExecutor(max_workers=4)


def process_json_file(file_path: str) -> dict:

    found_songs_map = {}
    found_albums_map = {}
    song_play_counts = {}
    total_ms = 0

    with open(file_path, 'rb') as f:
        # Use ijson generator to stream items one by one (memory efficient)
        parser = ijson.items(f, 'item')

        for item in parser:
            try:

                track_name = item.get("master_metadata_track_name")
                album_name = item.get("master_metadata_album_album_name")
                artist_name = item.get("master_metadata_album_artist_name")
                ms_played = item.get("ms_played", 0)

                if not track_name or not artist_name:
                    continue

                artist_lower = str(artist_name).lower()
                if not any(target in artist_lower for target in TARGET_ARTISTS):
                    continue

                track_key = _normalize_key(track_name)
                if track_key in NORMALIZED_SONGS:

                    original_name = NORMALIZED_SONGS[track_key]
                    found_songs_map[track_key] = original_name

                    total_ms += ms_played

                    song_play_counts[track_key] = song_play_counts.get(
                        track_key, 0) + ms_played

                    if album_name:
                        album_key = _normalize_key(album_name)
                        if album_key in NORMALIZED_ALBUMS:
                            found_albums_map[album_key] = NORMALIZED_ALBUMS[album_key]

            except Exception as e:
                # Skip malformed items
                continue

    # Format ranked songs list: [(Display Name, ms_played), ...]
    ranked_songs = []
    for key, ms in song_play_counts.items():
        display_name = found_songs_map[key]
        ranked_songs.append((display_name, ms))

    ranked_songs.sort(key=lambda x: x[1], reverse=True)

    percent_songs = (len(found_songs_map) / len(rickySongs)
                     * 100) if rickySongs else 0
    percent_albums = (len(found_albums_map) / len(rickyAlbums)
                      * 100) if rickyAlbums else 0

    return {
        "songs": list(found_songs_map.values()),
        "albums": list(found_albums_map.values()),
        "timeListened": total_ms / 60000.0,  # Convert ms to minutes
        "percentSongs": percent_songs,
        "percentAlbums": percent_albums,
        "ranked": ranked_songs,
        "numberOfSongs": len(found_songs_map),
        "numberOfAlbums": len(found_albums_map)
    }


def aggregate_results(results: List[dict]) -> dict:

    unique_songs = set()
    unique_albums = set()
    total_time_minutes = 0.0
    merged_song_stats = {}

    for res in results:

        total_time_minutes += res.get("timeListened", 0)

        for s in res.get("songs", []):
            unique_songs.add(s)

        for a in res.get("albums", []):
            unique_albums.add(a)

        for song_name, ms in res.get("ranked", []):
            merged_song_stats[song_name] = merged_song_stats.get(
                song_name, 0) + ms

    percent_songs = (len(unique_songs) / len(rickySongs)
                     * 100) if rickySongs else 0
    percent_albums = (len(unique_albums) / len(rickyAlbums)
                      * 100) if rickyAlbums else 0

    # Re-sort ranked list
    final_ranked = sorted(merged_song_stats.items(),
                          key=lambda x: x[1], reverse=True)

    return {
        "songs": list(unique_songs),
        "albums": list(unique_albums),
        "timeListened": total_time_minutes,
        "percentSongs": percent_songs,
        "percentAlbums": percent_albums,
        "ranked": final_ranked,
        "numberOfSongs": len(unique_songs),
        "numberOfAlbums": len(unique_albums),
    }


@app.post("/process")
async def process_single_file(file: UploadFile = File(...)):
    if not file.filename.endswith('.json'):
        raise HTTPException(400, "File must be JSON")

    with tempfile.NamedTemporaryFile(delete=False, suffix='.json') as tmp:
        while chunk := await file.read(1024 * 1024):
            tmp.write(chunk)
        tmp_path = tmp.name

    try:
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(executor, process_json_file, tmp_path)
        return result
    finally:
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)


@app.post("/process-batch")
async def process_multiple_files(files: List[UploadFile] = File(...)):
    temp_paths = []
    for file in files:
        if not file.filename.endswith('.json'):
            continue
        with tempfile.NamedTemporaryFile(delete=False, suffix='.json') as tmp:
            while chunk := await file.read(1024 * 1024):
                tmp.write(chunk)
            temp_paths.append(tmp.name)

    try:
        loop = asyncio.get_event_loop()
        tasks = [
            loop.run_in_executor(executor, process_json_file, path)
            for path in temp_paths
        ]
        if not tasks:
            return aggregate_results([])

        results = await asyncio.gather(*tasks)
        return aggregate_results(results)

    finally:
        for path in temp_paths:
            if os.path.exists(path):
                os.unlink(path)


@app.get("/health")
async def health():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
