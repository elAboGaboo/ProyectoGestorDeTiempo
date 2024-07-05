import sys
from PyQt5.QtWidgets import QApplication
from gui.selection_window import SelectionWindow
from gui.main_window import MainWindow
from gui.alarm_window import AlarmWindow
from gui.pomodoro_window import PomodoroWindow

class AppController:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.main_window = None
        self.selection_window = None
        self.show_selection_window()

    def show_selection_window(self):
        self.selection_window = SelectionWindow(self.navigate_to)
        self.selection_window.show()

    def navigate_to(self, choice):
        self.selection_window.close()
        if choice == 'timer':
            self.main_window = MainWindow(self.show_selection_window)
        elif choice == 'alarm':
            self.main_window = AlarmWindow(self.show_selection_window)
        elif choice == 'pomodoro':
            self.main_window = PomodoroWindow(self.show_selection_window)
        self.main_window.show()

    def run(self):
        sys.exit(self.app.exec_())

if __name__ == "__main__":
    controller = AppController()
    controller.run()
