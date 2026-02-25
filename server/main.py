from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
import ijson
import json
import asyncio
from concurrent.futures import ProcessPoolExecutor
from typing import List
import tempfile
import os
from pathlib import Path
# hardcoded list of ricky & the honeysticks songs.
rickySongs = [
    "Line Without A Hook",
    "Mr Loverman",
    "Boy Toy",
    "Nobody Likes Me",
    "Black Fins",
    "Sorry for Me",
    "Talk to you",
    "Out like a Light",
    "My Heart is Buried in Venice",
    "I Dont't Love You Anymore",
    "Get to You",
    "Out Like a Light 2",
    "Snow",
    "Cabo",
    "Dont Know How",
    "Last Night",
    "California",
    "Get Used To It",
    "Cars",
    "Better",
    "Don't Say That",
    "Eraser",
    "Sunday Best",
]


rickyAlbums = [
    "Montgomery Ricky",
    "Edits",
    "Rick",
    "Ricky(y)",
    "The Honeysticks"
]
app = FastAPI(title="Rickify JSON Processor")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:4173",
                   "https://gf-ricky-website-2t900e5r8-coolhackerman27s-projects.vercel.app", "https://gf-ricky-website.vercel.app", "https://rickyif.vercel.app"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Process pool for CPU-bound JSON processing
executor = ProcessPoolExecutor(max_workers=4)


def getAlbumByArtist(jsonData, artistName):
    albumsByArtist = []
    for item in jsonData:
        try:
            if artistName in item["master_metadata_album_artist_name"]:
                albumsByArtist.append(item["master_metadata_album_album_name"])
        except Exception as e:
            # print(f"Error processing item: {e}")
            continue
    # remove duplicates
    albumsByArtist = list(set(albumsByArtist))
    return albumsByArtist


def percentAlbumInListened(jsonData, albumList):
    albumsListened = []
    for item in jsonData:
        try:
            albumName = item["master_metadata_album_album_name"]
            if albumName != "None":
                albumsListened.append(albumName)
        except Exception as e:
            # print(f"Error processing item: {e}")
            continue
    albumsListened = list(set(albumsListened))
    count = 0
    for album in albumList:
        if album in albumsListened:
            count += 1
    percent = (count / len(albumList)) * 100
    return percent


def percentSongsInListened(jsonData, songList):
    songsListened = []
    for item in jsonData:
        try:
            songName = item["master_metadata_track_name"]
            if songName != "None":
                songsListened.append(songName)
        except Exception as e:
            # print(f"Error processing item: {e}")
            continue
    songsListened = list(set(songsListened))
    count = 0
    for song in songList:
        if song in songsListened:
            count += 1
    percent = (count / len(songList)) * 100
    return percent


def rankSongsByPlayCount(jsonData):
    songPlayCount = {}
    for item in jsonData:
        try:
            songName = item["master_metadata_track_name"]
            if songName != "None":
                if songName in songPlayCount:
                    songPlayCount[songName] += 1
                else:
                    songPlayCount[songName] = 1
        except Exception as e:
            # print(f"Error processing item: {e}")
            continue
    rankedSongs = sorted(
        songPlayCount.items(), key=lambda x: x[1], reverse=True)
    return rankedSongs


def rankSongsByTimeListened(jsonData, songs, artistNames=None):
    songTimeListened = {}
    for item in jsonData:
        try:
            songName = item.get("master_metadata_track_name")
            if not songName or songName not in songs:
                continue
            # if artistNames provided, ensure the item's artist matches one of them
            if artistNames:
                artist = item.get("master_metadata_album_artist_name", "")
                if not any(a in artist for a in artistNames):
                    continue
            songTimeListened[songName] = songTimeListened.get(
                songName, 0) + item.get("ms_played", 0)
        except Exception:
            continue
    # remove songs with 0 time listened and songs not in songs list
    songTimeListened = {k: v for k,
                        v in songTimeListened.items() if v > 0 and k in songs}
    rankedSongs = sorted(
        songTimeListened.items(), key=lambda x: x[1], reverse=True)
    return rankedSongs


