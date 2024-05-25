# server.py
from flask import Flask, request, jsonify
from pydub import AudioSegment
import io

app = Flask(__name__)

@app.route('/process', methods=['POST'])
def process():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})
    file = request.files['file']
    if file:
        result = process_audio(file)
        str_result = ', '.join(map(str, result))
        return jsonify({'result': str_result})
    else:
        return jsonify({'error': 'Invalid file format'})

def process_audio(file):
    audio = AudioSegment.from_mp3(io.BytesIO(file.read()))
    #24000Hzにダウンサンプリング
    processed_data = [0,3,0,4,-7,10,5,6,8,11]
    return processed_data

if __name__ == '__main__':
    app.run(debug=True)
