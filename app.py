from flask import Flask, request, jsonify, send_file
import yt_dlp
import os

app = Flask(__name__)

# ✅ Health Check Route
@app.route("/")
def home():
    return jsonify({"message": "API is working!"})

# 🔍 YouTube Search with More Results
@app.route("/search")
def search():
    query = request.args.get("q")
    if not query:
        return jsonify({"error": "Provide a search query!"}), 400

    options = {
        "default_search": "ytsearch10",  # 🔍 Gets 10 results instead,
        "cookiefile": "cookies.json"
    }

    with yt_dlp.YoutubeDL(options) as ydl:
        search_results = ydl.extract_info(query, download=False)

    return jsonify(search_results.get("entries", []))

# 🎵 Download YouTube Video or Audio (Streaming Optimized)
@app.route("/download")
def download():
    video_url = request.args.get("url")
    format_type = request.args.get("format", "mp3")

    if not video_url:
        return jsonify({"error": "Provide a video URL!"}), 400

    options = {
        "format": "bestaudio/best" if format_type == "mp3" else "best",
        "postprocessors": [{"key": "FFmpegExtractAudio", "preferredcodec": format_type}] if format_type == "mp3" else [],
        "cookiefile": "cookies.json",
        "outtmpl": "downloaded.%(ext)s"
    }

    with yt_dlp.YoutubeDL(options) as ydl:
        video_info = ydl.extract_info(video_url, download=True)
    
    file_name = next((f for f in os.listdir() if f.startswith("downloaded")), None)
    return send_file(file_name, as_attachment=True) if file_name else jsonify({"error": "Download failed."})

# ✅ Fix Flask Binding (Listen on All IPs)
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)