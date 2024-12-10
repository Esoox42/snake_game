import pygame
import sys
import random

# Initialize the game
pygame.init()

# Constants
WINDOW_SIZE = (800, 600)
BLOCK_SIZE = 20  # Size of each block of the snake
FPS = 10  # Frames per second (controls game speed)

# Colors
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
GAME_OVER_BG = (0, 0, 0, 180)

# Game variables
score = 0
font = pygame.font.Font(None, 36)
running = True
game_over = False

def reset_game():
    global snake, snake_direction, food, score
    snake = [(400, 300), (380, 300), (360, 300)]
    snake_direction = "RIGHT"
    food = generate_food()
    score = 0

def generate_food():
    # Generate random positions that align with the grid
    x = random.randrange(0, WINDOW_SIZE[0], BLOCK_SIZE)
    y = random.randrange(0, WINDOW_SIZE[1], BLOCK_SIZE)
    return (x, y)

def check_collision():
    head_x, head_y = snake[0]
    # Check well collision
    if (head_x < 0 or head_x >= WINDOW_SIZE[0] 
        or head_y < 0 or head_y >= WINDOW_SIZE[1]):
        return True
    # Check self collision
    for segment in snake[1:]:
        if segment == (head_x, head_y):
            return True
    return False

screen = pygame.display.set_mode(WINDOW_SIZE) # Set window size
pygame.display.set_caption("Snake Game") # Set window title
clock = pygame.time.Clock() # Set clock

# Snake initialization
snake = [(400, 300), (380, 300), (360, 300)]  # Starting position (list of (x, y) tuples)
snake_direction = "RIGHT"  # Initial direction

# Food initialization
food = generate_food()  # Food position

# Game loop
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if game_over:
                if event.key == pygame.K_r:
                    game_over = False
                    reset_game()
                elif event.key == pygame.K_q:
                    running = False
            
            else:
                # Change direction based on key press
                if event.key == pygame.K_UP and snake_direction != "DOWN":
                    snake_direction = "UP"
                elif event.key == pygame.K_DOWN and snake_direction != "UP":
                    snake_direction = "DOWN"
                elif event.key == pygame.K_LEFT and snake_direction != "RIGHT":
                    snake_direction = "LEFT"
                elif event.key == pygame.K_RIGHT and snake_direction != "LEFT":
                    snake_direction = "RIGHT"


    if not game_over:
    # Move the snake
        head_x, head_y = snake[0]  # Current head position
        if snake_direction == "UP":
            head_y -= BLOCK_SIZE
        elif snake_direction == "DOWN":
            head_y += BLOCK_SIZE
        elif snake_direction == "LEFT":
            head_x -= BLOCK_SIZE
        elif snake_direction == "RIGHT":
            head_x += BLOCK_SIZE

        # Add the new head position
        new_head = (head_x, head_y)
        snake.insert(0, new_head)

        if check_collision():
            game_over = True
        elif snake[0] == food:
            food = generate_food()
            score += 1
        else:
            snake.pop()

    # Drawing
    screen.fill(BLACK)  # Clear the screen

    score_text = font.render(f"Score: {score}", True, WHITE) # Draw score
    screen.blit(score_text, (10, 10))

    for segment in snake:
        pygame.draw.rect(screen, GREEN, (*segment, BLOCK_SIZE, BLOCK_SIZE))  # Draw each block of the snake
    pygame.draw.rect(screen, RED, (*food, BLOCK_SIZE, BLOCK_SIZE))  # Draw the food

    if game_over:
        # Create semi-transparent overlay
        overlay = pygame.Surface(WINDOW_SIZE, pygame.SRCALPHA)
        overlay.fill(GAME_OVER_BG)
        screen.blit(overlay, (0, 0))
        
        # Game Over text
        game_over_text = font.render("GAME OVER!", True, WHITE)
        final_score_text = font.render(f"Final Score: {score}", True, WHITE)
        restart_text = font.render("Press R to Restart or Q to Quit", True, WHITE)
        
        # Position text in center
        screen_center_x = WINDOW_SIZE[0] // 2
        screen_center_y = WINDOW_SIZE[1] // 2
        
        screen.blit(game_over_text, 
                (screen_center_x - game_over_text.get_width() // 2, 
                    screen_center_y - 60))
        screen.blit(final_score_text, 
                (screen_center_x - final_score_text.get_width() // 2, 
                    screen_center_y))
        screen.blit(restart_text, 
                (screen_center_x - restart_text.get_width() // 2, 
                    screen_center_y + 60))

    # Update the display
    pygame.display.flip()
    # Control the game speed
    clock.tick(FPS)

# Quit the game
pygame.quit()
sys.exit()