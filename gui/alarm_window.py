from PyQt5.QtWidgets import QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, QTimeEdit
from PyQt5.QtCore import QTimer, QTime
import datetime

class AlarmWindow(QMainWindow):
    def __init__(self, back_callback):
        super().__init__()
        self.back_callback = back_callback

        self.setWindowTitle("Alarm")
        self.setGeometry(100, 100, 300, 200)

        self.layout = QVBoxLayout()

        self.alarm_time_edit = QTimeEdit()
        self.alarm_time_edit.setDisplayFormat("HH:mm:ss")
        self.layout.addWidget(self.alarm_time_edit)

        self.set_alarm_button = QPushButton("Set Alarm")
        self.set_alarm_button.clicked.connect(self.set_alarm)
        self.layout.addWidget(self.set_alarm_button)

        self.alarm_label = QLabel("Alarm: Not Set")
        self.layout.addWidget(self.alarm_label)

        self.back_button = QPushButton("Back")
        self.back_button.clicked.connect(self.go_back)
        self.layout.addWidget(self.back_button)

        self.alarm_timer = QTimer()
        self.alarm_timer.timeout.connect(self.check_alarm)
        self.alarm_timer.start(1000)

        container = QWidget()
        container.setLayout(self.layout)
        self.setCentralWidget(container)

        self.alarm_time = None

    def set_alarm(self):
        self.alarm_time = self.alarm_time_edit.time()
        self.alarm_label.setText(f"Alarm Set for {self.alarm_time.toString('HH:mm:ss')}")

    def check_alarm(self):
        if self.alarm_time:
            current_time = QTime.currentTime()
            if current_time >= self.alarm_time:
                self.alarm_label.setText("Alarm: Ringing!")
                self.play_ring()
                self.alarm_time = None

    def play_ring(self):
        print("Playing ring for 3 seconds...")
        QTimer.singleShot(3000, self.reset_alarm_label)

    def reset_alarm_label(self):
        self.alarm_label.setText("Alarm: Not Set")

    def go_back(self):
        self.close()
        self.back_callback()
