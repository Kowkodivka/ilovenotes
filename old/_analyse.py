import librosa
import numpy as np
import matplotlib.pyplot as plt

# Путь к аудиофайлу
audio_path = "./am.flac"

# Загрузка аудио
y, sr = librosa.load(audio_path)

# Полное FFT-преобразование для всего аудиосигнала
fft_result = np.fft.fft(y)
fft_magnitudes = np.abs(fft_result)  # Амплитуды частот
frequencies = np.fft.fftfreq(len(fft_magnitudes), 1 / sr)  # Частоты

# Оставим только положительные частоты для удобства отображения
positive_freqs = frequencies[: len(frequencies) // 2]
positive_magnitudes = fft_magnitudes[: len(fft_magnitudes) // 2]

# Визуализация спектра частот всего сигнала
plt.figure(figsize=(12, 6))
plt.plot(positive_freqs, positive_magnitudes, color="blue")
plt.xlabel("Частота (Hz)")
plt.ylabel("Амплитуда")
plt.title("Спектр частот аудиосигнала (FFT)")
plt.show()

# Кратковременное преобразование Фурье для спектрограммы
D = np.abs(librosa.stft(y))  # амплитудный спектр
DB = librosa.amplitude_to_db(D, ref=np.max)

# Визуализация спектрограммы
plt.figure(figsize=(12, 6))
librosa.display.specshow(DB, sr=sr, x_axis="time", y_axis="log", cmap="magma")
plt.colorbar(format="%+2.0f dB")
plt.title("Спектрограмма аудиосигнала")
plt.xlabel("Время (с)")
plt.ylabel("Частота (Hz)")
plt.show()
