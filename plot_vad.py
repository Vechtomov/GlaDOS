import matplotlib.pyplot as plt
import numpy as np
import queue
import threading
import time
from matplotlib.animation import FuncAnimation

from glados import vad
from pathlib import Path
from queue import Queue
import sounddevice as sd


VAD_MODEL = "silero_vad.onnx"

PAUSE_TIME = 0.05  # Time to wait between processing loops
SAMPLE_RATE = 16000  # Sample rate for input stream
VAD_SIZE = 50  # Milliseconds of sample for Voice Activity Detection (VAD)
VAD_THRESHOLD = 0.9  # Threshold for VAD detection
BUFFER_SIZE = 600  # Milliseconds of buffer before VAD detection
PAUSE_LIMIT = 400  # Milliseconds of pause allowed before processing

data_queue = queue.Queue()

vad_model = vad.VAD(model_path=str(Path.cwd() / "models" / VAD_MODEL))

def audio_callback(indata, frames, time, status):
    data = indata.copy()
    data = data.squeeze()
    conf = vad_model.process_chunk(data)
    # vad_confidence = conf > VAD_THRESHOLD
    data_queue.put(conf)


input_stream = sd.InputStream(
            samplerate=SAMPLE_RATE,
            channels=1,
            callback=audio_callback,
            blocksize=int(SAMPLE_RATE * VAD_SIZE / 1000),
        )


# Setup the queue

# Initialize the plot
fig, ax = plt.subplots()
ax.set_ylim(0, 1)
x, y = [], []
line, = ax.plot(x, y, 'r-')  # 'r-' is for a red line

def update(frame):
    while not data_queue.empty():
        new_y = data_queue.get()
        x.append(len(x))
        y.append(new_y)
        print(new_y)

    line.set_data(x, y)
    ax.set_xlim(0, max(x) + 1) if x else 1
    return line,

def data_feeder():
    input_stream.start()

# Start a thread for feeding data
thread = threading.Thread(target=data_feeder)
thread.daemon = True
thread.start()

# Animation function
ani = FuncAnimation(fig, update, blit=True, interval=10)

plt.show()