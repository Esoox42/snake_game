import pygame
from typing import List, Tuple

class Snake:
    def __init__(self, start_pos: List[Tuple[int, int]], block_size: int):
        self.body = start_pos
        self.direction = "RIGHT"
        self.block_size = block_size
        
    def move(self) -> None:
        head_x, head_y = self.body[0]
        if self.direction == "UP":
            head_y -= self.block_size
        elif self.direction == "DOWN":
            head_y += self.block_size
        elif self.direction == "LEFT":
            head_x -= self.block_size
        elif self.direction == "RIGHT":
            head_x += self.block_size
        
        self.body.insert(0, (head_x, head_y))
    
    def grow(self) -> None:
        pass  # Don't remove the tail
        
    def shrink(self) -> None:
        self.body.pop()
        
    def draw(self, screen: pygame.Surface, colors: dict) -> None:
        for i, segment in enumerate(self.body):
            pygame.draw.rect(screen, colors['GREEN'] if i == 0 else colors['DARK_GREEN'], 
                           (*segment, self.block_size, self.block_size))
            
            if i == 0:  # Draw head details
                self._draw_head_details(screen, segment, colors)
    
    def _draw_head_details(self, screen: pygame.Surface, segment: Tuple[int, int], colors: dict) -> None:
        center_x = segment[0] + self.block_size//2
        center_y = segment[1] + self.block_size//2
        self._draw_eyes(screen, segment, colors)
        self._draw_tongue(screen, segment, center_x, center_y, colors)
    
    def _draw_eyes(self, screen, segment, colors):
        eye_radius = 3
        eye_positions = {
            "RIGHT": [(segment[0] + self.block_size - 5, segment[1] + 7),
                     (segment[0] + self.block_size - 5, segment[1] + self.block_size - 7)],
            "LEFT": [(segment[0] + 5, segment[1] + 7),
                    (segment[0] + 5, segment[1] + self.block_size - 7)],
            "UP": [(segment[0] + 7, segment[1] + 5),
                   (segment[0] + self.block_size - 7, segment[1] + 5)],
            "DOWN": [(segment[0] + 7, segment[1] + self.block_size - 5),
                    (segment[0] + self.block_size - 7, segment[1] + self.block_size - 5)]
        }
        
        for pos in eye_positions[self.direction]:
            pygame.draw.circle(screen, colors['BLACK'], pos, eye_radius)
            
    def _draw_tongue(self, screen, segment, center_x, center_y, colors):
        if self.direction == "RIGHT":
            pygame.draw.line(screen, colors['DARK_RED'], 
                           (segment[0] + self.block_size, center_y), 
                           (segment[0] + self.block_size + 10, center_y), 2)
            pygame.draw.line(screen, colors['DARK_RED'], 
                           (segment[0] + self.block_size + 10, center_y), 
                           (segment[0] + self.block_size + 15, center_y - 5), 2)
            pygame.draw.line(screen, colors['DARK_RED'], 
                           (segment[0] + self.block_size + 10, center_y), 
                           (segment[0] + self.block_size + 15, center_y + 5), 2)
        
        elif self.direction == "LEFT":
            pygame.draw.line(screen, colors['DARK_RED'], 
                           (segment[0], center_y), 
                           (segment[0] - 10, center_y), 2)
            pygame.draw.line(screen, colors['DARK_RED'], 
                           (segment[0] - 10, center_y), 
                           (segment[0] - 15, center_y - 5), 2)
            pygame.draw.line(screen, colors['DARK_RED'], 
                           (segment[0] - 10, center_y), 
                           (segment[0] - 15, center_y + 5), 2)
        
        elif self.direction == "UP":
            pygame.draw.line(screen, colors['DARK_RED'], 
                           (center_x, segment[1]), 
                           (center_x, segment[1] - 10), 2)
            pygame.draw.line(screen, colors['DARK_RED'], 
                           (center_x, segment[1] - 10), 
                           (center_x - 5, segment[1] - 15), 2)
            pygame.draw.line(screen, colors['DARK_RED'], 
                           (center_x, segment[1] - 10), 
                           (center_x + 5, segment[1] - 15), 2)
        
        elif self.direction == "DOWN":
            pygame.draw.line(screen, colors['DARK_RED'], 
                           (center_x, segment[1] + self.block_size), 
                           (center_x, segment[1] + self.block_size + 10), 2)
            pygame.draw.line(screen, colors['DARK_RED'], 
                           (center_x, segment[1] + self.block_size + 10), 
                           (center_x - 5, segment[1] + self.block_size + 15), 2)
            pygame.draw.line(screen, colors['DARK_RED'], 
                           (center_x, segment[1] + self.block_size + 10), 
                           (center_x + 5, segment[1] + self.block_size + 15), 2)