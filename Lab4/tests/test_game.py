import os
import unittest

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")

import pygame

from game.bird import Bird
from game.game_engine import GameEngine
from game.pipe import Pipe


class SilentSounds:
    def __init__(self):
        self.played = []

    def play(self, name):
        self.played.append(name)


class GameTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pygame.init()

    @classmethod
    def tearDownClass(cls):
        pygame.quit()

    def test_circle_edge_collides_when_center_is_outside_pipe(self):
        bird = Bird(100, 100, radius=15)
        pipe_edge = pygame.Rect(112, 0, 70, 180)
        self.assertFalse(pipe_edge.collidepoint(bird.center()))
        self.assertTrue(bird.collides_with_rect(pipe_edge))

    def test_pipe_collision_area_covers_high_speed_movement(self):
        pipe = Pipe(180, 700, speed=90)
        pipe.gap_y = 220
        pipe.move()
        swept_top, _ = pipe.collision_rects()
        self.assertTrue(swept_top.collidepoint((130, 100)))

    def test_ground_collision_opens_game_over_screen(self):
        sounds = SilentSounds()
        engine = GameEngine(500, 700, sound_manager=sounds)
        engine.bird.y = 690
        engine.update()
        self.assertEqual(engine.state, "game_over")
        self.assertEqual(engine.final_score, 0)
        self.assertIn("ground", engine.game_over_reason)
        self.assertIn("death", sounds.played)

    def test_game_over_difficulty_key_starts_new_game(self):
        engine = GameEngine(500, 700, sound_manager=SilentSounds())
        engine._finish_game("Test")
        engine.handle_event(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_3))
        self.assertEqual(engine.state, "playing")
        self.assertEqual(engine.difficulty, "Hard")
        self.assertEqual(engine.pipe_speed, 6)
        self.assertEqual(engine.pipe_gap, 130)

    def test_flap_and_score_play_feedback(self):
        sounds = SilentSounds()
        engine = GameEngine(500, 700, sound_manager=sounds)
        engine.handle_event(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_SPACE))
        self.assertEqual(engine.bird.velocity, engine.bird.flap_strength)
        self.assertIn("flap", sounds.played)

        pipe = engine.pipes[0]
        pipe.x = engine.bird.x - pipe.width - 2
        pipe.previous_x = pipe.x
        pipe.gap_y = int(engine.bird.y - engine.pipe_gap / 2)
        engine.update()
        self.assertEqual(engine.score, 1)
        self.assertIn("score", sounds.played)


if __name__ == "__main__":
    unittest.main()
