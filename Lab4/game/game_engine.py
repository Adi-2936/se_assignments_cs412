import pygame

from .bird import Bird
from .pipe import Pipe
from .sound_manager import SoundManager


WHITE = (255, 255, 255)
DARK = (21, 32, 48)
GREEN = (42, 168, 74)
GREEN_DARK = (24, 116, 51)
GOLD = (255, 205, 74)

DIFFICULTIES = {
    "Easy": {"speed": 3, "gap": 190, "interval": 105},
    "Medium": {"speed": 4, "gap": 160, "interval": 90},
    "Hard": {"speed": 6, "gap": 130, "interval": 74},
}


class GameEngine:
    """Owns gameplay state, input handling, collision, audio, and menus."""

    def __init__(self, width, height, sound_manager=None):
        self.width = width
        self.height = height
        self.font = pygame.font.SysFont("Arial", 30, bold=True)
        self.small_font = pygame.font.SysFont("Arial", 20)
        self.title_font = pygame.font.SysFont("Arial", 48, bold=True)
        self.sounds = sound_manager or SoundManager()
        self.should_quit = False
        self.difficulty = "Medium"
        self.final_score = 0
        self.game_over_reason = ""
        self.start_game(self.difficulty)

    def start_game(self, difficulty):
        if difficulty not in DIFFICULTIES:
            raise ValueError(f"Unknown difficulty: {difficulty}")
        self.difficulty = difficulty
        settings = DIFFICULTIES[difficulty]
        self.pipe_speed = settings["speed"]
        self.pipe_gap = settings["gap"]
        self.pipe_interval = settings["interval"]
        self.bird = Bird(self.width // 4, self.height // 2)
        self._spawn_timer = 0
        self.pipes = [
            Pipe(
                self.width + 100,
                self.height,
                gap=self.pipe_gap,
                speed=self.pipe_speed,
            )
        ]
        self.score = 0
        self.final_score = 0
        self.state = "playing"
        # Kept as a public compatibility flag for simple tests and extensions.
        self.game_over = False
        self.game_over_reason = ""

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            self.should_quit = True
            return

        if self.state == "playing":
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self._flap()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self._flap()
            return

        if self.state == "game_over":
            if event.type == pygame.KEYDOWN:
                difficulty_keys = {
                    pygame.K_1: "Easy",
                    pygame.K_e: "Easy",
                    pygame.K_2: "Medium",
                    pygame.K_m: "Medium",
                    pygame.K_3: "Hard",
                    pygame.K_h: "Hard",
                }
                if event.key in difficulty_keys:
                    self.start_game(difficulty_keys[event.key])
                elif event.key in (pygame.K_ESCAPE, pygame.K_q):
                    self.should_quit = True
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                selected = self._difficulty_at(event.pos)
                if selected:
                    self.start_game(selected)

    def handle_input(self):
        # Flapping is deliberately edge-triggered in handle_event, preventing a
        # held key from turning into continuous flight.
        pass

    def _flap(self):
        self.bird.flap()
        self.sounds.play("flap")

    def _finish_game(self, reason):
        if self.state != "playing":
            return
        self.state = "game_over"
        self.game_over = True
        self.final_score = self.score
        self.game_over_reason = reason
        self.sounds.play("death")

    def update(self):
        if self.state != "playing":
            return

        self.bird.update()
        if self.bird.y - self.bird.radius <= 0:
            self._finish_game("You hit the ceiling")
            return
        if self.bird.y + self.bird.radius >= self.height:
            self._finish_game("You hit the ground")
            return

        self._spawn_timer += 1
        if self._spawn_timer >= self.pipe_interval:
            self._spawn_timer = 0
            self.pipes.append(
                Pipe(
                    self.width,
                    self.height,
                    gap=self.pipe_gap,
                    speed=self.pipe_speed,
                )
            )

        for pipe in self.pipes:
            pipe.move()
            if any(
                self.bird.collides_with_rect(rect)
                for rect in pipe.collision_rects()
            ):
                self._finish_game("You hit a pipe")
                break

            if not pipe.scored and pipe.x + pipe.width < self.bird.x:
                pipe.scored = True
                self.score += 1
                self.sounds.play("score")

        self.pipes = [pipe for pipe in self.pipes if not pipe.off_screen()]

    def render(self, screen):
        self._draw_background(screen)
        for pipe in self.pipes:
            self._draw_pipe(screen, pipe.top_rect(), cap_at_bottom=True)
            self._draw_pipe(screen, pipe.bottom_rect(), cap_at_bottom=False)

        bird_center = (round(self.bird.x), round(self.bird.y))
        pygame.draw.circle(screen, GOLD, bird_center, self.bird.radius)
        pygame.draw.circle(screen, DARK, bird_center, self.bird.radius, 2)
        pygame.draw.circle(screen, WHITE, (bird_center[0] + 6, bird_center[1] - 5), 5)
        pygame.draw.circle(screen, DARK, (bird_center[0] + 7, bird_center[1] - 5), 2)

        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        difficulty_text = self.small_font.render(self.difficulty, True, WHITE)
        screen.blit(score_text, (16, 14))
        screen.blit(difficulty_text, (self.width - difficulty_text.get_width() - 16, 20))

        if self.state == "game_over":
            self._draw_game_over(screen)

    def _draw_background(self, screen):
        screen.fill((118, 194, 232))
        pygame.draw.circle(screen, (255, 236, 147), (420, 90), 48)
        for x, y in ((55, 95), (245, 145), (390, 225)):
            pygame.draw.circle(screen, WHITE, (x, y), 24)
            pygame.draw.circle(screen, WHITE, (x + 25, y + 4), 18)
            pygame.draw.circle(screen, WHITE, (x - 24, y + 6), 17)

    def _draw_pipe(self, screen, rect, cap_at_bottom):
        pygame.draw.rect(screen, GREEN_DARK, rect)
        inner = rect.inflate(-8, 0)
        pygame.draw.rect(screen, GREEN, inner)
        cap_height = 24
        cap_y = rect.bottom - cap_height if cap_at_bottom else rect.top
        cap = pygame.Rect(rect.x - 5, cap_y, rect.width + 10, cap_height)
        pygame.draw.rect(screen, GREEN_DARK, cap)
        pygame.draw.rect(screen, GREEN, cap.inflate(-6, -6))

    def _button_rects(self):
        width, height, gap = 124, 48, 12
        total = width * 3 + gap * 2
        left = (self.width - total) // 2
        top = 430
        return {
            name: pygame.Rect(left + index * (width + gap), top, width, height)
            for index, name in enumerate(("Easy", "Medium", "Hard"))
        }

    def _difficulty_at(self, position):
        for difficulty, rect in self._button_rects().items():
            if rect.collidepoint(position):
                return difficulty
        return None

    def _draw_game_over(self, screen):
        overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        overlay.fill((7, 14, 24, 205))
        screen.blit(overlay, (0, 0))

        title = self.title_font.render("GAME OVER", True, GOLD)
        final = self.font.render(f"Final score: {self.final_score}", True, WHITE)
        reason = self.small_font.render(self.game_over_reason, True, (220, 229, 239))
        prompt = self.small_font.render("Choose a difficulty to play again", True, WHITE)
        screen.blit(title, title.get_rect(center=(self.width // 2, 235)))
        screen.blit(final, final.get_rect(center=(self.width // 2, 305)))
        screen.blit(reason, reason.get_rect(center=(self.width // 2, 344)))
        screen.blit(prompt, prompt.get_rect(center=(self.width // 2, 395)))

        for index, (difficulty, rect) in enumerate(self._button_rects().items(), start=1):
            pygame.draw.rect(screen, (54, 83, 117), rect, border_radius=8)
            pygame.draw.rect(screen, WHITE, rect, 2, border_radius=8)
            label = self.small_font.render(f"{index}  {difficulty}", True, WHITE)
            screen.blit(label, label.get_rect(center=rect.center))

        exit_text = self.small_font.render("Press Q or Esc to exit", True, (207, 218, 232))
        screen.blit(exit_text, exit_text.get_rect(center=(self.width // 2, 515)))
