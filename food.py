import pygame
import random
from typing import Tuple

class Food:
    def __init__(self, window_size: Tuple[int, int], block_size: int):
        self.window_size = window_size
        self.block_size = block_size
        self.position = self.generate_position()
        self.colors = {
            'RED': (255, 0, 0),
            'DARK_GREEN': (0, 200, 0),
            'BROWN': (139, 69, 19)
        }
        
    def generate_position(self) -> Tuple[int, int]:
        x = random.randrange(0, self.window_size[0], self.block_size)
        y = random.randrange(0, self.window_size[1], self.block_size)
        return (x, y)
    
    def draw(self, screen: pygame.Surface, _: Tuple[int, int]) -> None:  # Ignore the color parameter
        x, y = self.position
        center_x = x + self.block_size // 2
        center_y = y + self.block_size // 2
        
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