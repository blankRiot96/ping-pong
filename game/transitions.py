from game.helper import Time
import pygame
from game.global_state import Global


class Transition:
    def __init__(self) -> None:
        self.glow = Global()
        self.num_rows = 3
        self.num_cols = 4
        self.max_width = self.glow.SCREEN_WIDTH / self.num_cols
        self.max_height = self.glow.SCREEN_HEIGHT / self.num_rows
        self.squares: dict[tuple, pygame.Rect] = {}
        self.state = "none"
        self.next_state = None
        self.cool_time = Time(1.5)

        self.expand_rate = 1.05
        self.width = self.max_width / 8
        self.height = self.max_height / 8
        self.create_squares()

    def start(self, state: str) -> None:
        self.next_state = state
        self.state = "in"

    def create_squares(self):
        n = 0
        for row in range(self.num_rows):
            for col in range(self.num_cols):
                rect = pygame.Rect(
                    self.max_width * col,
                    self.max_height * row,
                    self.width,
                    self.height,
                )
                bottomright = pygame.Rect(
                    self.max_width * col,
                    self.max_height * row,
                    self.max_width,
                    self.max_height,
                ).bottomright
                self.squares[bottomright] = rect

    def trans_in(self):
        if self.width < self.max_width:
            self.width *= self.expand_rate
            self.height *= self.expand_rate
        else:
            if not self.cool_time.tick():
                return
            self.glow.current_state = self.next_state
            self.next_state = None
            self.state = "out"

    def stop(self):
        self.cool_time.reset()
        self.squares.clear()
        self.create_squares()
        self.state = "none"

    def trans_out(self):
        if self.width > 1:
            self.width /= self.expand_rate
            self.height /= self.expand_rate

            for bottomright, square in self.squares.items():
                square.bottomright = bottomright
        else:
            self.stop()

    def update(self):
        if self.state == "none":
            return

        elif self.state == "in":
            self.trans_in()
        elif self.state == "out":
            self.trans_out()

        for square in self.squares.values():
            square.width, square.height = self.width, self.height

    def draw(self):
        if self.state == "none":
            return
        for square in self.squares.values():
            pygame.draw.rect(self.glow.screen, "black", square)
