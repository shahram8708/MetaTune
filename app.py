from flask import Flask, render_template, request, redirect, url_for
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, TIT2, TPE1, TALB, TCON, TDRC, TRCK, COMM
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'mp3'}

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def get_metadata(filepath):
    audio = MP3(filepath, ID3=ID3)
    
    metadata = {
        "title": audio.tags.get('TIT2').text[0] if audio.tags.get('TIT2') else "Unknown",
        "artist": audio.tags.get('TPE1').text[0] if audio.tags.get('TPE1') else "Unknown",
        "album": audio.tags.get('TALB').text[0] if audio.tags.get('TALB') else "Unknown",
        "genre": audio.tags.get('TCON').text[0] if audio.tags.get('TCON') else "Unknown",
        "release_year": audio.tags.get('TDRC').text[0] if audio.tags.get('TDRC') else "Unknown",
        "track_number": audio.tags.get('TRCK').text[0] if audio.tags.get('TRCK') else "Unknown",
        "comments": audio.tags.get('COMM').text[0] if audio.tags.get('COMM') else "None",
        "duration": int(audio.info.length),
        "bitrate": audio.info.bitrate
    }
    
    return metadata

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)
            return redirect(url_for('show_metadata', filename=file.filename))
    return render_template('upload.html')

@app.route('/metadata/<filename>')
def show_metadata(filename):
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    metadata = get_metadata(filepath)
    
    return render_template('metadata.html', metadata=metadata)

if __name__ == '__main__':
    app.run(debug=True)
