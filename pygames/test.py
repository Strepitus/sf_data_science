import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
WIDTH = 800
HEIGHT = 600
PADDLE_WIDTH = 200
PADDLE_HEIGHT = 10
PADDLE_SPEED = 10
BALL_RADIUS = 15
BALL_SPEED = 6
BRICK_WIDTH = 80
BRICK_HEIGHT = 30
BRICK_ROWS = 5
BRICK_COLS = 10
BRICK_GAP = 4
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Breakout")

# Clock for controlling the frame rate
clock = pygame.time.Clock()

# Paddle
paddle = pygame.Rect(WIDTH // 2 - PADDLE_WIDTH // 2, HEIGHT - PADDLE_HEIGHT - 10, PADDLE_WIDTH, PADDLE_HEIGHT)

# Ball
ball = pygame.Rect(WIDTH // 2 - BALL_RADIUS, HEIGHT // 2 - BALL_RADIUS, BALL_RADIUS * 2, BALL_RADIUS * 2)
ball_speed_x = BALL_SPEED
ball_speed_y = -BALL_SPEED

# Bricks
bricks = []
for row in range(BRICK_ROWS):
    for col in range(BRICK_COLS):
        brick = pygame.Rect(col * (BRICK_WIDTH + BRICK_GAP) + BRICK_GAP // 2,
                            row * (BRICK_HEIGHT + BRICK_GAP) + BRICK_GAP // 2,
                            BRICK_WIDTH, BRICK_HEIGHT)
        bricks.append(brick)

# Game loop
running = True
while running:
    screen.fill(BLACK)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and paddle.left > 0:
        paddle.x -= PADDLE_SPEED
    if keys[pygame.K_RIGHT] and paddle.right < WIDTH:
        paddle.x += PADDLE_SPEED
    
    # Move the ball
    ball.x += ball_speed_x
    ball.y += ball_speed_y
    
    # Ball collision with walls
    if ball.left < 0 or ball.right > WIDTH:
        ball_speed_x *= -1
    if ball.top < 0:
        ball_speed_y *= -1
    
    # Ball collision with paddle
    if ball.colliderect(paddle) and ball_speed_y > 0:
        ball_speed_y *= -1
    
    # Ball collision with bricks
    for brick in bricks:
        if ball.colliderect(brick):
            bricks.remove(brick)
            ball_speed_y *= -1
    
    # Draw the paddle
    pygame.draw.rect(screen, WHITE, paddle)
    
    # Draw the ball
    pygame.draw.circle(screen, RED, ball.center, BALL_RADIUS)
    
    # Draw the bricks
    for brick in bricks:
        pygame.draw.rect(screen, BLUE, brick)
    
    # Check for game over
    if ball.bottom > HEIGHT:
        running = False
    
    pygame.display.flip()
    clock.tick(60)

# Quit Pygame
pygame.quit()
sys.exit()
