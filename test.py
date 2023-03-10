import pygame

pygame.init()
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
bg_color = (255, 255, 255)
clock = pygame.time.Clock()

from game.helper import Time


class Transition:
    def __init__(self) -> None:
        self.num_rows = 3
        self.num_cols = 4
        self.max_size = width / self.num_cols
        self.squares: dict[tuple, pygame.Rect] = {}
        self.create_squares()
        self.state = "in"
        self.cool_time = Time(2.2)

        self.expand_rate = 1.05
        self.size = 1

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
            self.state = "out"

    def trans_out(self):
        if self.size > 1:
            self.size /= self.expand_rate
            for bottomright, square in self.squares.items():
                square.bottomright = bottomright
        else:
            self.cool_time.reset()
            self.create_squares()
            self.state = "in"

    def update(self):
        if self.state == "none":
            return

        elif self.state == "in":
            self.trans_in()
        elif self.state == "out":
            self.trans_out()

        for square in self.squares.values():
            square.width, square.height = self.size, self.size

    def draw(self, screen):
        for square in self.squares.values():
            pygame.draw.rect(screen, "black", square)


transition = Transition()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill(bg_color)
    transition.update()
    transition.draw(screen)

    pygame.display.update()
    clock.tick(60)
pygame.quit()
