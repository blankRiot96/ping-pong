import pygame

WIDTH = 800
HEIGHT = 600
FPS = 60


class Paddle(pygame.sprite.Sprite):
    def __init__(self, friction=0.1, initial_speed=0.0):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((20, 100))
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH - 20
        self.rect.centery = HEIGHT / 2
        self.speed = initial_speed
        self.friction = friction

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.speed -= 0.05
        elif keys[pygame.K_DOWN]:
            self.speed += 0.05
        elif abs(self.speed) > 0:
            self.speed -= self.speed * self.friction

        self.rect.y += self.speed
        self.rect.y = max(0, min(HEIGHT - self.rect.height, self.rect.y))


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

all_sprites = pygame.sprite.Group()
paddle = Paddle()
all_sprites.add(paddle)

running = True
while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    all_sprites.update()
    screen.fill((0, 0, 0))
    all_sprites.draw(screen)
    pygame.display.flip()

pygame.quit()
