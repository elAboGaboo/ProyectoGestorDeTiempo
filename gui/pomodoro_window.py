# gui/pomodoro_window.py
import sys
import threading
from PyQt5.QtWidgets import QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, QSpinBox
from PyQt5.QtCore import QTimer, QThread, pyqtSignal
from models.timer import Timer

class PomodoroWorker(QThread):
    timer_updated = pyqtSignal(int, int)
    timer_finished = pyqtSignal(bool)

    def __init__(self, work_duration, break_duration):
        super().__init__()
        self.work_duration = work_duration
        self.break_duration = break_duration
        self.is_work_period = True

    def run(self):
        while True:
            if self.is_work_period:
                self.run_timer(self.work_duration)
                self.timer_finished.emit(True)
            else:
                self.run_timer(self.break_duration)
                self.timer_finished.emit(False)

    def run_timer(self, duration):
        timer = Timer(duration)
        timer_thread = threading.Thread(target=timer.start)
        timer_thread.start()
        while timer.running:
            minutes, seconds = divmod(int(timer.remaining), 60)
            self.timer_updated.emit(minutes, seconds)
            QThread.sleep(1)

    def switch_period(self):
        self.is_work_period = not self.is_work_period

class PomodoroWindow(QMainWindow):
    def __init__(self, back_callback):
        super().__init__()
        self.back_callback = back_callback

        self.setWindowTitle("Pomodoro Timer")
        self.setGeometry(100, 100, 300, 200)

        self.layout = QVBoxLayout()

        self.work_duration_spinbox = QSpinBox()
        self.work_duration_spinbox.setRange(1, 60)
        self.work_duration_spinbox.setSuffix(" minutes")
        self.layout.addWidget(self.work_duration_spinbox)

        self.break_duration_spinbox = QSpinBox()
        self.break_duration_spinbox.setRange(1, 30)
        self.break_duration_spinbox.setSuffix(" minutes")
        self.layout.addWidget(self.break_duration_spinbox)

        self.timer_label = QLabel("Timer: 00:00")
        self.layout.addWidget(self.timer_label)

        self.start_button = QPushButton("Start Pomodoro")
        self.start_button.clicked.connect(self.start_pomodoro)
        self.layout.addWidget(self.start_button)

        self.back_button = QPushButton("Back")
        self.back_button.clicked.connect(self.go_back)
        self.layout.addWidget(self.back_button)

        container = QWidget()
        container.setLayout(self.layout)
        self.setCentralWidget(container)

    def start_pomodoro(self):
        work_duration = self.work_duration_spinbox.value() * 60
        break_duration = self.break_duration_spinbox.value() * 60

        self.worker = PomodoroWorker(work_duration, break_duration)
        self.worker.timer_updated.connect(self.update_timer_display)
        self.worker.timer_finished.connect(self.switch_period)
        self.worker.start()

    def update_timer_display(self, minutes, seconds):
        self.timer_label.setText(f"Timer: {minutes:02d}:{seconds:02d}")

    def switch_period(self, is_work_period):
        if is_work_period:
            self.timer_label.setText("Break Time!")
        else:
            self.timer_label.setText("Work Time!")

    def go_back(self):
        self.close()
        self.back_callback()
