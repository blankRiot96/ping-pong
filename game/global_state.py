from typing import Self
import pygame


class Global:
    _inst = None

    # Constants
    SCREEN_WIDTH, SCREEN_HEIGHT = (800, 500)
    SCRECT = pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)
    FPS = 60
    screen: pygame.Surface

    def __new__(cls: type[Self], *args, **kwargs) -> Self:
        if Global._inst is None:
            Global._inst = super().__new__(cls)

        return Global._inst

    def __init__(self, **kwargs) -> None:
        self.__dict__.update(kwargs)
