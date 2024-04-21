import pygame

pygame.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Froggy volley')

clock = pygame.time.Clock()
game_run = True
game_pause = False
pause_font = pygame.font.Font('FONT/flappy-font.ttf', 50)
background = pygame.transform.rotozoom(pygame.image.load('assets/img.png'), 0, 1.5)
net = pygame.image.load('assets/net.png')
net_rect = net.get_rect(midbottom=(SCREEN_WIDTH/2, SCREEN_HEIGHT + 125))
pause_txt = pause_font.render('PAUSE', True, 'white')
pause_txt_rect = pause_txt.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
start_time = 0
p1_score = 0
p2_score = 0
p1_score_txt = pause_font.render(str(p1_score), True, 'black')
p1_score_txt_rect = p1_score_txt.get_rect(center=(SCREEN_WIDTH/3, SCREEN_HEIGHT - 50))
p2_score_txt = pause_font.render(str(p2_score), True, 'black')
p2_score_txt_rect = p2_score_txt.get_rect(center=(SCREEN_WIDTH/3, SCREEN_HEIGHT - 50))


class Ball(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.gravity = 0
        self.x_velocity = 5
        self.image = pygame.transform.rotozoom(pygame.image.load('assets/ball.png'), 0, 0.5)
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH/2, SCREEN_HEIGHT/2)

    def update(self):
        global p1_score, p2_score
        self.gravity += 0.7
        self.rect.bottom += self.gravity
        self.rect.centerx += self.x_velocity
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.gravity = 0
            if self.rect.centerx > SCREEN_WIDTH/2:
                self.x_velocity = -5
                p1_score += 1
            else:
                p2_score += 1
                self.x_velocity = 5
            self.rect.center = (SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
        if self.rect.clipline((net_rect.x, net_rect.y), net_rect.topright) and self.gravity == abs(self.gravity):
            self.gravity = -20
        if self.rect.clipline((net_rect.x, net_rect.y + 10), net_rect.bottomleft):
            self.gravity = -12
            self.x_velocity = 5
        elif self.rect.clipline((net_rect.topright[0], net_rect.topright[1] + 10), net_rect.bottomright):
            self.gravity = -12
            self.x_velocity = -5
        if self.rect.right >= SCREEN_WIDTH:
            self.x_velocity = -self.x_velocity
        elif self.rect.left <= 0:
            self.x_velocity = abs(self.x_velocity)
        if self.x_velocity > 12:
            self.x_velocity = 9
        elif self.x_velocity < -12:
            self.x_velocity = -9


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.player_indication = pygame.transform.rotozoom(pygame.image.load('assets/player1-indication.png'), 0, 0.2)
        self.gravity = 0
        self.image = pygame.transform.rotozoom(pygame.image.load('assets/player1.png'), 0, 0.2)
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH/3, SCREEN_HEIGHT - self.rect.centery)
        self.player_indication_rect = self.player_indication.get_rect(midbottom=self.rect.midtop)

    def update(self):
        self.player_indication_rect = self.player_indication.get_rect(midbottom=self.rect.midtop)
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
        if keys[pygame.K_q]:
            self.rect.left -= 7
        if keys[pygame.K_d]:
            self.rect.right += 7
        if keys[pygame.K_z] and self.rect.bottom >= SCREEN_HEIGHT:
            self.gravity = -10


class Player2(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        height = 50
        width = 50
        self.gravity = 0
        self.image = pygame.transform.rotozoom(pygame.image.load('assets/player2.png'), 0, 0.56)
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH - (SCREEN_WIDTH/3), SCREEN_HEIGHT - height/2)
        self.player_indication = pygame.transform.rotozoom(pygame.image.load('assets/player2-indication.png'), 0, 0.2)
        self.player_indication_rect = self.player_indication.get_rect(midbottom=self.rect.midtop)

    def update(self):
        self.player_indication_rect = self.player_indication.get_rect(midbottom=self.rect.midtop)
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
        if keys[pygame.K_LEFT]:
            self.rect.left -= 7
        if keys[pygame.K_RIGHT]:
            self.rect.right += 7
        if keys[pygame.K_UP] and self.rect.bottom >= SCREEN_HEIGHT:
            self.gravity = -10


player = Player()
player2 = Player2()
ball = Ball()


def player_collision(keys):
    if ball.rect.colliderect(player2):
        ball.gravity = -20
        ball.x_velocity = -ball.x_velocity
        if keys[pygame.K_RIGHT] or player2.rect.bottom > SCREEN_HEIGHT:
            ball.x_velocity -= 2
            print(ball.x_velocity)
        elif not keys[pygame.K_q]:
            print(ball.x_velocity)
    if ball.rect.colliderect(player):
        player.state = False
        ball.gravity = -20
        ball.x_velocity = abs(ball.x_velocity)
        if keys[pygame.K_q] and player.rect.bottom < SCREEN_HEIGHT:
            ball.x_velocity += 2
        else:
            pass
    else:
        player.state = True


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if game_run:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                game_run = False
                game_pause = True
        elif game_pause:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                game_run = True
                game_pause = False
    if game_pause:
        screen.blit(pause_txt, pause_txt_rect)
    if game_run:
        p1_score_txt = pause_font.render(str(p1_score), True, 'black')
        p1_score_txt_rect = p1_score_txt.get_rect(center=(SCREEN_WIDTH / 3, SCREEN_HEIGHT/2))
        p2_score_txt = pause_font.render(str(p2_score), True, 'black')
        p2_score_txt_rect = p2_score_txt.get_rect(center=(SCREEN_WIDTH - (SCREEN_WIDTH/3), SCREEN_HEIGHT/2))
        keys_input = pygame.key.get_pressed()
        player_collision(keys_input)
        screen.blit(background, (0, 0))
        screen.blit(player.image, player.rect)
        screen.blit(net, net_rect)
        player.movement(keys_input)
        player.update()
        screen.blit(player2.image, player2.rect)
        player2.movement(keys_input)
        player2.update()
        screen.blit(p1_score_txt, p1_score_txt_rect)
        screen.blit(p2_score_txt, p2_score_txt_rect)
        screen.blit(player.player_indication, player.player_indication_rect)
        screen.blit(player2.player_indication, player2.player_indication_rect)
        screen.blit(ball.image, ball.rect)
        ball.update()
    pygame.display.update()
    clock.tick(70)
