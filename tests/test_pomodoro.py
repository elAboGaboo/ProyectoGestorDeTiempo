import unittest
from models.pomodoro import PomodoroTimer

class TestPomodoroTimer(unittest.TestCase):
    def setUp(self):
        self.work_duration = 25 * 60  # 25 minutes in seconds
        self.break_duration = 5 * 60  # 5 minutes in seconds
        self.pomodoro_timer = PomodoroTimer(self.work_duration, self.break_duration)

    def test_pomodoro_timer(self):
        self.pomodoro_timer.start()
        self.assertTrue(self.pomodoro_timer.work_timer.running)
        self.assertTrue(self.pomodoro_timer.break_timer.running)

    def tearDown(self):
        self.pomodoro_timer.work_timer.reset()
        self.pomodoro_timer.break_timer.reset()

if __name__ == '__main__':
    unittest.main()
