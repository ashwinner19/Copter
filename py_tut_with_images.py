# Import the pygame module
import pygame
import time

# Import random for random numbers
import random

# Import pygame.locals for easier access to key coordinates
# Updated to conform to flake8 and black standards
# from pygame.locals import *
from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_SPACE,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

# Define constants for the screen width and height
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

DISPLAY_GAME = True

# Define the Player object extending pygame.sprite.Sprite
# Instead of a surface, we use an image for a better looking sprite
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.image.load("jet.png").convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect()

    # Move the sprite based on keypresses
    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -5)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 5)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)

        # Keep player on the screen
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        elif self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT


# Define the enemy object extending pygame.sprite.Sprite
# Instead of a surface, we use an image for a better looking sprite
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.surf = pygame.Surface((50, 30))
        self.surf.fill((255, 255, 255))
        # The starting position is randomly generated, as is the speed
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 100, SCREEN_WIDTH + 240),
                random.randint(0, SCREEN_HEIGHT),
            )
        )
        self.speed = 10

    # Move the enemy based on speed
    # Remove it when it passes the left edge of the screen
    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()

# Our main loop
def main():
    # Initialize pygame
    pygame.init()

    # Setup the clock for a decent framerate
    clock = pygame.time.Clock()

    # Create the screen object
    # The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    # Create custom events for adding a new enemy and cloud
    ADDENEMY = pygame.USEREVENT + 1
    pygame.time.set_timer(ADDENEMY, 1000)
    ADDCLOUD = pygame.USEREVENT + 2
    pygame.time.set_timer(ADDCLOUD, 1000)

    # Create our 'player'
    player = Player()

    # Create groups to hold enemy sprites, cloud sprites, and all sprites
    # - enemies is used for collision detection and position updates
    # - clouds is used for position updates
    # - all_sprites isused for rendering
    enemies = pygame.sprite.Group()
    clouds = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)
    myfont = pygame.font.SysFont("freesansbold", 32)
    textX = 10
    textY = 10
    font = pygame.font.SysFont("freesansbold", 50)
    textA = 200
    textB = 200
    running = True
    score = 0

    def show_score(x, y, score):
        scoretext = myfont.render("Score :" + str(score), True, (255, 255, 255))
        screen.blit(scoretext, (x, y))

    def show_win(x, y, score):
        text1 = ["You Win!!!",
                 "Press space to play again",
                 "Esc to Quit"]
        x1 = x
        y1 = y
        for i in text1:
            text = font.render(i, True, (255, 255, 255))
            screen.blit(text, (x1, y1))
            y1 += 60

    while running:
        # Look at every event in the queue
        if score < 500:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    # Was it the Escape key? If so, stop the loop
                    if event.key == K_ESCAPE:
                        running = False
                    if event.key == K_RIGHT:
                        score += 1

                # Did the user click the window close button? If so, stop the loop
                elif event.type == QUIT:
                    running = False

                # Should we add a new enemy?
                elif event.type == ADDENEMY:
                    # Create the new enemy, and add it to our sprite groups
                    new_enemy = Enemy()
                    enemies.add(new_enemy)
                    all_sprites.add(new_enemy)

            # Get the set of keys pressed and check for user input
            pressed_keys = pygame.key.get_pressed()
            player.update(pressed_keys)

            # Update the position of our enemies and clouds
            enemies.update()

            # Fill the screen with sky blue
            screen.fill((135, 206, 250))

            # Draw all our sprites
            for entity in all_sprites:
                screen.blit(entity.surf, entity.rect)

            # Check if any enemies have collided with the player
            if pygame.sprite.spritecollideany(player, enemies):
                # If so, remove the player
                player.kill()

                # Stop the loop
                running = False

            #score display
            show_score(textX, textY,score)
            score += 1

        else:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    # Was it the Escape key? If so, stop the loop
                    if event.key == K_ESCAPE:
                        running = False
                    elif event.key == K_SPACE:
                        main()

                # Did the user click the window close button? If so, stop the loop
                elif event.type == QUIT:
                    running = False

            screen.fill((135, 206, 250))
            show_win(textA, textB, score)

            show_score(textX, textY, score)

        # Flip everything to the display
        if DISPLAY_GAME == True:
            pygame.display.flip()

        # Ensure we maintain a 30 frames per second rate
        clock.tick(30)


main()