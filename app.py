from flask import Flask, request, jsonify, send_file
import yt_dlp
import os

app = Flask(__name__)

# ✅ Health Check Route
@app.route("/")
def home():
    return jsonify({"message": "API is working!"})

# 🔍 Normal Search — Get Song/Video Details
@app.route("/search")
def search():
    query = request.args.get("query")
    if not query:
        return jsonify({"error": "Provide a search query!"}), 400

    search_options = {
        "default_search": "ytsearch1",  # Fetch only 1 best match
        "dump_single_json": True
    }

    with yt_dlp.YoutubeDL(search_options) as ydl:
        search_result = ydl.extract_info(query, download=False)

    if not search_result or "entries" not in search_result or len(search_result["entries"]) == 0:
        return jsonify({"error": "No results found!"})

    first_result = search_result["entries"][0]
    details = {
        "title": first_result.get("title"),
        "uploader": first_result.get("uploader"),
        "duration": first_result.get("duration"),
        "views": first_result.get("view_count"),
        "likes": first_result.get("like_count"),
        "thumbnail": first_result.get("thumbnail"),
        "url": first_result.get("webpage_url")
    }

    return jsonify(details)

# 🎵 Download Song — MP3 Format
@app.route("/download/song")
def download_song():
    query = request.args.get("query")
    if not query:
        return jsonify({"error": "Provide a song query!"}), 400

    return download_media(query, "mp3")

# 🎥 Download Video — MP4 Format
@app.route("/download/video")
def download_video():
    query = request.args.get("query")
    if not query:
        return jsonify({"error": "Provide a video query!"}), 400

    return download_media(query, "mp4")

# 🔥 Universal Media Downloader (Handles Both Audio & Video)
def download_media(query, format_type):
    search_options = {
        "default_search": "ytsearch1",
        "dump_single_json": True
    }

    with yt_dlp.YoutubeDL(search_options) as ydl:
        search_result = ydl.extract_info(query, download=False)

    if not search_result or "entries" not in search_result or len(search_result["entries"]) == 0:
        return jsonify({"error": "No results found!"})

    first_video_url = search_result["entries"][0]["webpage_url"]

    download_options = {
        "format": "bestaudio/best" if format_type == "mp3" else "best",
        "postprocessors": [{"key": "FFmpegExtractAudio", "preferredcodec": "mp3"}] if format_type == "mp3" else [],
        "outtmpl": f"downloaded.{format_type}"
    }

    with yt_dlp.YoutubeDL(download_options) as ydl:
        ydl.extract_info(first_video_url, download=True)

    file_name = next((f for f in os.listdir() if f.startswith("downloaded")), None)
    return send_file(file_name, as_attachment=True) if file_name else jsonify({"error": "Download failed."})

# ✅ Flask Binding
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)