import pygame
from game.global_state import Global


class Game:
    def __init__(self) -> None:
        self.win_init()

        from game.states import GameState, MenuState

        self.glow.current_state = "menu"
        self.states = {"menu": MenuState, "maingame": GameState}
        self.state = self.states[self.glow.current_state]()
        self.last_current_state = self.glow.current_state

        pygame.display.set_caption("Ping Pong")

    def win_init(self):
        pygame.init()
        self.screen = pygame.display.set_mode(Global.SCRECT.size)
        self.clock = pygame.time.Clock()
        self.glow = Global(events=[], keys=[], dt=0.0, screen=self.screen)
        pygame.display.set_caption("Ping Pong")
        logo = pygame.image.load("assets/logo.jpg")
        pygame.display.set_icon(logo)

    def handle_quit(self) -> None:
        for event in self.glow.events:
            if event.type == pygame.QUIT:
                raise SystemExit

    def update(self) -> None:
        events = pygame.event.get()
        self.glow.events = events
        self.glow.keys = pygame.key.get_pressed()
        self.glow.dt = self.clock.tick(self.glow.FPS) / 1000

        self.handle_quit()

        self.state.update()
        if self.glow.current_state != self.last_current_state:
            self.state = self.states[self.glow.current_state]()
        self.last_current_state = self.glow.current_state

    def draw(self) -> None:
        self.screen.fill((30, 30, 40))

        self.state.draw()
        # pygame.draw.rect(self.screen, "red", (150, 10, 200, 30), width=3)

        pygame.display.update()

    def run(self) -> None:
        while True:
            self.update()
            self.draw()


def main():
    game = Game()
    game.run()
