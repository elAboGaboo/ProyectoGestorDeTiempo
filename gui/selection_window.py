import sys
from PyQt5.QtWidgets import QMainWindow, QPushButton, QVBoxLayout, QWidget

class SelectionWindow(QMainWindow):
    def __init__(self, navigate_to):
        super().__init__()
        self.navigate_to = navigate_to

        self.setWindowTitle("Select Timer Type")
        self.setGeometry(100, 100, 300, 200)

        self.layout = QVBoxLayout()

        self.timer_button = QPushButton("Timer")
        self.timer_button.clicked.connect(lambda: self.navigate_to('timer'))
        self.layout.addWidget(self.timer_button)

        self.alarm_button = QPushButton("Alarm")
        self.alarm_button.clicked.connect(lambda: self.navigate_to('alarm'))
        self.layout.addWidget(self.alarm_button)

        self.pomodoro_button = QPushButton("Pomodoro")
        self.pomodoro_button.clicked.connect(lambda: self.navigate_to('pomodoro'))
        self.layout.addWidget(self.pomodoro_button)

        container = QWidget()
        container.setLayout(self.layout)
        self.setCentralWidget(container)
