import numpy as np
import soundfile as sf
from core import Note


path = "G.flac"
y, sr = sf.read(path)

if y.ndim > 1:
    y = np.mean(y, axis=1)

fft_y = np.fft.fft(y)
fft_m = np.abs(fft_y)
freqs = np.fft.fftfreq(len(fft_m), 1 / sr)

positive_mask = freqs > 0
positive_freqs = freqs[positive_mask]
positive_fft_m = fft_m[positive_mask]

threshold = np.max(positive_fft_m) * 0.1
significant_mask = positive_fft_m > threshold
significant_freqs = positive_freqs[significant_mask]

min_freq = 41
max_freq = 660
filtered_freqs = significant_freqs[
    (significant_freqs >= min_freq) & (significant_freqs <= max_freq)
]

notes = [Note.from_hz(hz) for hz in filtered_freqs]
human_readable = [note.to_human_readable() for note in notes]
unique_notes = np.unique(human_readable)

print(unique_notes)
