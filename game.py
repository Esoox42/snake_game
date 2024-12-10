import pygame
from typing import Dict, Tuple
from snake import Snake
from food import Food

class Game:
    def __init__(self, window_size: Tuple[int, int], block_size: int):
        self.window_size = window_size
        self.block_size = block_size
        self.colors = {
            'BLACK': (0, 0, 0),
            'GREEN': (0, 255, 0),
            'DARK_GREEN': (0, 200, 0),
            'RED': (255, 0, 0),
            'DARK_RED': (200, 0, 0),
            'WHITE': (255, 255, 255),
            'GAME_OVER_BG': (0, 0, 0, 180)
        }
        self.reset()
        
    def reset(self) -> None:
        start_pos = [(400, 300), (380, 300), (360, 300)]
        self.snake = Snake(start_pos, self.block_size)
        self.food = Food(self.window_size, self.block_size)
        self.score = 0
        self.game_over = False
    
    def update(self) -> None:
        if self.game_over:
            return
            
        self.snake.move()
        
        if self.check_collision():
            self.game_over = True
        elif self.snake.body[0] == self.food.position:
            self.food.new_fruit()
            self.score += 1
        else:
            self.snake.shrink()
    
    def check_collision(self) -> bool:
        head_x, head_y = self.snake.body[0]
        # Wall collision
        if (head_x < 0 or head_x >= self.window_size[0] or 
            head_y < 0 or head_y >= self.window_size[1]):
            return True
        # Self collision
        if self.snake.body[0] in self.snake.body[1:]:
            return True
        return False
    
    def draw_game_over(self, screen: pygame.Surface, font: pygame.font.Font) -> None:
        # Create semi-transparent overlay
        overlay = pygame.Surface(self.window_size, pygame.SRCALPHA)
        overlay.fill(self.colors['GAME_OVER_BG'])
        screen.blit(overlay, (0, 0))
        
        # Game Over text
        game_over_text = font.render("GAME OVER!", True, self.colors['WHITE'])
        final_score_text = font.render(f"Final Score: {self.score}", True, self.colors['WHITE'])
        restart_text = font.render("Press R to Restart or Q to Quit", True, self.colors['WHITE'])
        
        # Position text in center
        screen_center_x = self.window_size[0] // 2
        screen_center_y = self.window_size[1] // 2
        
        screen.blit(game_over_text, 
                   (screen_center_x - game_over_text.get_width() // 2, 
                    screen_center_y - 60))
        screen.blit(final_score_text, 
                   (screen_center_x - final_score_text.get_width() // 2, 
                    screen_center_y))
        screen.blit(restart_text, 
                   (screen_center_x - restart_text.get_width() // 2, 
                    screen_center_y + 60))