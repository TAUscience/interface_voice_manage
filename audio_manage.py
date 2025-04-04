import numpy as np
import matplotlib.pyplot as plt
import wave
import scipy.signal as signal
from scipy.signal import firwin, lfilter

def procesar_audio(archivo_wav):
    with wave.open(archivo_wav, 'rb') as wav_file:
        sample_rate = wav_file.getframerate()
        num_frames = wav_file.getnframes()
        num_channels = wav_file.getnchannels()
        sample_width = wav_file.getsampwidth()

        frames = wav_file.readframes(num_frames)
        audio_data = np.frombuffer(frames, dtype=np.int16 if sample_width == 2 else np.int32)

        # Si el audio tiene más de un canal, convertirlo a mono
        if num_channels > 1:
            audio_data = audio_data.reshape(-1, num_channels)
            audio_data = np.mean(audio_data, axis=1)

    # Normalizar el audio
    audio_data = audio_data / np.iinfo(np.int16).max

    # Generar vector de tiempo
    tiempo = np.linspace(0, len(audio_data) / sample_rate, num=len(audio_data))

    # Convertir amplitud a decibeles
    audio_data_db = 20 * np.log10(np.abs(audio_data) + 1e-10)  # Para evitar log(0)

    return sample_rate, tiempo, audio_data, audio_data_db

def guardar_audio(archivo_salida, sample_rate, audio_data):
    # Escalar de vuelta a int16 para guardar como WAV
    audio_data = (audio_data * np.iinfo(np.int16).max).astype(np.int16)
    with wave.open(archivo_salida, 'wb') as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(audio_data.tobytes())
