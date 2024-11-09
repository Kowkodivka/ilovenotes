import librosa
import numpy as np
from collections import Counter

# Загрузка аудиофайла
audio_path = "G.flac"
y, sr = librosa.load(audio_path)

# Выполнение FFT и фильтрация частот
fft_y = np.fft.fft(y)
fft_m = np.abs(fft_y)
freqs = np.fft.fftfreq(len(fft_m), 1 / sr)

positive_freqs = freqs[freqs > 0]
positive_fft_m = fft_m[freqs > 0]

# Порог для значимых частот
threshold = np.max(positive_fft_m) * 0.1
significant_freqs = positive_freqs[positive_fft_m > threshold]

# Фильтрация по диапазону гитарных частот
min_freq = 41
max_freq = 660
filtered_freqs = significant_freqs[
    (significant_freqs >= min_freq) & (significant_freqs <= max_freq)
]

# Преобразование значимых частот в ноты
notes = librosa.hz_to_note(filtered_freqs, octave=False)
unique_notes = np.unique(notes)

# Определение аккордов с максимальным совпадением
chord_dictionary = {
    "C": {"C", "E", "G"},
    "Cm": {"C", "D♯", "G"},
    "D": {"D", "F♯", "A"},
    "Dm": {"D", "F", "A"},
    "E": {"E", "G♯", "B"},
    "Em": {"E", "G", "B"},
    "F": {"F", "A", "C"},
    "Fm": {"F", "G♯", "C"},
    "G": {"G", "B", "D"},
    "Gm": {"G", "A♯", "D"},
    "A": {"A", "C♯", "E"},
    "Am": {"A", "C", "E"},
    "B": {"B", "D♯", "F♯"},
    "Bm": {"B", "D", "F♯"},
}

# Найдем количество совпадений нот для каждого аккорда и добавим в список
chord_matches = []
for chord, chord_notes in chord_dictionary.items():
    match_count = sum(1 for note in chord_notes if note in unique_notes)
    if match_count > 0:  # Сохраняем аккорды с совпадением хотя бы одной ноты
        chord_matches.append((chord, match_count))

# Сортируем аккорды по количеству совпадений (полное совпадение будет первым)
chord_matches = sorted(chord_matches, key=lambda x: -x[1])

# Определяем максимальное количество совпадений
if chord_matches:
    max_count = chord_matches[0][1]
    best_chords = [chord for chord, count in chord_matches if count == max_count]
else:
    best_chords = []

# Вывод результатов
print("Извлеченные ноты:", unique_notes)
print("Наиболее подходящие аккорды с максимальным совпадением:")
for chord in best_chords:
    print(f"{chord}")
