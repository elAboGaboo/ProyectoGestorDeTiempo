import unittest
import time
from models.timer import Timer

class TestTimer(unittest.TestCase):
    def test_timer_start(self):
        timer = Timer(duration=1)
        timer.start()
        time.sleep(1.5)  # Let the timer run and exceed the duration
        self.assertEqual(timer.remaining, 0)

    def test_timer_pause(self):
        timer = Timer(duration=2)
        timer.start()
        time.sleep(0.5)  # Let the timer run for half a second
        timer.pause()
        self.assertGreater(timer.remaining, 0)
        self.assertLess(timer.remaining, 2)

    def test_timer_reset(self):
        timer = Timer(duration=10)
        timer.start()
        time.sleep(0.5)  # Let the timer run for half a second
        timer.reset()
        self.assertEqual(timer.remaining, 10)

if __name__ == '__main__':
    unittest.main()
