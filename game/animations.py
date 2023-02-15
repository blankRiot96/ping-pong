from __future__ import annotations

import math
import pygame
from game.global_state import Global
from game.helper import circle_surf


class SinWave:
    def __init__(self, speed: float) -> None:
        self.rad = 0.0
        self.speed = speed

    def val(self) -> float:
        self.rad += self.speed
        if self.rad >= 2 * math.pi:
            self.rad = 0

        return math.sin(self.rad)


class BallParticle:
    SIZE_DECREASE = 5
    GLOW_COLOR = (20, 20, 20)

    def __init__(self, x: float, y: float) -> None:
        self.color = "green"
        self.pos = pygame.Vector2()
        self.rand_offset = pygame.Vector2(x, y)
        self.offset = pygame.Vector2(0, 0)
        self.glow = Global()
        self.de_factor = 4
        self.radius = 5
        self.alive = True
        self.create_glow()
        self.surf = pygame.Surface((self.radius * 2, self.radius * 2))
        self.surf.fill("white")
        self.rect = self.surf.get_rect(center=self.pos + self.offset + self.rand_offset)

    def create_glow(self):
        self.glow_surf = circle_surf(BallParticle.GLOW_COLOR, self.radius * 2.5)
        self.glow_rect = self.glow_surf.get_rect(
            center=self.pos + self.offset + self.rand_offset
        )

    def update(self):
        self.pos = self.glow.ball.pos.copy()
        self.offset.x += -self.glow.ball.dv.x / self.de_factor
        self.offset.y += -self.glow.ball.dv.y / self.de_factor
        self.radius -= self.SIZE_DECREASE * self.glow.dt

        self.rand_offset.move_towards_ip((0, 0), 10 * self.glow.dt)
        self.surf = pygame.Surface((self.radius * 2, self.radius * 2))
        self.surf.fill(self.glow.ball.color)
        self.rect = self.surf.get_rect(center=self.pos + self.offset + self.rand_offset)

        self.create_glow()
        if self.radius < 0:
            self.alive = False

    def draw(self):
        self.glow.screen.blit(self.surf, self.rect)
        self.glow.screen.blit(
            self.glow_surf, self.glow_rect, special_flags=pygame.BLEND_RGB_ADD
        )
