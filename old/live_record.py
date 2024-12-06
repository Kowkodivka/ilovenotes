import sounddevice as sd
import numpy as np
from collections import deque
import time

# Параметры записи
sample_rate = 44100  # или подходящую частоту, совместимую с PulseAudio/ALSA
sd.default.device = "pulse"  # или 'pipewire'
duration = 3  # Длина буфера в секундах
buffer_size = int(sample_rate * duration)  # Размер буфера в отсчетах
chunk_size = int(sample_rate * 0.5)  # Размер фрагмента для анализа (полсекунды)

# Создаем циклический буфер фиксированного размера для аудиоданных
audio_buffer = deque(maxlen=buffer_size)


# Функция обработки аудио
def analyze_audio(data_chunk):
    # Пример: вычисление средней амплитуды для анализа
    amplitude = np.mean(np.abs(data_chunk))
    print("Средняя амплитуда:", amplitude)


# Callback-функция для потоковой записи
def audio_callback(indata, frames, time, status):
    if status:
        print("Ошибка записи:", status)
    # Добавляем данные в буфер
    audio_buffer.extend(indata[:, 0])


# Запуск потока
with sd.InputStream(samplerate=sample_rate, channels=1, callback=audio_callback):
    print("Запись начата. Обработка на лету...")

    try:
        while True:
            # Если буфер содержит достаточно данных для анализа
            if len(audio_buffer) >= chunk_size:
                # Преобразуем буфер в массив и возьмем последние chunk_size отсчетов
                current_data = np.array(audio_buffer)[-chunk_size:]

                # Вызываем функцию анализа
                analyze_audio(current_data)

            time.sleep(0.5)  # Интервал обновления анализа (0.5 секунды)

    except KeyboardInterrupt:
        print("Остановлено пользователем.")
