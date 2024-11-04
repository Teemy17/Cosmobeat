import pygame
from constants import GAME

def main_menu(screen, screen_manager):
    screen.fill((0, 0, 0))  

    font = pygame.font.Font(None, 36)
    text = font.render("Press Enter to Start", True, (255, 255, 255))
    screen.blit(text, (100, 100))

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:  
                screen_manager.change_screen(GAME)  

    return True