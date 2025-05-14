from flask import Flask, request, jsonify
from flask_cors import CORS
import yt_dlp

app = Flask(__name__)
CORS(app)

@app.route('/download', methods=['POST'])
def download():
    data = request.json
    video_url = data.get('url')
    if not video_url:
        return jsonify({'error': 'URL missing'}), 400

    try:
        ydl_opts = {
            'format': 'best[ext=mp4]/best',
            'quiet': True,
            'noplaylist': True
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            return jsonify({
                'title': info.get('title'),
                'url': info.get('url'),
                'thumbnail': info.get('thumbnail')
            })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/', methods=['GET'])
def home():
    return "Fast Downloader Backend is Running"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
