import pygame
import math
import random

SCREEN_TITLE = 'Crossy'
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

HIGH_SCORE = 0

PURPLE_COLOR = (128,0,128)
BLACK_COLOR = (0, 0, 0)

clock = pygame.time.Clock()
pygame.font.init()
font = pygame.font.SysFont('comicsans', 75)
level_font = pygame.font.SysFont('comicsans', 25)
birthday_font = pygame.font.SysFont('comicsans', 60)

class Game:

    # Typical rate of 60, equivalent to FPS
    TICK_RATE = 60

    # Initializer for the game class to set up the width, height, and title
    def __init__(self, image_path, title, width, height):
        self.title = title
        self.width = width
        self.height = height

        # Create the window of specified size in white to display the game
        self.game_screen = pygame.display.set_mode((width, height))
        # Set the game window color to white
        self.game_screen.fill(PURPLE_COLOR)
        pygame.display.set_caption(title)

        # Load and set the background image for the scene
        background_image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(background_image, (width, height))

    def run_game_loop(self, level_speed, level):
        global HIGH_SCORE
        did_win = False
        direction = 0
        exit_game = False
        show_happy_birthday = False

        player_character = PlayerCharacter('player.png', 375, 700, 50, 50)
        enemy_0 = NonPlayerCharacter('enemy.png', random.randint(20, self.width - 40), 400, 50, 50)
        # Speed increased as we advance in difficulty
        enemy_0.SPEED *= level_speed

        # Create another enemy
        enemy_1 = NonPlayerCharacter('enemy.png', random.randint(20, self.width - 40), 250, 50, 50)
        enemy_1.SPEED *= level_speed

        # Create another enemy
        enemy_2 = NonPlayerCharacter('enemy.png', random.randint(20, self.width - 40), 100, 50, 50)
        enemy_2.SPEED *= level_speed

        treasure = GameObject('treasure.png', 375, 50, 50, 50)

        # image_path, x, y, width, height
        heart = GameObject('heart.png', 375, 355, 50, 50)

        # Main game loop, used to update all gameplay such as movement, checks, and graphics
        while not exit_game:

            # A loop to get all of the events occuring at any given time
            # Events are most often mouse movement, mouse and button clicks, or exit events
            for event in pygame.event.get():
                keys = pygame.key.get_pressed()
                # If we have a quite type event (exit out) then exit out of the game loop
                if event.type == pygame.QUIT:
                    exit_game = True
                # Detect when key is pressed down
                elif event.type == pygame.KEYDOWN:
                    # Move up if up key pressed
                    if event.key == pygame.K_UP:
                        direction = 1
                    # Move down if down key pressed
                    elif event.key == pygame.K_DOWN:
                        direction = -1
                    elif event.key == pygame.K_7:
                       show_happy_birthday = not show_happy_birthday
                       keys[pygame.K_RIGHT] and keys[pygame.K_LEFT]
                # Detect when key is released
                elif event.type == pygame.KEYUP:
                    # Stop movement when key no longer pressed
                    if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                        direction = 0

            # Redraw the screen to be a blank white window

            self.game_screen.fill(PURPLE_COLOR)
            # Draw the image onto the background
            self.game_screen.blit(self.image, (0, 0))

            text = level_font.render(f'Level {math.ceil(level)}', True, BLACK_COLOR)
            self.game_screen.blit(text, (375, 525))

            high_score_text = level_font.render(f'High Score {math.ceil(HIGH_SCORE)}', True, BLACK_COLOR)
            self.game_screen.blit(high_score_text, (350, 500))

            # Draw the treasure
            treasure.draw(self.game_screen)
            
            # Update the player position
            player_character.move(direction, self.height)
            # Draw the player at the new position
            player_character.draw(self.game_screen)

            # Move and draw the enemy character
            enemy_0.move(self.width)
            enemy_0.draw(self.game_screen)

            # Move and draw more enemies when we reach higher levels of difficulty
            if level_speed > 2:
                enemy_1.move(self.width)
                enemy_1.draw(self.game_screen)
                if player_character.detect_collision(enemy_1):
                    did_win = self.enemy_collision()
                    break
            if level_speed > 4:
                if player_character.detect_collision(enemy_2):
                    did_win = self.enemy_collision()
                    break
                enemy_2.move(self.width)
                enemy_2.draw(self.game_screen)

            if player_character.detect_collision(enemy_0):
                did_win = self.enemy_collision()
                break
            elif player_character.detect_collision(treasure):
                did_win = True
                text = font.render('You win! :)', True, BLACK_COLOR)
                self.game_screen.blit(text, (275, 350))
                pygame.display.update()
                clock.tick(1)
                break
            if show_happy_birthday:
                text = birthday_font.render('Happy Birthday, Connelly!', True, PURPLE_COLOR)
                text3 = birthday_font.render('D + J', True, PURPLE_COLOR)
                heart.draw(self.game_screen)
                self.game_screen.blit(text, (150, 310))
                self.game_screen.blit(text3, (348, 410))
                pygame.display.update()

            # Update all game graphics
            pygame.display.update()
            # Tick the clock to update everything within the game
            clock.tick(self.TICK_RATE)

        if exit_game:
            return
        if did_win:
            self.run_game_loop(level_speed + 0.5, level + 1)
        else:
            if level > HIGH_SCORE:
                 HIGH_SCORE = level
            self.run_game_loop(1, 1)

    def enemy_collision(self):
         text = font.render('You lose! :(', True, BLACK_COLOR)
         self.game_screen.blit(text, (275, 350))
         pygame.display.update()
         clock.tick(1)
         return False

