import time
import numpy as np
import sounddevice as sd
import librosa
from collections import deque, Counter

sample_rate = 44100
sd.default.device = "pulse"
duration = 1

buffer_size = int(sample_rate * duration)
chunk_size = int(buffer_size * 0.1)

audio_buffer = deque(maxlen=buffer_size)

min_freq = 41
max_freq = 660

chord_dictionary = {
    "C": {"C", "E", "G"},
    "Cm": {"C", "D♯", "G"},
    "C7": {"C", "E", "G", "A♯"},
    "Cm7": {"C", "D♯", "G", "A♯"},
    "Cmaj7": {"C", "E", "G", "B"},
    "Cdim": {"C", "D♯", "F♯"},
    "Caug": {"C", "E", "G♯"},
    "C6": {"C", "E", "G", "A"},
    "C9": {"C", "E", "G", "A♯", "D"},

    "D": {"D", "F♯", "A"},
    "Dm": {"D", "F", "A"},
    "D7": {"D", "F♯", "A", "C"},
    "Dm7": {"D", "F", "A", "C"},
    "Dmaj7": {"D", "F♯", "A", "C♯"},
    "Ddim": {"D", "F", "G♯"},
    "Daug": {"D", "F♯", "A♯"},
    "D6": {"D", "F♯", "A", "B"},
    "D9": {"D", "F♯", "A", "C", "E"},

    "E": {"E", "G♯", "B"},
    "Em": {"E", "G", "B"},
    "E7": {"E", "G♯", "B", "D"},
    "Em7": {"E", "G", "B", "D"},
    "Emaj7": {"E", "G♯", "B", "D♯"},
    "Edim": {"E", "G", "A♯"},
    "Eaug": {"E", "G♯", "C"},
    "E6": {"E", "G♯", "B", "C♯"},
    "E9": {"E", "G♯", "B", "D", "F♯"},

    "F": {"F", "A", "C"},
    "Fm": {"F", "G♯", "C"},
    "F7": {"F", "A", "C", "D♯"},
    "Fm7": {"F", "G♯", "C", "D♯"},
    "Fmaj7": {"F", "A", "C", "E"},
    "Fdim": {"F", "G♯", "B"},
    "Faug": {"F", "A", "C♯"},
    "F6": {"F", "A", "C", "D"},
    "F9": {"F", "A", "C", "D♯", "G"},

    "G": {"G", "B", "D"},
    "Gm": {"G", "A♯", "D"},
    "G7": {"G", "B", "D", "F"},
    "Gm7": {"G", "A♯", "D", "F"},
    "Gmaj7": {"G", "B", "D", "F♯"},
    "Gdim": {"G", "A♯", "C♯"},
    "Gaug": {"G", "B", "D♯"},
    "G6": {"G", "B", "D", "E"},
    "G9": {"G", "B", "D", "F", "A"},

    "A": {"A", "C♯", "E"},
    "Am": {"A", "C", "E"},
    "A7": {"A", "C♯", "E", "G"},
    "Am7": {"A", "C", "E", "G"},
    "Amaj7": {"A", "C♯", "E", "G♯"},
    "Adim": {"A", "C", "D♯"},
    "Aaug": {"A", "C♯", "F"},
    "A6": {"A", "C♯", "E", "F♯"},
    "A9": {"A", "C♯", "E", "G", "B"},
    
    "B": {"B", "D♯", "F♯"},
    "Bm": {"B", "D", "F♯"},
    "B7": {"B", "D♯", "F♯", "A"},
    "Bm7": {"B", "D", "F♯", "A"},
    "Bmaj7": {"B", "D♯", "F♯", "A♯"},
    "Bdim": {"B", "D", "F"},
    "Baug": {"B", "D♯", "G"},
    "B6": {"B", "D♯", "F♯", "G♯"},
    "B9": {"B", "D♯", "F♯", "A", "C♯"},
}


def analyze_audio(data, sr):
    fft_y = np.fft.fft(data)
    fft_m = np.abs(fft_y)
    freqs = np.fft.fftfreq(len(fft_m), 1 / sr)

    positive_freqs = freqs[freqs > 0]
    positive_fft_m = fft_m[freqs > 0]

    threshold = np.max(positive_fft_m) * 0.1
    significant_freqs = positive_freqs[positive_fft_m > threshold]

    filtered_freqs = significant_freqs[
        (significant_freqs >= min_freq) & (significant_freqs <= max_freq)
    ]

    notes = librosa.hz_to_note(filtered_freqs, octave=False)
    unique_notes = np.unique(notes)

    chord_matches = []
    for chord, chord_notes in chord_dictionary.items():
        match_count = sum(1 for note in chord_notes if note in unique_notes)
        if match_count > 0:
            chord_matches.append((chord, match_count))

    chord_matches = sorted(chord_matches, key=lambda x: -x[1])

    best_chords = (
        [chord for chord, count in chord_matches if count == chord_matches[0][1]]
        if chord_matches
        else []
    )

    print("Извлеченные ноты:", unique_notes)
    print("Наиболее подходящие аккорды:")
    for chord in best_chords:
        print(f"{chord}")


def audio_callback(indata, frames, time, status):
    audio_buffer.extend(indata[:, 0])


with sd.InputStream(samplerate=sample_rate, channels=1, callback=audio_callback):
    try:
        while True:
            if len(audio_buffer) >= chunk_size:
                current_data = np.array(audio_buffer)[-chunk_size:]
                analyze_audio(current_data, sample_rate)
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("Программа остановлена")
