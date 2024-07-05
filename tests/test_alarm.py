import unittest
import datetime
import logging
from models.alarm import Alarm


class TestAlarm(unittest.TestCase):
    def test_alarm_ring(self):
        # Set alarm time to 1 second from now
        alarm_time = (datetime.datetime.now() + datetime.timedelta(seconds=1)).time()
        alarm = Alarm(alarm_time)

        with self.assertLogs(level='INFO') as log:
            alarm.start()
            # Verificar que 'Playing alarm ring for 3 seconds...' esté en algún mensaje del log
            log_messages = [record.getMessage() for record in log.records]
            self.assertIn('Playing alarm ring for 3 seconds...', log_messages)


if __name__ == '__main__':
    unittest.main()
