from game.animations import SinWave
import pygame
from game.global_state import Global


class TitleText:
    def __init__(self) -> None:
        self.glow = Global()
        self.wave = SinWave(0.03)
        self.font = pygame.font.Font(None, 75)
        self.text = "Ping Pong"
        self.surf = self.font.render(self.text, True, "white")
        self.rect = self.surf.get_rect(center=self.glow.SCRECT.center)
        self.pos = pygame.Vector2(self.rect.topleft[0], self.rect.topleft[1] - 150)
        self.speed_scalar = 20

    def update(self):
        self.pos.y += self.glow.dt * self.wave.val() * self.speed_scalar

    def draw(self):
        self.glow.screen.blit(self.surf, self.pos)


class Button:
    FONT = pygame.font.Font(None, 40)
    PAD_Y = -50
    PAD_SEGMENT = 20
    SPACE_Y = 20
    HOVER_SPEED = 30

    def __init__(self, title: str, statename: str = "") -> None:
        self.title = title
        self.glow = Global()
        self.wave = SinWave(0.1)
        self.gen_title("white")
        self.rect = self.surf.get_rect(center=self.glow.SCRECT.center)
        self.rect.y += Button.PAD_Y + Button.SPACE_Y
        Button.SPACE_Y += self.rect.height + Button.PAD_SEGMENT
        self.pos = pygame.Vector2(self.rect.topleft)
        self.original_pos = self.pos.copy()
        self.statename = statename

    def gen_title(self, color):
        self.color = color
        self.surf = self.FONT.render(self.title, True, color)

    def handle_selection(self):
        for event in self.glow.events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.glow.current_state = self.statename

    def update(self):
        if self.color == "yellow":
            self.pos.y += self.wave.val() * self.HOVER_SPEED * self.glow.dt
            self.handle_selection()
        else:
            self.pos = self.original_pos.copy()

        self.rect.topleft = self.pos

    def draw(self):
        self.glow.screen.blit(self.surf, self.rect)


class Buttons:
    def __init__(self) -> None:
        self.btns = [
            Button("< Play >", statename="maingame"),
            Button("< Settings >"),
            Button("< Credits >"),
        ]
        self.current_btn_index = 0
        self.glow = Global()

    @property
    def current_btn_index(self):
        return self.__current_btn_index

    @current_btn_index.setter
    def current_btn_index(self, val):
        if val < 0:
            val = len(self.btns) - 1
        if val >= len(self.btns):
            val = 0
        self.__current_btn_index = val
        self.current_btn = self.btns[self.current_btn_index]
        self.current_btn.gen_title("yellow")

    def update(self):
        for event in self.glow.events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.current_btn_index -= 1
                elif event.key == pygame.K_DOWN:
                    self.current_btn_index += 1

        for index, btn in enumerate(self.btns):
            if index != self.current_btn_index and btn.color != "white":
                btn.gen_title("white")
            btn.update()

    def draw(self):
        for btn in self.btns:
            btn.draw()
