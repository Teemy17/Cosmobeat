import pygame
from game import Game
from screen_manager import ScreenManager
from menu import main_menu
from constants import MENU, GAME

def main():
    pygame.init()
    screen_manager = ScreenManager()
    screen = pygame.display.set_mode((1280, 720))
    running = True
    game_instance = Game(1280,720, screen_manager)

    while running:
        if screen_manager.current_screen == MENU:
            running = main_menu(screen, screen_manager)
        elif screen_manager.current_screen == GAME:
            running = game_instance.run()

    pygame.quit()

if __name__ == "__main__":
    main()