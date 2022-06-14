from flask import Flask, Response
import pyaudio
# import webbrowser

from threading import Thread


HOST = '0.0.0.0'
PORT = 2408

# webbrowser.open('http://127.0.0.1:80/radio', new=2)

DEVICE_INDEX = 1 # microphone.py
FORMAT = pyaudio.paInt16
CHUNK = 1024
RATE = 48000
bitsPerSample = 16
CHANNELS = 1

app = Flask(__name__)
audio = pyaudio.PyAudio()

def Header(sampleRate, bitsPerSample, channels):
    datasize = 2048*10**5
    o = bytes("RIFF",'ascii')                                               # (4byte) Marks file as RIFF
    o += (datasize + 36).to_bytes(4,'little')                               # (4byte) File size in bytes excluding this and RIFF marker
    o += bytes("WAVE",'ascii')                                              # (4byte) File type
    o += bytes("fmt ",'ascii')                                              # (4byte) Format Chunk Marker
    o += (16).to_bytes(4,'little')                                          # (4byte) Length of above format data
    o += (1).to_bytes(2,'little')                                           # (2byte) Format type (1 - PCM)
    o += (channels).to_bytes(2,'little')                                    # (2byte)
    o += (sampleRate).to_bytes(4,'little')                                  # (4byte)
    o += (sampleRate * channels * bitsPerSample // 8).to_bytes(4,'little')  # (4byte)
    o += (channels * bitsPerSample // 8).to_bytes(2,'little')               # (2byte)
    o += (bitsPerSample).to_bytes(2,'little')                               # (2byte)
    o += bytes("data",'ascii')                                              # (4byte) Data Chunk Marker
    o += (datasize).to_bytes(4,'little')                                    # (4byte) Data size in bytes
    return o

stream = audio.open(
    format=FORMAT, 
    channels=CHANNELS,
    rate=RATE, 
    input=True, 
    input_device_index=DEVICE_INDEX,
    frames_per_buffer=CHUNK
    )


def test():
    @app.route('/radio')
    def radio():
        def sound():
            wav_header = Header(RATE, bitsPerSample, CHANNELS)
            data = wav_header
            data += stream.read(CHUNK)
            yield(data)
            while True:
                data = stream.read(CHUNK)
                yield(data)
        return Response(sound(), mimetype="audio/x-wav; codec=vorbis")

    if __name__ == "__main__":
        app.run(host=HOST, port=PORT, threaded=True)

Thread(target=test).start()