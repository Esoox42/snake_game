import pygame
from typing import Dict, Tuple
from snake import Snake
from food import Food
from highscores import HighScoreManager

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
        self.high_scores = HighScoreManager()
        self.player_name = ""
        self.in_menu = True
        self.show_new_high_score = False
        self.reset()

    def handle_menu_input(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN and len(self.player_name) > 0:
                self.in_menu = False
            elif event.key == pygame.K_BACKSPACE:
                self.player_name = self.player_name[:-1]
            elif len(self.player_name) < 10 and event.unicode.isalnum():
                self.player_name += event.unicode.upper()
    
    def draw_menu(self, screen: pygame.Surface, font: pygame.font.Font) -> None:
        screen.fill(self.colors['BLACK'])
        
        # Draw title
        title = font.render("SNAKE GAME", True, self.colors['GREEN'])
        name_prompt = font.render("Enter Your Name:", True, self.colors['WHITE'])
        name_text = font.render(self.player_name + "_", True, self.colors['WHITE'])
        
        screen_center_x = self.window_size[0] // 2
        screen_center_y = self.window_size[1] // 2
        
        screen.blit(title, (screen_center_x - title.get_width() // 2, 
                           screen_center_y - 100))
        screen.blit(name_prompt, (screen_center_x - name_prompt.get_width() // 2, 
                                screen_center_y - 20))
        screen.blit(name_text, (screen_center_x - name_text.get_width() // 2, 
                               screen_center_y + 20))
        # Draw high scores
        self.draw_high_scores(screen, font, screen_center_y + 80)

    def draw_high_scores(self, screen: pygame.Surface, font: pygame.font.Font, start_y: int) -> None:
        title = font.render("HIGH SCORES", True, self.colors['GREEN'])
        screen_center_x = self.window_size[0] // 2
        screen.blit(title, (screen_center_x - title.get_width() // 2, start_y))
        
        for i, score in enumerate(self.high_scores.get_high_scores()):
            score_text = font.render(f"{i+1}. {score['name']}: {score['score']}", 
                                   True, self.colors['WHITE'])
            screen.blit(score_text, 
                       (screen_center_x - score_text.get_width() // 2, 
                        start_y + 30 + i * 25))
    
    def check_high_score(self) -> None:
        if self.high_scores.add_score(self.player_name, self.score):
            self.show_new_high_score = True

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
            self.check_high_score()
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
        
        # Add high score text if achieved
        texts = [(game_over_text, -60),
                (final_score_text, 0)]
        
        if self.show_new_high_score:
            high_score_text = font.render("NEW HIGH SCORE!", True, self.colors['GREEN'])
            texts.insert(1, (high_score_text, -30))
        
        texts.append((restart_text, 60))
        
        # Position text in center
        screen_center_x = self.window_size[0] // 2
        screen_center_y = self.window_size[1] // 2
        
        for text, y_offset in texts:
            screen.blit(text, 
                       (screen_center_x - text.get_width() // 2, 
                        screen_center_y + y_offset))