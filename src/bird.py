import pygame
import math

class Bird:
    def __init__(self, x, y, ground_level):
        self.original_x = x
        self.original_y = y
        self.x = x
        self.y = y
        self.velocity = 0
        self.radius = 15
        self.ground_level = ground_level
        self.rotation = 0
        self.flap_animation = 0
        
        # Bird colors
        self.body_color = (255, 255, 0)  # Yellow
        self.beak_color = (255, 165, 0)  # Orange
        self.eye_color = (0, 0, 0)       # Black
        self.wing_color = (255, 140, 0)  # Darker orange
        
    def flap(self, strength):
        """Make the bird flap (jump)"""
        self.velocity = strength
        self.flap_animation = 5
        
    def update(self, gravity):
        """Update bird position and physics"""
        self.velocity += gravity
        self.y += self.velocity
        
        # Calculate rotation based on velocity
        self.rotation = max(-30, min(90, -self.velocity * 3))
        
        # Update flap animation
        if self.flap_animation > 0:
            self.flap_animation -= 1
            
        # Keep bird on screen
        if self.y - self.radius < 0:
            self.y = self.radius
            self.velocity = 0
            
    def check_ground_collision(self):
        """Check if bird hit the ground"""
        return self.y + self.radius >= self.ground_level
        
    def draw(self, screen):
        """Draw the bird with rotation and animation"""
        # Create a surface for the bird to allow rotation
        bird_surface = pygame.Surface((self.radius * 4, self.radius * 4), pygame.SRCALPHA)
        
        # Draw body
        pygame.draw.circle(bird_surface, self.body_color, 
                         (self.radius * 2, self.radius * 2), self.radius)
        
        # Draw wing (animated)
        wing_offset = math.sin(pygame.time.get_ticks() / 200) * 2 if self.flap_animation == 0 else 3
        wing_points = [
            (self.radius * 2 - 10, self.radius * 2),
            (self.radius * 2 - 20, self.radius * 2 - wing_offset),
            (self.radius * 2 - 10, self.radius * 2 - 5)
        ]
        pygame.draw.polygon(bird_surface, self.wing_color, wing_points)
        
        # Draw beak
        beak_points = [
            (self.radius * 2 + self.radius - 5, self.radius * 2),
            (self.radius * 2 + self.radius + 10, self.radius * 2 - 3),
            (self.radius * 2 + self.radius + 10, self.radius * 2 + 3)
        ]
        pygame.draw.polygon(bird_surface, self.beak_color, beak_points)
        
        # Draw eye
        pygame.draw.circle(bird_surface, self.eye_color, 
                         (self.radius * 2 + 8, self.radius * 2 - 5), 4)
        pygame.draw.circle(bird_surface, (255, 255, 255), 
                         (self.radius * 2 + 9, self.radius * 2 - 6), 1)
        
        # Rotate the bird surface
        rotated_bird = pygame.transform.rotate(bird_surface, self.rotation)
        
        # Get the rect of rotated surface and center it on bird position
        rotated_rect = rotated_bird.get_rect(center=(self.x, self.y))
        
        # Draw to screen
        screen.blit(rotated_bird, rotated_rect)
        
    def reset(self):
        """Reset bird to starting position"""
        self.x = self.original_x
        self.y = self.original_y
        self.velocity = 0
        self.rotation = 0
        self.flap_animation = 0
        
    def get_rect(self):
        """Get collision rectangle"""
        return pygame.Rect(self.x - self.radius, self.y - self.radius, 
                          self.radius * 2, self.radius * 2)
