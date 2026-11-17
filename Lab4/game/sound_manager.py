import math
from array import array

import pygame


class SoundManager:
    """Small procedural sound bank with a silent fallback.

    Generating tones at startup keeps the project self-contained while still
    providing immediate feedback for flapping, scoring, and dying.
    """

    def __init__(self):
        self.enabled = False
        self.sounds = {}
        try:
            if pygame.mixer.get_init() is None:
                pygame.mixer.init(frequency=44_100, size=-16, channels=2)
            self.sounds = {
                "flap": self._tone(660, 0.07, 0.18),
                "score": self._tone(990, 0.11, 0.22),
                "death": self._tone(180, 0.32, 0.26, end_frequency=80),
            }
            self.enabled = True
        except pygame.error:
            # The game remains fully playable on machines without an audio device.
            self.enabled = False

    def _tone(self, frequency, duration, volume, end_frequency=None):
        sample_rate, _, channels = pygame.mixer.get_init()
        frame_count = int(sample_rate * duration)
        samples = array("h")
        end_frequency = frequency if end_frequency is None else end_frequency

        phase = 0.0
        for index in range(frame_count):
            progress = index / max(1, frame_count - 1)
            current_frequency = frequency + (end_frequency - frequency) * progress
            phase += 2 * math.pi * current_frequency / sample_rate
            envelope = min(1.0, progress * 20) * max(0.0, 1.0 - progress)
            value = int(32_767 * volume * envelope * math.sin(phase))
            for _ in range(channels):
                samples.append(value)
        return pygame.mixer.Sound(buffer=samples.tobytes())

    def play(self, name):
        if self.enabled and name in self.sounds:
            self.sounds[name].play()
