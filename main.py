import pygame
import sys
from game import Game

def main():
    pygame.init()
    
    # Constants
    WINDOW_SIZE = (800, 600)
    BLOCK_SIZE = 20
    FPS = 10
    
    # Setup
    screen = pygame.display.set_mode(WINDOW_SIZE)
    pygame.display.set_caption("Snake Game")
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 36)
    
    game = Game(WINDOW_SIZE, BLOCK_SIZE)
    running = True
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if game.game_over:
                    if event.key == pygame.K_r:
                        game.reset()
                    elif event.key == pygame.K_q:
                        running = False
                else:
                    handle_input(event.key, game)
        
        game.update()
        draw(screen, game, font)
        pygame.display.flip()
        clock.tick(FPS)
    
    pygame.quit()
    sys.exit()

def handle_input(key: int, game: Game) -> None:
    if key == pygame.K_UP and game.snake.direction != "DOWN":
        game.snake.direction = "UP"
    elif key == pygame.K_DOWN and game.snake.direction != "UP":
        game.snake.direction = "DOWN"
    elif key == pygame.K_LEFT and game.snake.direction != "RIGHT":
        game.snake.direction = "LEFT"
    elif key == pygame.K_RIGHT and game.snake.direction != "LEFT":
        game.snake.direction = "RIGHT"

def draw(screen: pygame.Surface, game: Game, font: pygame.font.Font) -> None:
    screen.fill(game.colors['BLACK'])
    
    # Draw score
    score_text = font.render(f"Score: {game.score}", True, game.colors['WHITE'])
    screen.blit(score_text, (10, 10))
    
    # Draw game elements
    game.snake.draw(screen, game.colors)
    game.food.draw(screen, game.colors['RED'])
    
    # Draw game over screen if game is over
    if game.game_over:
        game.draw_game_over(screen, font)

if __name__ == "__main__":
    main()