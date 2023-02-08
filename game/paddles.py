import abc
import pygame
from game.global_state import Global
from game.helper import Time


class Paddle(abc.ABC):
    SIZE = 25, 90
    PAD = 10
    MAXSPEED = 250.3

    def __init__(self) -> None:
        super().__init__()
        self.glow = Global()
        self.speed = 0.0
        self.__score = 0
        self.font = pygame.font.Font(None, 40)
        self.score_surf = self.font.render(str(self.__score), True, "white")
        self.energy = 100
        self.energy_cooldown = Time(1)

    @property
    def score(self):
        return self.__score

    @score.setter
    def score(self, val):
        self.__score = val
        self.score_surf = self.font.render(str(self.__score), True, "white")

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

        if self.energy_cooldown.tick():
            self.energy += 1
            if self.energy >= 100:
                self.energy = 100

    def draw(self) -> None:
        self.glow.screen.blit(self.image, self.pos)
        self.glow.screen.blit(self.score_surf, (self.pos.x, 20))


class LeftPaddle(Paddle):
    UP_CONTROL = pygame.K_w
    DOWN_CONTROL = pygame.K_s
    LEFT_CONTROL = pygame.K_a
    RIGHT_CONTROL = pygame.K_d

    COLOR = "blue"

    def __init__(self) -> None:
        super().__init__()
        self.image = pygame.Surface(self.SIZE)
        self.image.fill(self.COLOR)
        self.rect = self.image.get_rect(centery=self.glow.SCRECT.centery)
        self.rect.x = self.PAD
        self.pos = pygame.Vector2(self.rect.topleft)

    def update(self) -> None:
        super().update()


class RightPaddle(Paddle):
    UP_CONTROL = pygame.K_UP
    DOWN_CONTROL = pygame.K_DOWN
    LEFT_CONTROL = pygame.K_LEFT
    RIGHT_CONTROL = pygame.K_RIGHT

    COLOR = "red"

    def __init__(self) -> None:
        super().__init__()
        self.image = pygame.Surface(self.SIZE)
        self.image.fill(self.COLOR)
        self.rect = self.image.get_rect(centery=self.glow.SCRECT.centery)
        self.rect.x = self.glow.SCRECT.width - self.rect.width - self.PAD
        self.pos = pygame.Vector2(self.rect.topleft)
