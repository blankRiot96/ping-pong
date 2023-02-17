import pygame
from game.global_state import Global
from game.paddles import LeftPaddle, RightPaddle
from game.ball import Ball

from game.main_menu import TitleText, Buttons
from game.powerups import Powerups
from game.helper import Time
from itertools import cycle


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
    WIN_REQ = 50

    def __init__(self) -> None:
        self.glow = Global()
        self.glow.balls = []
        self.glow.left_paddle, self.glow.right_paddle = (LeftPaddle(), RightPaddle())
        self.glow.ball = Ball(50)
        self.dotted_lines.set_alpha(50)
        self.powerups = Powerups()
        self.game_over_surf = pygame.Surface(self.glow.SCRECT.size)
        self.game_over_surf.set_alpha(0)
        self.game_over_alpha = 0
        self.won = False

        self.blue_win_surf = self.game_over_surf.copy()
        self.blue_win_surf.fill("cyan")

        self.red_win_surf = self.game_over_surf.copy()
        self.red_win_surf.fill("red")

        self.font = pygame.font.Font(None, 65)
        Ball.active = True

    def update(self) -> None:
        self.glow.left_paddle.update()
        self.glow.right_paddle.update()
        self.powerups.update()

        self.glow.ball.update()
        if (
            self.glow.left_paddle.score >= self.WIN_REQ
            or self.glow.right_paddle.score >= self.WIN_REQ
        ):
            self.won = True

        if self.won:
            self.on_victory_update()

    def on_victory_update(self):
        self.won = True
        self.glow.left_paddle.active = False
        self.glow.right_paddle.active = False

        Ball.active = False
        if self.game_over_alpha < 100:
            self.game_over_alpha += 10.3 * self.glow.dt

        if self.glow.left_paddle.score >= self.WIN_REQ:
            self.blue_win_surf.set_alpha(self.game_over_alpha)
        elif self.glow.right_paddle.score >= self.WIN_REQ:
            self.red_win_surf.set_alpha(self.game_over_alpha)

        for event in self.glow.events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.glow.current_state = "menu"

    def on_victory_draw(self):
        self.glow.screen.blit(self.blue_win_surf, (0, 0))
        self.glow.screen.blit(self.red_win_surf, (0, 0))
        self.glow.screen.blit(
            self.font.render("Press ENTER to go to main menu", True, "yellow"),
            (10, 100),
        )
        if self.glow.left_paddle.score >= self.WIN_REQ:
            self.glow.screen.blit(
                self.font.render("BLUE WINS", True, "yellow"),
                self.glow.SCRECT.center,
            )
        else:
            self.glow.screen.blit(
                self.font.render("RED WINS", True, "yellow"),
                self.glow.SCRECT.center,
            )

    def draw(self) -> None:
        self.glow.screen.blit(self.dotted_lines, (0, 0))
        self.glow.left_paddle.draw()
        self.glow.right_paddle.draw()
        self.powerups.draw()

        self.glow.ball.draw()

        if self.won:
            self.on_victory_draw()


class IntroState:
    N_PAGES = 9

    def __init__(self) -> None:
        self.glow = Global()
        self.intro_pages = tuple(
            pygame.image.load(f"assets/intro_{n}.png").convert()
            for n in range(1, IntroState.N_PAGES + 1)
        )
        self.index = 0
        self.cooldown = Time(5)
        self.current_page = self.intro_pages[self.index]
        self.font = pygame.font.Font(None, 32)
        self.msg_surf = self.font.render("Press ENTER to go to menu", True, "white")
        self.guide_surf = self.font.render(
            "RIGHT key for next page, LEFT key for prev page", True, "white"
        )

    def next_page(self):
        self.index += 1
        if self.index >= IntroState.N_PAGES:
            self.index = 0

    def prev_page(self):
        self.index -= 1
        if self.index < 0:
            self.index = IntroState.N_PAGES - 1

    def update(self):
        if self.cooldown.tick():
            self.next_page()

        for event in self.glow.events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    self.next_page()
                elif event.key == pygame.K_LEFT:
                    self.prev_page()
                elif event.key == pygame.K_RETURN:
                    self.glow.current_state = "menu"
        self.current_page = self.intro_pages[self.index]

    def draw(self):
        self.glow.screen.blit(self.current_page, (0, 0))
        self.glow.screen.blit(self.msg_surf, (0, 0))
        self.glow.screen.blit(self.guide_surf, (0, 30))
