import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Game settings
player_pos = [SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2]  # Center the player initially
player_size = 50  # Size of the player, you might want to adjust this based on your sprite
player_speed = 5  # How fast the player moves
gravity = 0.5  # Gravity effect for jumping
jump_speed = -10  # Initial speed when jumping
velocity = 0  # Initial velocity for jumping
is_jumping = False

# Load player sprite (Replace 'path_to_your_sprite' with the actual path to your fox sprite image)
# For example, player_sprite = pygame.image.load('fox_sprite.png').convert_alpha()
# player_sprite = pygame.Surface((player_size, player_size))  # Placeholder square, replace with sprite
player_sprite = pygame.Surface((player_size, player_size))  # Placeholder square, replace with sprite
player_sprite('fox.webp')  # Fill the placeholder with black, replace with sprite

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Key press handling
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_pos[0] -= player_speed
    if keys[pygame.K_RIGHT]:
        player_pos[0] += player_speed
    if keys[pygame.K_SPACE] and not is_jumping:
        is_jumping = True
        velocity = jump_speed

    # Gravity and jumping logic
    if is_jumping:
        player_pos[1] += velocity
        velocity += gravity
        if player_pos[1] >= SCREEN_HEIGHT // 2:  # Reset to the original level, adjust as necessary
            player_pos[1] = SCREEN_HEIGHT // 2
            is_jumping = False

    # Clear the screen
    screen.fill(WHITE)

    # Draw the player
    screen.blit(player_sprite, player_pos)  # Use blit to draw the sprite instead of a rectangle

    # Update the display
    pygame.display.flip()

    # Cap the framerate to 60fps
    pygame.time.Clock().tick(60)
