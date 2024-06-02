import sounddevice as sd
import soundfile as sf

SAMPLE_RATE = 44100  # Sample rate in Hz
RECORD_SECONDS = 10  # Duration to record in seconds

def record_audio(duration, samplerate):
    print("Recording...")
    myrecording = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=1, dtype='float32')
    sd.wait()  # Wait until recording is finished
    print("Done recording.")
    return myrecording

# Record audio
audio_data = record_audio(RECORD_SECONDS, SAMPLE_RATE)

# Save the recorded audio as a WAV file
wav_file = 'output.wav'
sf.write(wav_file, audio_data, SAMPLE_RATE)

