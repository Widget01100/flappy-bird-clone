import pygame
import random

class Pipe:
    def __init__(self, x, screen_height, ground_height):
        self.x = x
        self.width = 70
        self.gap_height = 150
        self.screen_height = screen_height
        self.ground_height = ground_height
        self.available_height = screen_height - ground_height
        self.passed = False
        
        # Random gap position
        self.gap_y = random.randint(100, self.available_height - 100 - self.gap_height)
        
        # Pipe colors
        self.pipe_color = (0, 180, 0)
        self.pipe_highlight = (0, 220, 0)
        self.pipe_cap_color = (0, 140, 0)
        
    def update(self, speed=3):
        """Move pipe to the left"""
        self.x -= speed
        
    def draw(self, screen):
        """Draw the pipe pair"""
        # Top pipe
        top_pipe_height = self.gap_y
        pygame.draw.rect(screen, self.pipe_color, 
                        (self.x, 0, self.width, top_pipe_height))
        # Top pipe cap
        pygame.draw.rect(screen, self.pipe_cap_color,
                        (self.x - 3, top_pipe_height - 20, self.width + 6, 20))
        # Top pipe highlight
        pygame.draw.rect(screen, self.pipe_highlight,
                        (self.x, 0, 15, top_pipe_height))
        
        # Bottom pipe
        bottom_pipe_y = self.gap_y + self.gap_height
        bottom_pipe_height = self.available_height - bottom_pipe_y
        pygame.draw.rect(screen, self.pipe_color,
                        (self.x, bottom_pipe_y, self.width, bottom_pipe_height))
        # Bottom pipe cap
        pygame.draw.rect(screen, self.pipe_cap_color,
                        (self.x - 3, bottom_pipe_y, self.width + 6, 20))
        # Bottom pipe highlight
        pygame.draw.rect(screen, self.pipe_highlight,
                        (self.x, bottom_pipe_y, 15, bottom_pipe_height))
        
    def get_rects(self):
        """Get collision rectangles for both pipes"""
        top_rect = pygame.Rect(self.x, 0, self.width, self.gap_y)
        bottom_rect = pygame.Rect(self.x, self.gap_y + self.gap_height, 
                                 self.width, self.available_height - (self.gap_y + self.gap_height))
        return top_rect, bottom_rect
        
    def is_off_screen(self):
        """Check if pipe is off screen"""
        return self.x + self.width < 0
        
    def check_collision(self, bird_rect):
        """Check if bird collides with this pipe"""
        top_rect, bottom_rect = self.get_rects()
        return bird_rect.colliderect(top_rect) or bird_rect.colliderect(bottom_rect)
        
    def check_scoring(self, bird):
        """Check if bird passed this pipe for scoring"""
        if not self.passed and bird.x > self.x + self.width:
            self.passed = True
            return True
        return False

class PipeManager:
    def __init__(self, screen_width, ground_level):
        self.screen_width = screen_width
        self.ground_level = ground_level
        self.pipes = []
        self.pipe_speed = 3
        
    def add_pipe(self):
        """Add a new pipe to the right side"""
        new_pipe = Pipe(self.screen_width, self.ground_level, 0)
        self.pipes.append(new_pipe)
        
    def update(self):
        """Update all pipes"""
        for pipe in self.pipes[:]:
            pipe.update(self.pipe_speed)
            if pipe.is_off_screen():
                self.pipes.remove(pipe)
                
    def draw(self, screen):
        """Draw all pipes"""
        for pipe in self.pipes:
            pipe.draw(screen)
            
    def check_collision(self, bird):
        """Check collision with any pipe"""
        bird_rect = bird.get_rect()
        for pipe in self.pipes:
            if pipe.check_collision(bird_rect):
                return True
        return False
        
    def check_scoring(self, bird):
        """Check scoring for all pipes"""
        for pipe in self.pipes:
            if pipe.check_scoring(bird):
                return True
        return False
        
    def reset(self):
        """Remove all pipes"""
        self.pipes = []
