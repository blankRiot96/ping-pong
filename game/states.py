import pygame
from game.global_state import Global
from game.paddles import LeftPaddle, RightPaddle
from game.ball import Ball

from game.main_menu import TitleText, Buttons
from game.powerups import Powerups


class MenuState:
    def __init__(self) -> None:
        self.glow = Global()
        self.title_text = TitleText()
        self.buttons = Buttons()

    def update(self):
        self.title_text.update()
        self.buttons.update()

    def draw(self):
        self.title_text.draw()
        self.buttons.draw()


class GameState:
    dotted_lines = pygame.image.load("assets/dotted.png").convert_alpha()

    def __init__(self) -> None:
        self.glow = Global()
        self.glow.left_paddle, self.glow.right_paddle = (LeftPaddle(), RightPaddle())
        self.glow.ball = Ball(50)
        self.dotted_lines.set_alpha(50)
        self.powerups = Powerups()

    def update(self) -> None:
        self.glow.left_paddle.update()
        self.glow.right_paddle.update()
        self.powerups.update()

        self.glow.ball.update()

    def on_victory(self):
        if 7 in (self.glow.left_paddle.score, self.glow.right_paddle.score):
            self.glow.current_state = "menu"

    def draw(self) -> None:
        self.glow.screen.blit(self.dotted_lines, (0, 0))
        self.glow.left_paddle.draw()
        self.glow.right_paddle.draw()
        self.powerups.draw()

        self.glow.ball.draw()
        self.on_victory()
