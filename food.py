import pygame
import random
from typing import Tuple

class Food:
    def __init__(self, window_size: Tuple[int, int], block_size: int):
        self.window_size = window_size
        self.block_size = block_size
        self.position = self.generate_position()
        
    def generate_position(self) -> Tuple[int, int]:
        x = random.randrange(0, self.window_size[0], self.block_size)
        y = random.randrange(0, self.window_size[1], self.block_size)
        return (x, y)
    
    def draw(self, screen: pygame.Surface, color: Tuple[int, int, int]) -> None:
        pygame.draw.rect(screen, color, (*self.position, self.block_size, self.block_size))