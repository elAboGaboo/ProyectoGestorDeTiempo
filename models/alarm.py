import datetime
import time
import logging

class Alarm:
    def __init__(self, alarm_time):
        self.alarm_time = alarm_time

    def start(self):
        while True:
            current_time = datetime.datetime.now().time()
            if current_time >= self.alarm_time:
                self.play_ring()
                break
            time.sleep(1)

    def play_ring(self):
        logging.info("Playing alarm ring for 3 seconds...")
        time.sleep(3)  # Simulating ring duration

# models/alarm.py
import pygame

class Alarm:
    def __init__(self):
        pygame.mixer.init()  # Inicializar pygame para la reproducción de sonidos

    def ring(self, sound_file):
        pygame.mixer.music.load(sound_file)
        pygame.mixer.music.play()
        pygame.time.delay(3000)  # Reproducir por 3 segundos
        pygame.mixer.music.stop()
