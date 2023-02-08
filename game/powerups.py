import abc
import pygame
from game.global_state import Global
from game.helper import Time


class Powerup(abc.ABC):
    def __init__(
        self, image: pygame.Surface, title: str, energy_cost: int, paddle
    ) -> None:
        super().__init__()
        self.paddle = paddle
        self.glow = Global()
        self.energy_cost = energy_cost
        self.image = image
        self.default_image = self.image.copy()
        # self.selected_image =
        self.rect = self.image.get_rect()
        self.title = title
        self.__pos = pygame.Vector2()
        self.active = False

    @property
    def pos(self) -> pygame.Vector2:
        return self.__pos

    @pos.setter
    def pos(self, val):
        self.__pos = val
        self.rect.topleft = self.pos

    def on_choose(self) -> None:
        if self.paddle.energy < self.energy_cost:
            return

        self.paddle.energy -= self.energy_cost
        self.active = True

    def on_mouse_button_down(self, event: pygame.event.Event):
        if self.rect.collidepoint(event.pos):
            self.on_choose()

    def update(self):
        for event in self.glow.events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.on_mouse_button_down(event)

    def draw(self):
        self.glow.screen.blit(self.image, self.rect)


class LongBat(Powerup):
    def __init__(self, paddle) -> None:
        image = pygame.image.load("assets/longer-bat.png").convert_alpha()
        title = "Longer Bat"
        energy_cost = 25
        super().__init__(image, title, energy_cost, paddle)

        self.duration_timer = Time(3)

    def update(self):
        super().update()

        if self.active:
            self.paddle.image = pygame.Surface(
                (self.paddle.SIZE[0], self.paddle.SIZE[1] + 50)
            )
            self.paddle.image.fill(self.paddle.COLOR)
            if self.duration_timer.tick():
                self.active = False
        else:
            self.paddle.image = pygame.Surface(self.paddle.SIZE)
            self.paddle.image.fill(self.paddle.COLOR)


class LightningBall(Powerup):
    def __init__(self, paddle) -> None:
        image = pygame.image.load("assets/lightning-ball.png").convert_alpha()
        title = "Lightning Ball"
        energy_cost = 50
        super().__init__(image, title, energy_cost, paddle)


class MuliBall(Powerup):
    def __init__(self, paddle) -> None:
        image = pygame.image.load("assets/multi-balls.png").convert_alpha()
        title = "Multi Balls"
        energy_cost = 50
        super().__init__(image, title, energy_cost, paddle)


class MirrorPaddles(Powerup):
    def __init__(self, paddle) -> None:
        image = pygame.image.load("assets/mirror-paddle.png").convert_alpha()
        title = "Mirror Paddle"
        energy_cost = 100
        super().__init__(image, title, energy_cost, paddle)


class Powerups:
    def __init__(self) -> None:
        self.glow = Global()
        self.left_paddle_powerups = (
            LongBat(self.glow.left_paddle),
            LightningBall(self.glow.left_paddle),
            MuliBall(self.glow.left_paddle),
            MirrorPaddles(self.glow.left_paddle),
        )

        self.right_paddle_powerups = (
            LongBat(self.glow.right_paddle),
            LightningBall(self.glow.right_paddle),
            MuliBall(self.glow.right_paddle),
            MirrorPaddles(self.glow.right_paddle),
        )

        self.set_positions()

    def set_positions(self):
        initial_left_pos = pygame.Vector2(50, 400)
        horizontal_padding = [20, 0]
        spacing = 70
        for powerup in self.left_paddle_powerups:
            powerup.pos = initial_left_pos + horizontal_padding
            horizontal_padding[0] += spacing

        initial_right_pos = pygame.Vector2(150, 400)
        for powerup in self.right_paddle_powerups:
            powerup.pos = initial_right_pos + horizontal_padding
            horizontal_padding[0] += spacing

    def update(self):
        for powerup in self.left_paddle_powerups:
            powerup.update()

        for powerup in self.right_paddle_powerups:
            powerup.update()

    def draw(self):
        for powerup in self.left_paddle_powerups:
            powerup.draw()

        for powerup in self.right_paddle_powerups:
            powerup.draw()
