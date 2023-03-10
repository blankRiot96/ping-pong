import pygame
from game.global_state import Global
from game.transitions import Transition


class Game:
    def __init__(self) -> None:
        self.win_init()

        from game.states import GameState, MenuState, IntroState

        self.glow.transition = Transition()
        self.glow.current_state = "intro"
        self.states = {"menu": MenuState, "maingame": GameState, "intro": IntroState}
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
        self.glow.dt = min(self.glow.dt, 0.01)

        self.handle_quit()

        self.glow.transition.update()
        self.state.update()
        if self.glow.current_state != self.last_current_state:
            self.state = self.states[self.glow.current_state]()
        self.last_current_state = self.glow.current_state

    def draw(self) -> None:
        self.screen.fill((30, 30, 40))

        self.state.draw()
        # pygame.draw.rect(self.screen, "red", (10, 50, 150, 20), width=3)

        self.glow.transition.draw()
        pygame.display.update()

    def run(self) -> None:
        while True:
            self.update()
            self.draw()


def main():
    game = Game()
    game.run()
