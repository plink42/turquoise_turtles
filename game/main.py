'''The main file of the game, where the game loop is defined and the game is run.'''
import sys, pygame
import random

# import the keys from the pygame module
from pygame.locals import (
    QUIT,
    K_ESCAPE,
    KEYDOWN,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_w,
    K_a,
    K_s,
    K_d)

# defind the screen width and height    
SW = 1800
SH = 940

# define the player class
# the player class is a subclass of the pygame.sprite.Sprite class
# the player class has the following methods:
# __init__ - initializes the player object
# update - updates the player object
# the player class has the following attributes:
# surf - the surface of the player object
# image - the image of the player object
# rect - the rectangle of the player object
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.Surface((400, 250))
        self.surf.fill((210, 180, 140))
        self.image = pygame.image.load("assets/new_player_2.0.png").convert()
        self.image.set_colorkey((255, 255, 255), pygame.RLEACCEL)
        self.image = pygame.transform.scale(self.image, (400, 250))
        self.rect = self.surf.get_rect(
                center = ((SW/2, SH/2))
            )
        
    def update(self, pk):
        if pk[K_UP] or pk[K_w]:
            self.rect.move_ip(0, -5)
        if pk[K_DOWN] or pk[K_s]:
            self.rect.move_ip(0, 5)
        if pk[K_LEFT] or pk[K_a]:
            self.rect.move_ip(-5, 0)
        if pk[K_RIGHT] or pk[K_d]:
            self.rect.move_ip(5, 0)
            
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SW:
            self.rect.right = SW
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SH:
            self.rect.bottom = SH

# define the plastic class
# the plastic class is a subclass of the pygame.sprite.Sprite class
# the plastic class has the following methods:
# __init__ - initializes the plastic object
# update - updates the plastic object
# the plastic class has the following attributes:
# surf - the surface of the plastic object
# image - the image of the plastic object
# rect - the rectangle of the plastic object
# speed - the speed of the plastic object          
class Plastic(pygame.sprite.Sprite):
    
    def __init__(self):
        super(Plastic, self).__init__()
        self.surf = pygame.Surface((67, 67))
        self.surf.fill((173, 216, 230))
        self.image = pygame.image.load("assets/plastic_bottel_new_vr2.0.png").convert()
        self.image.set_colorkey((255, 255, 255), pygame.RLEACCEL)
        self.image = pygame.transform.scale(self.image, (67, 67))
        self.rect = self.surf.get_rect(
            center = (
                (random.randint(SW-30, SW),
                random.randint(1, SH))
                )
            )
        self.speed = random.randint(2, 7)
        
    def update(self):
        self.rect.move_ip(-self.speed,0)
        if self.rect.left < 0:
            self.kill()

# initialize the pygame module
pygame.init()

# set the screen width and height
screen = pygame.display.set_mode((SW, SH))

# set the font
font = pygame.font.Font(None, 36)

# set the event ADDPLASTIC
ADDPLASTIC = pygame.USEREVENT + 1

# set the timer for the ADDPLASTIC event
pygame.time.set_timer(ADDPLASTIC, 255)

# load the background image
background = pygame.image.load("assets/Background.png").convert()
background = pygame.transform.scale(background, (SW, SH))

# create the player object and the plastic object
player = Player()
p = Plastic()

# create the sprite groups
plastics = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
players = pygame.sprite.Group()

# add the player object and the plastic object to the sprite groups
players.add(player)
all_sprites.add(player)
all_sprites.add(p)
plastics.add(p)
score = 0

# Control the FPS
clock = pygame.time.Clock()

# run the game loop
running = True
while running:
    clock.tick(60)
    # watch for events
    for event in pygame.event.get():
        if event.type == KEYDOWN: 
            if event.key == K_ESCAPE:
                running = False
        elif event.type == ADDPLASTIC:
            new_plastic = Plastic()
            plastics.add(new_plastic)
            all_sprites.add(new_plastic)

    # get key presses            
    pk = pygame.key.get_pressed()
    player.update(pk)
    plastics.update()
    screen.fill((25, 25, 25))
    screen.blit(background, (0, 0))
    
    # draw the sprites
    for e in all_sprites:
        try:
            entity = e.image
        except:
            entity = e.surf
        screen.blit(entity, e.rect)
    
    # watch for collisions
    hits = pygame.sprite.spritecollide(player, plastics, True)
    
    # update the score
    for hit in hits:
        score+=1
    
    # draw the score
    score_text = font.render("score: "+str(score),True,(255,255,255))       
    score_rect = score_text.get_rect()
    score_rect.topleft = (10, 10)
    
    screen.blit(score_text, score_rect)
        
    pygame.display.flip()
    
pygame.quit()