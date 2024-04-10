import pygame

pygame.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Frog game')

clock = pygame.time.Clock()
background = pygame.surface.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
net = pygame.surface.Surface((25, 200))
net_rect = net.get_rect(midbottom=(SCREEN_WIDTH/2, SCREEN_HEIGHT))
net.fill('green')


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        height = 50
        width = 50
        self.gravity = 0
        self.image = pygame.surface.Surface((width, height))
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH/3, SCREEN_HEIGHT - height/2)
        self.image.fill('red')

    def update(self):
        self.gravity += 0.5
        self.rect.bottom += self.gravity
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
        if self.rect.right >= SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        elif self.rect.left <= 0:
            self.rect.left = 0
        if self.rect.right >= net_rect.left:
            self.rect.right = net_rect.left

    def movement(self, keys):
        if keys[pygame.K_LEFT]:
            self.rect.left -= 5
        if keys[pygame.K_RIGHT]:
            self.rect.right += 5
        if keys[pygame.K_UP] and self.rect.bottom >= SCREEN_HEIGHT:
            self.gravity = -10


class Player2(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        height = 50
        width = 50
        self.gravity = 0
        self.image = pygame.surface.Surface((width, height))
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH - (SCREEN_WIDTH/3), SCREEN_HEIGHT - height/2)
        self.image.fill('blue')

    def update(self):
        self.gravity += 0.5
        self.rect.bottom += self.gravity
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
        if self.rect.right >= SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        elif self.rect.left <= 0:
            self.rect.left = 0
        if self.rect.left <= net_rect.right:
            self.rect.left = net_rect.right

    def movement(self, keys):
        if keys[pygame.K_q]:
            self.rect.left -= 5
        if keys[pygame.K_d]:
            self.rect.right += 5
        if keys[pygame.K_z] and self.rect.bottom >= SCREEN_HEIGHT:
            self.gravity = -10


player = Player()
player2 = Player2()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    keys_input = pygame.key.get_pressed()
    screen.blit(background, (0, 0))
    screen.blit(player.image, player.rect)
    screen.blit(net, net_rect)
    player.movement(keys_input)
    player.update()
    screen.blit(player2.image, player2.rect)
    player2.movement(keys_input)
    player2.update()
    pygame.display.update()
    clock.tick(65)
