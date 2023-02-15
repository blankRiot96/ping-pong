import time
import pygame


def circle_surf(color, radius):
    surf = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
    pygame.draw.circle(surf, color, (radius, radius), radius)
    return surf


class Time:
    def __init__(self, seconds: float) -> None:
        self.seconds = seconds
        self.start = time.perf_counter()

    def reset(self):
        self.start = time.perf_counter()

    def tick(self) -> bool:
        end = time.perf_counter()
        if end - self.start > self.seconds:
            self.start = end
            return True
        return False
