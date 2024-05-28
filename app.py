# server.py
from flask import Flask, request, jsonify
from pydub import AudioSegment
from pydub.playback import play
import numpy as np
from scipy.fft import fft
import io
import librosa
from flask_cors import CORS
import pprint

app = Flask(__name__)
CORS(app)

@app.route('/process', methods=['POST'])
def process():
    print(request, flush=True)
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})
    file = request.files['file']
    if file:
        result, times, length, maybe_result = process_audio(file)
        str_result = ', '.join(map(str, result))
        str_times = ', '.join(map(str, times))
        str_maybe_result = ', '.join(map(str, maybe_result))
        print('success', flush=True)
        return jsonify({'result': str_result,'times': str_times,'length': str(length),'f0_full': str_maybe_result})
    else:
        return jsonify({'error': 'Invalid file format'})

def process_audio(file):
    # Read the MP3 file
    audio = AudioSegment.from_mp3(io.BytesIO(file.read()))
    ad_length = len(audio) /1000
    # Downsample to 24000Hz
    target_rate = 24000
    downsampled_audio = audio.set_frame_rate(target_rate)
    del audio
    # WAV形式のデータとして保持
    wav_data = io.BytesIO()
    downsampled_audio.export(wav_data, format="wav")
    del downsampled_audio
    y, sr = librosa.load(wav_data)
    f0, voiced_flag, voiced_probs = librosa.pyin(y, fmin=librosa.note_to_hz('C2'), fmax=librosa.note_to_hz('C7'), sr = target_rate, frame_length = 2400, hop_length = 2400//4)
    f00, voiced_flag, voiced_probs = librosa.pyin(y, fmin=librosa.note_to_hz('C2'), fmax=librosa.note_to_hz('C7'), sr = target_rate, frame_length = 2400, hop_length = 2400//4, fill_na=None)#hop_lengthの影響で設定したフレーム数の情報を得られない
    print(f00,flush=True)
    times = librosa.times_like(f0, sr = target_rate, hop_length = 2400//4)
    return f0, times, ad_length, f00

# 最も顕著なピッチを抽出する
def get_pitch(pitches, magnitudes):
    pitch = []
    for t in range(pitches.shape[1]):
        index = magnitudes[:, t].argmax()
        pitch.append(pitches[index, t])
    return pitch

#pydub2librosa
def audiosegment_to_librosawav(audiosegment):    
    channel_sounds = audiosegment.split_to_mono()
    samples = [s.get_array_of_samples() for s in channel_sounds]

    fp_arr = np.array(samples).T.astype(np.float32)
    fp_arr /= np.iinfo(samples[0].typecode).max
    fp_arr = fp_arr.reshape(-1)

    return fp_arr

if __name__ == '__main__':
    app.run(debug=True)
