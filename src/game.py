import pygame
import sys
import os
from bird import Bird
from pipes import PipeManager
from score import Score

class FlappyGame:
    def __init__(self):
        # Initialize pygame
        pygame.init()
        
        # Game constants
        self.SCREEN_WIDTH = 400
        self.SCREEN_HEIGHT = 600
        self.FPS = 60
        self.GRAVITY = 0.5
        self.FLAP_STRENGTH = -8
        self.GROUND_HEIGHT = 100
        
        # Colors
        self.SKY_BLUE = (135, 206, 235)
        self.GROUND_COLOR = (222, 184, 135)
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.RED = (255, 0, 0)
        self.GREEN = (0, 128, 0)
        
        # Setup display
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption("Flappy Bird Clone")
        self.clock = pygame.time.Clock()
        
        # Load fonts
        self.font = pygame.font.SysFont('Arial', 32)
        self.small_font = pygame.font.SysFont('Arial', 24)
        
        # Game objects
        self.bird = Bird(self.SCREEN_WIDTH // 4, self.SCREEN_HEIGHT // 2, 
                        self.SCREEN_HEIGHT - self.GROUND_HEIGHT)
        self.pipe_manager = PipeManager(self.SCREEN_WIDTH, self.SCREEN_HEIGHT - self.GROUND_HEIGHT)
        self.score = Score()
        
        # Game state
        self.game_state = "START"  # START, PLAYING, GAME_OVER
        self.last_pipe_time = pygame.time.get_ticks()
        self.pipe_interval = 1500  # milliseconds
        
    def handle_events(self):
        """Handle pygame events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                    
                if self.game_state == "START" and event.key in (pygame.K_SPACE, pygame.K_UP):
                    self.game_state = "PLAYING"
                    self.bird.flap(self.FLAP_STRENGTH)
                    
                elif self.game_state == "PLAYING" and event.key in (pygame.K_SPACE, pygame.K_UP):
                    self.bird.flap(self.FLAP_STRENGTH)
                    
                elif self.game_state == "GAME_OVER" and event.key == pygame.K_r:
                    self.reset_game()
                    
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.game_state == "START":
                    self.game_state = "PLAYING"
                    self.bird.flap(self.FLAP_STRENGTH)
                elif self.game_state == "PLAYING":
                    self.bird.flap(self.FLAP_STRENGTH)
                elif self.game_state == "GAME_OVER":
                    self.reset_game()
                    
        return True
        
    def update(self):
        """Update game state"""
        if self.game_state != "PLAYING":
            return
            
        # Update bird
        self.bird.update(self.GRAVITY)
        
        # Spawn new pipes
        current_time = pygame.time.get_ticks()
        if current_time - self.last_pipe_time > self.pipe_interval:
            self.pipe_manager.add_pipe()
            self.last_pipe_time = current_time
            
        # Update pipes
        self.pipe_manager.update()
        
        # Check collisions
        if self.bird.check_ground_collision() or self.pipe_manager.check_collision(self.bird):
            self.game_state = "GAME_OVER"
            
        # Check scoring
        if self.pipe_manager.check_scoring(self.bird):
            self.score.increment()
            
    def draw(self):
        """Draw everything"""
        # Background
        self.screen.fill(self.SKY_BLUE)
        
        # Draw clouds (simple circles)
        for i in range(3):
            x = (pygame.time.get_ticks() // 50 + i * 150) % (self.SCREEN_WIDTH + 100) - 50
            y = 80 + i * 60
            pygame.draw.circle(self.screen, self.WHITE, (x, y), 30)
            pygame.draw.circle(self.screen, self.WHITE, (x + 20, y - 10), 25)
            pygame.draw.circle(self.screen, self.WHITE, (x + 40, y), 30)
        
        # Draw pipes
        self.pipe_manager.draw(self.screen)
        
        # Draw ground
        pygame.draw.rect(self.screen, self.GROUND_COLOR, 
                        (0, self.SCREEN_HEIGHT - self.GROUND_HEIGHT, 
                         self.SCREEN_WIDTH, self.GROUND_HEIGHT))
        
        # Draw ground pattern
        for i in range(0, self.SCREEN_WIDTH, 40):
            pygame.draw.rect(self.screen, (200, 160, 120), 
                           (i, self.SCREEN_HEIGHT - self.GROUND_HEIGHT, 20, 20))
        
        # Draw bird
        self.bird.draw(self.screen)
        
        # Draw score
        score_text = self.font.render(str(self.score.value), True, self.WHITE)
        score_shadow = self.font.render(str(self.score.value), True, self.BLACK)
        self.screen.blit(score_shadow, (self.SCREEN_WIDTH // 2 - score_text.get_width() // 2 + 2, 52))
        self.screen.blit(score_text, (self.SCREEN_WIDTH // 2 - score_text.get_width() // 2, 50))
        
        # Draw game state messages
        if self.game_state == "START":
            start_text = self.small_font.render("Press SPACE or CLICK to start", True, self.WHITE)
            self.screen.blit(start_text, (self.SCREEN_WIDTH // 2 - start_text.get_width() // 2, 
                                        self.SCREEN_HEIGHT // 2))
                                        
        elif self.game_state == "GAME_OVER":
            game_over_text = self.font.render("Game Over", True, self.RED)
            restart_text = self.small_font.render("Press R or CLICK to restart", True, self.WHITE)
            final_score = self.small_font.render(f"Score: {self.score.value}", True, self.WHITE)
            
            self.screen.blit(game_over_text, (self.SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, 
                                            self.SCREEN_HEIGHT // 2 - 50))
            self.screen.blit(final_score, (self.SCREEN_WIDTH // 2 - final_score.get_width() // 2, 
                                         self.SCREEN_HEIGHT // 2))
            self.screen.blit(restart_text, (self.SCREEN_WIDTH // 2 - restart_text.get_width() // 2, 
                                          self.SCREEN_HEIGHT // 2 + 40))
        
        pygame.display.flip()
        
    def reset_game(self):
        """Reset game to initial state"""
        self.bird.reset()
        self.pipe_manager.reset()
        self.score.reset()
        self.game_state = "START"
        self.last_pipe_time = pygame.time.get_ticks()
        
    def run(self):
        """Main game loop"""
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(self.FPS)
            
        pygame.quit()
        sys.exit()
