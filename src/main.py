import pygame
from game import Game
from screen_manager import ScreenManager

def main():
    pygame.init()
    screen_manager = ScreenManager()
    game_instance = Game(1280,720, screen_manager)
    game_instance.run()

if __name__ == "__main__":
    main()