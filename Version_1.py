# Import the pygame module
import pygame
import random
from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)
# Define constants for the screen width and height
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

clock = pygame.time.Clock()

class Cloud(pygame.sprite.Sprite):
    def __init__(self):
        super(Cloud,self).__init__()
        self.surf = pygame.image.load("cloud.png").convert()
        self.surf.set_colorkey((0,0,0),RLEACCEL)
        #Starting position randomly generated at right of screen border
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH+20,SCREEN_WIDTH+100),
                random.randint(0,SCREEN_HEIGHT),
            )
        )
    def update(self):
        self.rect.move_ip(-2,0)
        #kill the cloud when it leaves screen to the left
        if self.rect.right < 0:
            self.kill()

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.surf = pygame.image.load("missile.png").convert()
        self.surf.set_colorkey((255,255,255),RLEACCEL)
        self.surf 
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH +20, SCREEN_WIDTH +100),
                random.randint(0, SCREEN_HEIGHT),
            )
        )
        #self.speed = random.randint(1,2)
        self.speed = random.randint(5,15)
    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
              self.kill()

# Define a player object by extending pygame.sprite.Sprit
# The surface drawn on the screen is now an attribute of 'player'
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.image.load("jet.png").convert()
        self.surf.set_colorkey((255,255,255),RLEACCEL)
        self.rect = self.surf.get_rect()
    def update(self,pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0,-5)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0,5)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-5,0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(5,0)
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
# Initialize pygame
pygame.init()
# Create the screen object
# The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
#Create custom event for adding new enemy
ADDENEMY = pygame.USEREVENT +1
pygame.time.set_timer(ADDENEMY, 500)
#Create custom event for adding new cloud
ADDCLOUD = pygame.USEREVENT +2
pygame.time.set_timer(ADDCLOUD,1000)
player = Player()
# Variable to keep the main loop running
enemies = pygame.sprite.Group()
clouds = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)
running = True

# Main loop
while running:
    # for loop through the event queue
    for event in pygame.event.get():
        # Check for KEYDOWN event
        if event.type == KEYDOWN:
            # If the Esc key is pressed, then exit the main loop
            if event.key == K_ESCAPE:
                running = False
        # Check for QUIT event. If QUIT, then set running to false.
        elif event.type == QUIT:
            running = False
        elif event.type == ADDENEMY:
            new_enemy = Enemy()
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)
        elif event.type == ADDCLOUD:
            new_cloud = Cloud()
            clouds.add(new_cloud)
            all_sprites.add(new_cloud)
        
    pressed_keys = pygame.key.get_pressed()
    player.update(pressed_keys)

    enemies.update()
    clouds.update()

    # Fill the screen with black
    screen.fill((135,206,250))

    # Draw the player on the screen
    #blit updates part of surface while flip updates whole surface.
    for entity in all_sprites:
        screen.blit(entity.surf,entity.rect)

    #Check if any enemies have collided with the player
    if pygame.sprite.spritecollideany(player,enemies):
        player.kill()
        running = False

    # Update the display
    pygame.display.flip()
    clock.tick(60)                