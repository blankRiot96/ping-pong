import pygame, random, math
from game.global_state import Global
from game.animations import BallParticle
from game.helper import circle_surf


def get_dv(rad):
    dx = math.cos(rad)
    dy = math.sin(rad)

    return pygame.Vector2(dx, dy)


def get_rand_offset(scale_factor: float) -> float:
    return random.uniform(-1, 1) * scale_factor


def get_right_paddle_fallback() -> float:
    return random.uniform(2 * math.pi / 3, (4 * math.pi) / 3)


class BallTrail:
    def __init__(self) -> None:
        self.glow = Global()
        self.particles: list[BallParticle] = list()
        self.particles_per_tick = 3

    def update(self):
        for _ in range(self.particles_per_tick):
            self.particles.append(
                BallParticle(
                    get_rand_offset(self.glow.ball.size / 3),
                    get_rand_offset(self.glow.ball.size / 3),
                )
            )

        for particle in list(self.particles):
            particle.update()
            if not particle.alive:
                self.particles.remove(particle)

    def draw(self):
        for particle in self.particles:
            particle.draw()


class Ball:
    active = True
    ORIGINAL_COLOR = (0, 200, 0)

    def __init__(self, size, mini: bool = False) -> None:
        self.mini = mini
        self.size = size
        self.color = Ball.ORIGINAL_COLOR
        self.size_tup = size, size
        self.glow = Global()
        self.create_image()
        self.hitbox = self.image.get_rect(center=self.glow.SCRECT.center)
        self.pos = pygame.Vector2(self.glow.SCRECT.center)
        self.rad = random.uniform(0, 2 * math.pi)
        self.speed = 350.2
        self.original_speed = self.speed
        self.dv = pygame.Vector2()
        self.alive = True
        self.trail = None if mini else BallTrail()
        self.create_glow()
        self.swap_facto = 1

    def create_image(self):
        self.image = pygame.Surface(self.size_tup, pygame.SRCALPHA)
        pygame.draw.circle(
            self.image, self.color, (self.size / 2, self.size / 2), self.size / 2
        )

    def mirror_swap(self):
        self.dv.x *= self.swap_facto
        self.dv.y *= self.swap_facto

    def create_glow(self):
        self.glow_surf = circle_surf(BallParticle.GLOW_COLOR, (self.size / 2) * 1.5)
        self.glow_rect = self.glow_surf.get_rect(center=self.pos)

    def collide_left_paddle(self):
        if not self.hitbox.colliderect(self.glow.left_paddle.rect):
            return

        choices = (0, math.pi / 3), (0, math.pi * 5 / 3)
        choice = random.choice(choices)

        self.rad = random.uniform(*choice)
        self.mirror_swap()

    def collide_right_paddle(self):
        if self.hitbox.colliderect(self.glow.right_paddle.rect):
            self.rad = get_right_paddle_fallback()
            self.mirror_swap()

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
        dv.x *= self.glow.dt * self.speed
        dv.y *= self.glow.dt * self.speed
        self.dv = dv

    def finalize_pos(self):
        self.pos += self.dv
        self.hitbox.center = self.pos

    def update_score(self):
        if self.hitbox.left < 0:
            self.glow.right_paddle.score += 1 if self.mini else 10
            self.alive = False
        elif self.hitbox.right > self.glow.SCREEN_WIDTH:
            self.glow.left_paddle.score += 1 if self.mini else 10
            self.alive = False

    def bounce_around(self):
        if self.hitbox.left < 0:
            self.alive = False
        elif self.hitbox.right > self.glow.SCREEN_WIDTH:
            self.alive = False

    def on_mini_ball_death(self):
        if not self.alive:
            self.glow.balls.remove(self)

    def on_death(self):
        if self.mini:
            self.on_mini_ball_death()
            return
        if not self.alive:
            pygame.event.post(self.glow.BALL_DEATH_EVENT)
            self.glow.ball = type(self)(50)

    def on_active(self):
        if Ball.active:
            self.update_score()
        else:
            self.bounce_around()

    def trail_handler(self):
        if not self.mini:
            self.trail.update()

    def update(self):
        self.move()
        self.collide_bottom()
        self.collide_top()
        self.collide_left_paddle()
        self.collide_right_paddle()
        self.on_active()
        self.on_death()
        self.trail_handler()
        self.create_glow()
        self.finalize_pos()

    def draw(self):
        self.glow.screen.blit(self.image, self.hitbox)

        if not self.mini:
            self.trail.draw()
        self.glow.screen.blit(
            self.glow_surf, self.glow_rect, special_flags=pygame.BLEND_RGB_ADD
        )
        # pygame.draw.rect(self.glow.screen, "red", self.hitbox, width=3)
