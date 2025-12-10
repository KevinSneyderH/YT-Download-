from flask import Flask, request, send_file, jsonify, send_from_directory
import yt_dlp
import os
import uuid

app = Flask(__name__, static_folder="static", static_url_path="")

DOWNLOAD_FOLDER = "downloads"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)


# --- FRONTEND ---
@app.route("/")
def home():
    return send_from_directory("static", "index.html")


# --- BACKEND ---
@app.route("/download", methods=["POST"])
def download():
    url = request.form.get("url")

    if not url:
        return "Error: No ingresaste URL"

    file_id = str(uuid.uuid4())
    output_path = os.path.join(DOWNLOAD_FOLDER, file_id + ".mp3")

    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": os.path.join(DOWNLOAD_FOLDER, file_id + ".%(ext)s"),
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }],
        "noplaylist": True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.extract_info(url, download=True)

        return send_file(output_path, as_attachment=True)

    except Exception as e:
        return f"Error al descargar: {str(e)}"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
