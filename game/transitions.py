from game.helper import Time
import pygame
from game.global_state import Global


class Transition:
    def __init__(self) -> None:
        self.glow = Global()
        self.num_rows = 3
        self.num_cols = 4
        self.max_size = self.glow.SCREEN_WIDTH / self.num_cols
        self.squares: dict[tuple, pygame.Rect] = {}
        self.create_squares()
        self.state = "none"
        self.next_state = None
        self.cool_time = Time(2.2)

        self.expand_rate = 1.05
        self.size = 1

    def start(self, state: str) -> None:
        self.next_state = state
        self.state = "in"

    def create_squares(self):
        n = 0
        for row in range(self.num_rows):
            for col in range(self.num_cols):
                rect = pygame.Rect(
                    self.max_size * col,
                    self.max_size * row,
                    self.max_size,
                    self.max_size,
                )
                bottomright = rect.bottomright
                self.squares[bottomright] = rect

    def trans_in(self):
        if self.size < self.max_size:
            self.size *= self.expand_rate
        else:
            if not self.cool_time.tick():
                return
            self.glow.current_state = self.next_state
            self.next_state = None
            self.state = "out"

    def stop(self):
        self.cool_time.reset()
        self.create_squares()
        self.state = "none"

    def trans_out(self):
        if self.size > 1:
            self.size /= self.expand_rate
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
            square.width, square.height = self.size, self.size

    def draw(self):
        if self.state == "none":
            return
        for square in self.squares.values():
            pygame.draw.rect(self.glow.screen, "black", square)
