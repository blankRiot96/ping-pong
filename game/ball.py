import pygame, random, math
from game.global_state import Global


def get_dv(rad):
    dx = math.cos(rad)
    dy = math.sin(rad)

    return pygame.Vector2(dx, dy)


class Ball:
    def __init__(self, size) -> None:
        self.size = size
        self.size_tup = size, size
        self.glow = Global()
        self.image = pygame.Surface(self.size_tup, pygame.SRCALPHA)
        pygame.draw.circle(self.image, "white", (size / 2, size / 2), size / 2)
        self.hitbox = self.image.get_rect(center=self.glow.SCRECT.center)
        self.pos = pygame.Vector2(self.glow.SCRECT.center)
        self.rad = random.uniform(0, 2 * math.pi)
        self.speed = 350.2
        self.dv = pygame.Vector2()
        self.alive = True

    def collide_left_paddle(self):
        if not self.hitbox.colliderect(self.glow.left_paddle.rect):
            return

        choices = (0, math.pi / 3), (0, math.pi * 5 / 3)
        choice = random.choice(choices)

        self.rad = random.uniform(*choice)

    def collide_right_paddle(self):
        if self.hitbox.colliderect(self.glow.right_paddle.rect):
            self.rad = random.uniform(2 * math.pi / 3, (4 * math.pi) / 3)

    def collide_bottom(self):
        if not (self.pos.y > self.glow.SCREEN_HEIGHT - (self.size / 2)):
            return

        if self.dv.x > 0.0:
            self.rad = random.uniform(11 * math.pi / 6, 5 * math.pi / 3)
        else:
            self.rad = random.uniform(7 * math.pi / 6, 4 * math.pi / 3)

    def collide_top(self):
        if not (self.pos.y < 0 + (self.size / 2)):
            return

        if self.dv.x > 0.0:
            self.rad = random.uniform(math.pi / 6, math.pi / 3)
        else:
            self.rad = random.uniform(2 * math.pi / 3, 5 * math.pi / 6)

    def move(self):
        dv = get_dv(self.rad)
        self.dv = dv
        dv.x *= self.glow.dt * self.speed
        dv.y *= self.glow.dt * self.speed
        self.pos += dv
        self.hitbox.center = self.pos

    def update_score(self):
        if self.hitbox.left < 0:
            self.glow.right_paddle.score += 1
            self.alive = False
        elif self.hitbox.right > self.glow.SCREEN_WIDTH:
            self.glow.left_paddle.score += 1
            self.alive = False

    def on_death(self):
        if not self.alive:
            self.glow.ball = type(self)(50)

    def update(self):
        self.move()
        self.collide_left_paddle()
        self.collide_right_paddle()
        self.collide_bottom()
        self.collide_top()
        self.update_score()
        self.on_death()

    def draw(self):
        self.glow.screen.blit(self.image, self.hitbox)
        # pygame.draw.rect(self.glow.screen, "red", self.hitbox, width=3)
