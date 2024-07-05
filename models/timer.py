import time
import threading

class Timer:
    def __init__(self, duration):
        self.duration = duration
        self.remaining = duration
        self.running = False
        self.start_time = None
        self._thread = None
        self._lock = threading.Lock()

    def start(self):
        self.running = True
        if not self._thread:
            self._thread = threading.Thread(target=self._run)
            self._thread.start()
        else:
            with self._lock:
                self.start_time = time.time() - (self.duration - self.remaining)

    def _run(self):
        with self._lock:
            self.start_time = time.time()
        while self.running:
            with self._lock:
                elapsed = time.time() - self.start_time
                self.remaining = self.duration - elapsed
                if self.remaining <= 0:
                    self.remaining = 0
                    self.running = False
                    self.play_ring()
                    break
            time.sleep(0.1)

    def pause(self):
        with self._lock:
            if self.running:
                elapsed = time.time() - self.start_time
                self.remaining -= elapsed
                self.running = False

    def reset(self):
        with self._lock:
            self.running = False
            self.remaining = self.duration
            self.start_time = None
            self._thread = None

    def play_ring(self):
        print("Playing ring for 3 seconds...")
        time.sleep(3)  # Simulating ring duration

# models/timer.py
import time
import pygame

class Timer:
    def __init__(self, duration):
        self.duration = duration
        pygame.mixer.init()  # Inicializar pygame para la reproducción de sonidos

    def start(self):
        self.play_sound("start_sound.mp3")  # Reproducir sonido al iniciar
        time.sleep(self.duration)
        self.play_sound("end_sound.mp3")    # Reproducir sonido al finalizar

    def play_sound(self, sound_file):
        pygame.mixer.music.load(sound_file)
        pygame.mixer.music.play()
        time.sleep(3)  # Ajustar según sea necesario
        pygame.mixer.music.stop()
