import pyaudio
import wave

SAMPLE_RATE = 16000  # Sample rate in Hz
CHANNELS = 1  # Mono recording
FORMAT = pyaudio.paInt16  # 16-bit audio format
RECORD_SECONDS = 5  # Duration to record
OUTPUT_FILE = "output_pydub.wav"  # Output file name

def record_audio(filename, duration, sample_rate, channels):
    p = pyaudio.PyAudio()

    # Open a new stream
    stream = p.open(format=FORMAT, channels=channels, rate=sample_rate,
                    input=True, frames_per_buffer=1024)

    print("Recording...")
    frames = []

    for _ in range(0, int(sample_rate / 1024 * duration)):
        data = stream.read(1024)
        frames.append(data)

    print("Done recording.")

    # Stop and close the stream
    stream.stop_stream()
    stream.close()
    p.terminate()

    # Save the audio to a WAV file
    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(sample_rate)
        wf.writeframes(b''.join(frames))

# Call the function to record audio
record_audio(OUTPUT_FILE, RECORD_SECONDS, SAMPLE_RATE, CHANNELS)
