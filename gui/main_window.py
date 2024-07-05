# gui/main_window.py
import sys
import threading
from PyQt5.QtWidgets import QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, QSpinBox
from PyQt5.QtCore import QTimer
from models.timer import Timer

class MainWindow(QMainWindow):
    def __init__(self, back_callback):
        super().__init__()
        self.back_callback = back_callback

        self.setWindowTitle("Timer")
        self.setGeometry(100, 100, 300, 200)

        self.layout = QVBoxLayout()

        self.timer_label = QLabel("Timer: 00:00")
        self.layout.addWidget(self.timer_label)

        self.duration_spinbox = QSpinBox()
        self.duration_spinbox.setRange(1, 3600)
        self.duration_spinbox.setSuffix(" seconds")
        self.layout.addWidget(self.duration_spinbox)

        self.start_button = QPushButton("Start Timer")
        self.start_button.clicked.connect(self.start_timer)
        self.layout.addWidget(self.start_button)

        self.pause_button = QPushButton("Pause Timer")
        self.pause_button.clicked.connect(self.pause_timer)
        self.layout.addWidget(self.pause_button)

        self.reset_button = QPushButton("Reset Timer")
        self.reset_button.clicked.connect(self.reset_timer)
        self.layout.addWidget(self.reset_button)

        self.back_button = QPushButton("Back")
        self.back_button.clicked.connect(self.go_back)
        self.layout.addWidget(self.back_button)

        self.timer = Timer(0)
        self.update_timer_display()

        self.timer_thread = None
        self.qt_timer = QTimer()
        self.qt_timer.timeout.connect(self.update_timer_display)
        self.qt_timer.start(100)

        container = QWidget()
        container.setLayout(self.layout)
        self.setCentralWidget(container)

    def start_timer(self):
        duration = self.duration_spinbox.value()
        self.timer = Timer(duration)
        self.timer_thread = threading.Thread(target=self.timer.start)
        self.timer_thread.start()

    def pause_timer(self):
        if self.timer.running:
            self.timer.pause()

    def reset_timer(self):
        self.timer.reset()
        self.update_timer_display()

    def update_timer_display(self):
        if self.timer:
            minutes, seconds = divmod(int(self.timer.remaining), 60)
            self.timer_label.setText(f"Timer: {minutes:02d}:{seconds:02d}")
            if not self.timer.running and self.timer.remaining == 0:
                self.timer_label.setText("Timer: 00:00")

    def go_back(self):
        self.close()
        self.back_callback()
