import sys, pygame
import random

from pygame.locals import (
    QUIT,
    K_ESCAPE,
    KEYDOWN,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT)
    
SW = 800
SH = 600

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.Surface((50, 50))
        self.surf.fill((210, 180, 140))
        self.rect = self.surf.get_rect(
                center = ((SW/2, SH/2))
            )
        
    def update(self, pk):
        if pk[K_UP]:
            self.rect.move_ip(0, -2)
        if pk[K_DOWN]:
            self.rect.move_ip(0, 2)
        if pk[K_LEFT]:
            self.rect.move_ip(-2, 0)
        if pk[K_RIGHT]:
            self.rect.move_ip(2, 0)
            
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SW:
            self.rect.right = SW
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SH:
            self.rect.bottom = SH
            
class Plastic(pygame.sprite.Sprite):
    
    def __init__(self):
        super(Plastic, self).__init__()
        self.surf = pygame.Surface((67, 67))
        self.surf.fill((173, 216, 230))
        self.image = pygame.image.load("assets/plastic bottle.png").convert()
        self.image.set_colorkey((255, 255, 255), pygame.RLEACCEL)
        self.image = pygame.transform.scale(self.image, (67, 67))
        self.rect = self.surf.get_rect(
            center = (
                (random.randint(SW-30, SW),
                random.randint(1, SH))
                )
            )
        self.speed = random.randint(1, 2)
        
    def update(self):
        self.rect.move_ip(-self.speed,0)
        if self.rect.left < 0:
            self.kill()


pygame.init()

screen = pygame.display.set_mode((SW, SH))
font = pygame.font.Font(None, 36)
ADDPLASTIC = pygame.USEREVENT + 1
pygame.time.set_timer(ADDPLASTIC, 255)

background = pygame.image.load("assets/Background.png").convert()
background = pygame.transform.scale(background, (SW, SH))
player = Player()
p = Plastic()

plastics = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
players = pygame.sprite.Group()
players.add(player)
all_sprites.add(player)
all_sprites.add(p)
plastics.add(p)
score = 0

running = True
while running:
    for event in pygame.event.get():
        if event.type == KEYDOWN: 
            if event.key == K_ESCAPE:
                running = False
        elif event.type == ADDPLASTIC:
            new_plastic = Plastic()
            plastics.add(new_plastic)
            all_sprites.add(new_plastic)
                
    pk = pygame.key.get_pressed()
    player.update(pk)
    plastics.update()
    screen.fill((25, 25, 25))
    screen.blit(background, (0, 0))
    
    for e in all_sprites:
        try:
            entity = e.image
        except:
            entity = e.surf
        screen.blit(entity, e.rect)
     
    hits = pygame.sprite.spritecollide(player, plastics, True)
    
    for hit in hits:
        score+=1
    
    score_text = font.render("score: "+str(score),True,(255,255,255))       
    score_rect = score_text.get_rect()
    score_rect.topleft = (10, 10)
    
    screen.blit(score_text, score_rect)
        
    pygame.display.flip()
    
pygame.quit()