def getSongByArtist(jsonData, artistName):
    songsByArtist = []
    for item in jsonData:
        try:
            if artistName in item["master_metadata_album_artist_name"]:
                songsByArtist.append(item["master_metadata_track_name"])
        except Exception as e:
            # print(f"Error processing item: {e}")
            continue
    # remove duplicates
    songsByArtist = list(set(songsByArtist))
    return songsByArtist


def getTimeListenedByArtist(jsonData, artistName):
    timeListened = 0
    for item in jsonData:
        try:
            if artistName in item["master_metadata_album_artist_name"]:
                timeListened += item["ms_played"]
        except Exception as e:
            # print(f"Error processing item: {e}")
            continue
    timeListened = timeListened / 60000
    return timeListened


def process_json_file(file_path: str) -> dict:
    """
    Process a single JSON file using streaming parser.
    Modify this function with your 'rickify' logic.
    """

    with open(file_path, 'rb') as f:

        parser = ijson.items(f, 'item')  # Assumes root is an array
        allData = []
        for item in parser:
            allData.append(item)
        songs = getSongByArtist(allData, "Ricky Montgomery")
        albums = getAlbumByArtist(allData, "Ricky Montgomery")
        timeListened = getTimeListenedByArtist(allData, "Ricky Montgomery")
        # add "The Honeysticks" a band he's in
        songs.extend(getSongByArtist(allData, "The Honeysticks"))
        albums.extend(getAlbumByArtist(allData, "The Honeysticks"))
        timeListened += getTimeListenedByArtist(allData, "The Honeysticks")
        # deduplicate after merging both artists
        songs = list(set(songs))
        albums = list(set(albums))
        percentAlbums = percentAlbumInListened(allData, rickyAlbums)
        percentSongs = percentSongsInListened(allData, rickySongs)
        rankSongsByTime = rankSongsByTimeListened(
            allData, rickySongs, ["Ricky Montgomery", "The Honeysticks"])
    result = {
        "songs": songs,
        "albums": albums,
        "timeListened": timeListened,
        "percentSongs": percentSongs,
        "percentAlbums": percentAlbums,
        "ranked": rankSongsByTime,
        "numberOfSongs": len(songs),
        "numberOfAlbums": len(albums)
    }
    return result


def rickify_item(item: dict) -> dict:

    return item


def aggregate_results(results: List[dict]) -> dict:
    """Combine multiple file results into one grand total."""

    all_songs = set()
    all_albums = set()
    total_time = 0.0
    merged_rankings = {}

    for res in results:
        all_songs.update(res["songs"])
        all_albums.update(res["albums"])
        total_time += res["timeListened"]

        for song_name, ms_played in res["ranked"]:
            if song_name in merged_rankings:
                merged_rankings[song_name] += ms_played
            else:
                merged_rankings[song_name] = ms_played

    # Percentages: how many of the hardcoded lists were found in the data
    percentSongs = (sum(1 for s in rickySongs if s in all_songs) /
                    len(rickySongs)) * 100 if rickySongs else 0
    percentAlbums = (sum(1 for a in rickyAlbums if a in all_albums) /
                     len(rickyAlbums)) * 100 if rickyAlbums else 0

    final_ranked = sorted(merged_rankings.items(),
                          key=lambda x: x[1], reverse=True)

    return {
        "songs": list(all_songs),
        "albums": list(all_albums),
        "timeListened": total_time,
        "percentSongs": percentSongs,
        "percentAlbums": percentAlbums,
        "ranked": final_ranked,
        "numberOfSongs": len(all_songs),
        "numberOfAlbums": len(all_albums)
    }


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
        # aggregate results if needed, for now just return list of results
        final_result = aggregate_results(results)
        return final_result

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
