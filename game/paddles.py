import abc
import pygame
from game.global_state import Global


class Paddle(abc.ABC):
    SIZE = 25, 90
    PAD = 10
    MAXSPEED = 250.3

    def __init__(self) -> None:
        super().__init__()
        self.glow = Global()
        self.speed = 0.0

    def update(self) -> None:
        self.update_pos()

    def update_pos(self):
        keys = self.glow.keys
        dt = self.glow.dt
        if keys[self.UP_CONTROL]:
            self.pos.y -= self.MAXSPEED * dt
        elif keys[self.DOWN_CONTROL]:
            self.pos.y += self.MAXSPEED * dt

        self.rect.topleft = self.pos

    def draw(self) -> None:
        self.glow.screen.blit(self.image, self.pos)


class LeftPaddle(Paddle):
    UP_CONTROL = pygame.K_w
    DOWN_CONTROL = pygame.K_s

    def __init__(self) -> None:
        super().__init__()
        self.image = pygame.Surface(self.SIZE)
        self.image.fill("blue")
        self.rect = self.image.get_rect(centery=self.glow.SCRECT.centery)
        self.rect.x = self.PAD
        self.pos = pygame.Vector2(self.rect.topleft)


class RightPaddle(Paddle):
    UP_CONTROL = pygame.K_UP
    DOWN_CONTROL = pygame.K_DOWN

    def __init__(self) -> None:
        super().__init__()
        self.image = pygame.Surface(self.SIZE)
        self.image.fill("red")
        self.rect = self.image.get_rect(centery=self.glow.SCRECT.centery)
        self.rect.x = self.glow.SCRECT.width - self.rect.width - self.PAD
        self.pos = pygame.Vector2(self.rect.topleft)
