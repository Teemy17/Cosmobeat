import pygame
import button
from constants import GAME

def main_menu(screen, screen_manager):
    screen.fill((0, 0, 0))  

    font = pygame.font.Font(None, 150)
    text = font.render("Cosmobeat", True, (255, 255, 255))
    
    play_img = pygame.image.load("assets/play_button.png").convert_alpha()
    control_img = pygame.image.load("assets/control_button.png").convert_alpha()
    quit_img = pygame.image.load("assets/quit_button.png").convert_alpha()

    play_button = button.Button(520, 285, play_img, 0.45)
    control_button = button.Button(520, 415, control_img, 0.45)
    quit_button = button.Button(520, 545, quit_img, 0.45)
    
    if play_button.draw(screen):
        screen_manager.change_screen(GAME)

    if control_button.draw(screen):
        # screen_manager.change_screen(CONTROL)
        pass
    
    if quit_button.draw(screen):
        return False
    
    screen.blit(text, (370, 100))

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:  
                screen_manager.change_screen(GAME)  

    return True