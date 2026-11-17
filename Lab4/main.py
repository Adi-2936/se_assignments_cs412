import pygame

from game.game_engine import GameEngine


WIDTH, HEIGHT = 500, 700
FPS = 60


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Flappy Bird - Adithya Singh")
    clock = pygame.time.Clock()
    engine = GameEngine(WIDTH, HEIGHT)

    while not engine.should_quit:
        for event in pygame.event.get():
            engine.handle_event(event)

        engine.handle_input()
        engine.update()
        engine.render(screen)
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()
