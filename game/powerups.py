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
        self.selected_image = self.get_selected_image()
        self.rect = self.image.get_rect()
        self.title = title
        self.__pos = pygame.Vector2()
        self.active = False

    def get_selected_image(self):
        px_array = pygame.PixelArray(self.default_image.copy())
        px_array.replace((255, 255, 255), (255, 255, 0))
        return px_array.make_surface()

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
    DURATION = 3

    def __init__(self, paddle) -> None:
        image = pygame.image.load("assets/longer-bat.png").convert_alpha()
        title = "Longer Bat"
        energy_cost = 25
        super().__init__(image, title, energy_cost, paddle)

        self.duration_timer = Time(LongBat.DURATION)

    def on_choose(self) -> None:
        super().on_choose()
        self.duration_timer.reset()

    def update(self):
        super().update()

        if self.active:
            self.paddle.image = pygame.Surface(
                (self.paddle.SIZE[0], self.paddle.SIZE[1] + 50)
            )
            self.paddle.rect = self.paddle.image.get_rect(topleft=self.paddle.pos)
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

        self.current_powerup_index = {"left": 0, "right": 0}
        self.paddle_keys = {
            self.glow.left_paddle: "left",
            self.glow.right_paddle: "right",
        }

        self.all_powerups = self.left_paddle_powerups + self.right_paddle_powerups

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

    def consume_keys(self, event: pygame.event.Event) -> None:
        for paddle in self.glow.left_paddle, self.glow.right_paddle:
            if event.key == paddle.LEFT_CONTROL:
                self.current_powerup_index[self.paddle_keys[paddle]] -= 1
                if self.current_powerup_index[self.paddle_keys[paddle]] < 0:
                    self.current_powerup_index[self.paddle_keys[paddle]] = (
                        len(self.left_paddle_powerups) - 1
                    )

            elif event.key == paddle.RIGHT_CONTROL:
                self.current_powerup_index[self.paddle_keys[paddle]] += 1
                if self.current_powerup_index[self.paddle_keys[paddle]] >= len(
                    self.left_paddle_powerups
                ):
                    self.current_powerup_index[self.paddle_keys[paddle]] = 0

    def on_enter(self, event: pygame.event.Event) -> None:
        if event.key == pygame.K_q:
            self.left_paddle_powerups[self.current_powerup_index["left"]].on_choose()
        elif event.key == pygame.K_RETURN:
            self.right_paddle_powerups[self.current_powerup_index["right"]].on_choose()

    def update(self):
        for index, powerup in enumerate(self.left_paddle_powerups):
            if index == self.current_powerup_index["left"]:
                powerup.image = pygame.transform.scale(powerup.selected_image, (60, 60))
                continue
            powerup.image = powerup.default_image.copy()

        for index, powerup in enumerate(self.right_paddle_powerups):
            if index == self.current_powerup_index["right"]:
                powerup.image = pygame.transform.scale(powerup.selected_image, (60, 60))
                continue
            powerup.image = powerup.default_image.copy()

        for event in self.glow.events:
            if event.type == pygame.KEYDOWN:
                self.consume_keys(event)
                self.on_enter(event)

        for powerup in self.all_powerups:
            powerup.update()

    def draw(self):
        for powerup in self.all_powerups:
            powerup.draw()
