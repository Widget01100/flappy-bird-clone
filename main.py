#!/usr/bin/env python3
"""
Flappy Bird Clone - Main Entry Point
"""
import pygame
import sys
import os

# Add src directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from game import FlappyGame

def main():
    """Main game function"""
    try:
        game = FlappyGame()
        game.run()
    except Exception as e:
        print(f"Error running game: {e}")
        pygame.quit()
        sys.exit(1)

if __name__ == "__main__":
    main()
