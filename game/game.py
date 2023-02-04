import pygame
from game.global_state import Global


class Game:
    def __init__(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode(Global.SCRECT.size, pygame.SCALED)
        self.clock = pygame.time.Clock()
        self.glow = Global(events=[], keys=[], dt=0.0, screen=self.screen)

        from game.paddles import LeftPaddle, RightPaddle
        from game.ball import Ball

        self.paddles = (LeftPaddle(), RightPaddle())
        self.dotted_lines = pygame.image.load("assets/dotted.png").convert_alpha()
        self.dotted_lines.set_alpha(50)
        self.ball = Ball(50)

        self.glow.left_paddle, self.glow.right_paddle = self.paddles
        pygame.display.set_caption("Ping Pong")

    def handle_quit(self) -> None:
        for event in self.glow.events:
            if event.type == pygame.QUIT:
                raise SystemExit

    def update(self) -> None:
        events = pygame.event.get()
        self.glow.events = events
        self.glow.keys = pygame.key.get_pressed()
        self.glow.dt = self.clock.tick(self.glow.FPS) / 1000

        self.handle_quit()

        for paddle in self.paddles:
            paddle.update()

        self.ball.update()

    def draw(self) -> None:
        self.screen.fill((30, 30, 40))
        self.screen.blit(self.dotted_lines, (0, 0))
        for paddle in self.paddles:
            paddle.draw()

        self.ball.draw()

        pygame.display.update()

    def run(self) -> None:
        while True:
            self.update()
            self.draw()


def main():
    game = Game()
    game.run()
