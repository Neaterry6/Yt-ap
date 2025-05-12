from flask import Flask, request, jsonify
import yt_dlp

app = Flask(__name__)

# ✅ Health Check Route
@app.route("/")
def home():
    return jsonify({"message": "API is working!"})

# 🔍 YouTube Search
@app.route("/search")
def search():
    query = request.args.get("q")
    if not query:
        return jsonify({"error": "Provide a search query!"}), 400

    options = {
        "default_search": "ytsearch5",
        "dump_single_json": True,
        "cookiefile": "cookies.json"  # ✅ Using JSON cookies
    }

    with yt_dlp.YoutubeDL(options) as ydl:
        search_results = ydl.extract_info(query, download=False)

    return jsonify(search_results.get("entries", []))

# 🎵 Download YouTube Video or Audio
@app.route("/download")
def download():
    video_url = request.args.get("url")
    format_type = request.args.get("format", "mp3")

    if not video_url:
        return jsonify({"error": "Provide a video URL!"}), 400

    options = {
        "format": "bestaudio/best" if format_type == "mp3" else "best",
        "postprocessors": [{"key": "FFmpegExtractAudio", "preferredcodec": format_type}],
        "cookiefile": "cookies.json"  # ✅ Using JSON cookies for authentication
    }

    with yt_dlp.YoutubeDL(options) as ydl:
        video_info = ydl.extract_info(video_url, download=True)

    return jsonify({"message": "Download complete!", "title": video_info["title"]})

# ✅ Fix Flask Binding for Render (Listen on All IPs)
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
