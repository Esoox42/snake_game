import pygame
import random
import math
from typing import Tuple

class Food:
    def __init__(self, window_size: Tuple[int, int], block_size: int):
        self.window_size = window_size
        self.block_size = block_size
        self.position = self.generate_position()
        self.colors = {
            'RED': (255, 0, 0),
            'BROWN': (139, 69, 19),
            'ORANGE': (255, 140, 0),
            'DARK_ORANGE': (200, 100, 0),
            'GREEN': (0, 255, 0),
            'DARK_GREEN': (0, 200, 0),
            'PEAR_GREEN': (209, 226, 49)
        }
        self.fruit_type = random.choice(['apple', 'orange', 'pear'])
        
    def generate_position(self) -> Tuple[int, int]:
        x = random.randrange(0, self.window_size[0], self.block_size)
        y = random.randrange(0, self.window_size[1], self.block_size)
        return (x, y)
    
    def draw(self, screen: pygame.Surface, _: Tuple[int, int]) -> None:  # Ignore the color parameter
        x, y = self.position
        center_x = x + self.block_size // 2
        center_y = y + self.block_size // 2
        
        if self.fruit_type == 'apple':
            self._draw_apple(screen, x, y, center_x, center_y)
        elif self.fruit_type == 'orange':
            self._draw_orange(screen, x, y, center_x, center_y)
        else:  # pear
            self._draw_pear(screen, x, y, center_x, center_y)

    def _draw_apple(self, screen, x, y, center_x, center_y):
        # Draw main apple body (red circle)
        apple_radius = self.block_size // 2 - 2
        pygame.draw.circle(screen, self.colors['RED'], (center_x, center_y), apple_radius)
        
        # Draw stem (brown rectangle)
        stem_width = self.block_size // 6
        stem_height = self.block_size // 3
        stem_x = center_x - stem_width // 2
        stem_y = y - stem_height // 2
        pygame.draw.rect(screen, self.colors['BROWN'],
                        (stem_x, stem_y, stem_width, stem_height))
        
        # Draw leaf (green triangle)
        leaf_points = [
            (center_x + 2, y),  # Leaf base
            (center_x + self.block_size // 3, y - self.block_size // 3),  # Leaf tip
            (center_x + self.block_size // 2, y)  # Leaf end
        ]
        pygame.draw.polygon(screen, self.colors['DARK_GREEN'], leaf_points)

    def _draw_orange(self, screen, x, y, center_x, center_y):
        # Draw main orange body
        orange_radius = self.block_size // 2 - 2
        pygame.draw.circle(screen, self.colors['ORANGE'], (center_x, center_y), orange_radius)
        
        # Draw small leaf
        leaf_points = [
            (center_x - 2, y + 2),
            (center_x + 2, y - self.block_size // 4),
            (center_x + 6, y + 2)
        ]
        pygame.draw.polygon(screen, self.colors['DARK_GREEN'], leaf_points)
        
        # Draw texture lines to make it look more like an orange
        for angle in range(0, 360, 45):  # 8 lines for texture
            rad = angle * math.pi / 180  # Convert to radians
            start_x = center_x + (orange_radius * 0.5 * math.cos(rad))
            start_y = center_y + (orange_radius * 0.5 * math.sin(rad))
            end_x = center_x + (orange_radius * 0.9 * math.cos(rad))
            end_y = center_y + (orange_radius * 0.9 * math.sin(rad))
            pygame.draw.line(screen, self.colors['DARK_ORANGE'], 
                           (start_x, start_y), (end_x, end_y), 1)
        
    def _draw_pear(self, screen, x, y, center_x, center_y):
        # Draw pear body (two circles)
        top_radius = self.block_size // 3
        bottom_radius = self.block_size // 2 - 2
        
        # Bottom circle (larger)
        pygame.draw.circle(screen, self.colors['PEAR_GREEN'],
                         (center_x, y + self.block_size - bottom_radius),
                         bottom_radius)
        
        # Top circle (smaller)
        pygame.draw.circle(screen, self.colors['PEAR_GREEN'],
                         (center_x, y + top_radius),
                         top_radius)
        
        # Draw stem
        stem_width = self.block_size // 6
        stem_height = self.block_size // 4
        stem_x = center_x - stem_width // 2
        stem_y = y - stem_height // 2
        pygame.draw.rect(screen, self.colors['BROWN'],
                        (stem_x, stem_y, stem_width, stem_height))
        
       # Draw leaf
        leaf_points = [
            (center_x + 2, y),
            (center_x + self.block_size // 3, y - self.block_size // 3),
            (center_x + self.block_size // 2, y)
        ]
        pygame.draw.polygon(screen, self.colors['DARK_GREEN'], leaf_points)

    def new_fruit(self):
        """Generate a new fruit with random type and position"""
        self.position = self.generate_position()
        self.fruit_type = random.choice(['apple', 'orange', 'pear'])