# Generic game object class to be subclassed by other objects in the game
class GameObject:

    def __init__(self, image_path, x, y, width, height):
        object_image = pygame.image.load(image_path)
        # Scale the image up
        self.image = pygame.transform.scale(object_image, (width, height))
        
        self.x_pos = x
        self.y_pos = y

        self.width = width
        self.height = height

    # Draw the object by blitting it onto the background (game screen)
    def draw(self, background):
        background.blit(self.image, (self.x_pos, self.y_pos))

# Class to represent the character contolled by the player
class PlayerCharacter(GameObject):

    # How many tiles the character moves per second
    SPEED = 5

    def __init__(self, image_path, x, y, width, height):
        super().__init__(image_path, x, y, width, height)

    # Move function will move character up if direction > 0 and down if < 0
    def move(self, direction, max_height):
        if direction > 0:
            self.y_pos -= self.SPEED
        elif direction < 0:
            self.y_pos += self.SPEED
        # Make sure the character never goes past the bottom of the screen
        if self.y_pos >= max_height - 40:
            self.y_pos = max_height - 40

    # Return False (no collision) if y positions and x positions do not overlap
    # Return True x and y positions overlap
    def detect_collision(self, other_body):
        if self.y_pos > other_body.y_pos + other_body.height:
            return False
        elif self.y_pos + self.height < other_body.y_pos:
            return False
        
        if self.x_pos > other_body.x_pos + other_body.width:
            return False
        elif self.x_pos + self.width < other_body.x_pos:
            return False
        return True

# Class to represent the enemies moving left to right and right to left
class NonPlayerCharacter(GameObject):

    # How many tiles the character moves per second
    SPEED = 3

    def __init__(self, image_path, x, y, width, height):
        super().__init__(image_path, x, y, width, height)

    # Move function will move character right once it hits the far left of the
    # screen and left once it hits the far right of the screen
    def move(self, max_width):
        if self.x_pos <= 20:
            self.SPEED = abs(self.SPEED)
        elif self.x_pos >= max_width - 40:
            self.SPEED = -abs(self.SPEED)
        self.x_pos += self.SPEED
            
pygame.init()

new_game = Game('background.png', SCREEN_TITLE, SCREEN_WIDTH, SCREEN_HEIGHT)
new_game.run_game_loop(1, 1)

# Quit pygame and the program
pygame.quit()
quit()
