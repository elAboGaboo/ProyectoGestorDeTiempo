from PyQt5.QtCore import QObject, pyqtSignal, QTimer, QThread, QCoreApplication
import time
import threading
import pygame

class Timer(QObject):
    timer_updated = pyqtSignal(int, int)
    timer_finished = pyqtSignal(bool)

    def __init__(self, duration):
        super().__init__()
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
                    self.timer_finished.emit(True)
                    break
            self.timer_updated.emit(self.remaining // 60, self.remaining % 60)
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

class PomodoroSoundPlayer(QObject):
    def __init__(self):
        super().__init__()
        pygame.mixer.init()

    def play_sound(self, sound_file):
        pygame.mixer.music.load(sound_file)
        pygame.mixer.music.play()

    def stop_sound(self):
        pygame.mixer.music.stop()

    def close(self):
        pygame.mixer.quit()

class PomodoroWorker(QObject):
    timer_updated = pyqtSignal(int, int)
    timer_finished = pyqtSignal(bool)

    def __init__(self, work_duration, break_duration):
        super().__init__()
        self.work_timer = Timer(work_duration)
        self.break_timer = Timer(break_duration)
        self.is_work_period = True
        self.sound_player = PomodoroSoundPlayer()

    def start_pomodoro(self):
        while True:
            if self.is_work_period:
                self.work_timer.timer_finished.connect(self._on_timer_finished)
                self.work_timer.start()
                self.sound_player.play_sound("work_sound.mp3")
                self.is_work_period = False
            else:
                self.break_timer.timer_finished.connect(self._on_timer_finished)
                self.break_timer.start()
                self.sound_player.play_sound("break_sound.mp3")
                self.is_work_period = True

    def _on_timer_finished(self):
        self.sound_player.stop_sound()
        self.timer_finished.emit(self.is_work_period)

    def pause(self):
        self.work_timer.pause()
        self.break_timer.pause()
        self.sound_player.stop_sound()

    def reset(self):
        self.work_timer.reset()
        self.break_timer.reset()
        self.is_work_period = True
        self.sound_player.stop_sound()

    def close(self):
        self.sound_player.close()

