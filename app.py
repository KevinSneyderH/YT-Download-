from flask import Flask, request, send_file, jsonify
import yt_dlp
import os
import uuid

app = Flask(__name__)

DOWNLOAD_FOLDER = "downloads"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

@app.route("/")
def home():
    return """
    <h2>Descargar MP3 de YouTube</h2>
    <form action='/download' method='post'>
        <input type='text' name='url' placeholder='URL del video' style='width:300px'>
        <button type='submit'>Descargar</button>
    </form>
    """

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
