import random

import pygame


class Pipe:
    def __init__(self, x, screen_height, gap=150, width=70, speed=4):
        self.x = x
        self.previous_x = x
        self.width = width
        self.gap = gap
        self.speed = speed
        self.screen_height = screen_height
        margin = 90
        self.gap_y = random.randint(margin, screen_height - margin - gap)
        self.scored = False

    def move(self):
        self.previous_x = self.x
        self.x -= self.speed

    def off_screen(self):
        return self.x + self.width < 0

    def top_rect(self):
        return pygame.Rect(round(self.x), 0, self.width, self.gap_y)

    def bottom_rect(self):
        bottom_y = self.gap_y + self.gap
        return pygame.Rect(
            round(self.x), bottom_y, self.width, self.screen_height - bottom_y
        )

    def collision_rects(self):
        """Return swept pipe rectangles for the most recent movement frame."""
        left = round(min(self.x, self.previous_x))
        travel = round(abs(self.x - self.previous_x))
        swept_width = self.width + travel
        bottom_y = self.gap_y + self.gap
        return (
            pygame.Rect(left, 0, swept_width, self.gap_y),
            pygame.Rect(
                left,
                bottom_y,
                swept_width,
                self.screen_height - bottom_y,
            ),
        )
