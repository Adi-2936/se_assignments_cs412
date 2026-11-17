import pygame


class Bird:
    """Physics and collision shape for the player-controlled bird."""

    def __init__(self, x, y, radius=15):
        self.spawn_x = x
        self.spawn_y = y
        self.radius = radius
        self.gravity = 0.5
        self.flap_strength = -8
        self.reset()

    def reset(self):
        self.x = self.spawn_x
        self.y = self.spawn_y
        self.previous_y = self.y
        self.velocity = 0

    def flap(self):
        self.velocity = self.flap_strength

    def update(self):
        self.previous_y = self.y
        self.velocity += self.gravity
        self.y += self.velocity

    def center(self):
        return self.x, self.y

    def rect(self):
        return pygame.Rect(
            int(self.x - self.radius),
            int(self.y - self.radius),
            self.radius * 2,
            self.radius * 2,
        )

    def collides_with_rect(self, rect):
        """Return True when this circle overlaps a rectangle.

        Using the closest point on the rectangle avoids the starter code's
        center-point bug, where the visible edge of the bird could enter a pipe
        without registering a collision.
        """
        closest_x = max(rect.left, min(self.x, rect.right))
        closest_y = max(rect.top, min(self.y, rect.bottom))
        dx = self.x - closest_x
        dy = self.y - closest_y
        return dx * dx + dy * dy <= self.radius * self.radius
