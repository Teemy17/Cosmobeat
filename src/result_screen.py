import pygame
from constants import RESULT, MENU
import button

class ResultScreen:
    def __init__(self, screen, screen_manager, game_stats):
        self.screen = screen
        self.screen_manager = screen_manager
        self.game_stats = game_stats
        self.font = pygame.font.Font(None, 48)
        bg = pygame.image.load("../assets/space_bg.jpg").convert_alpha()
        self.bg = pygame.transform.scale(bg, (self.screen.get_width(), self.screen.get_height()))   


    def draw(self):
        self.screen.blit(self.bg, (0, 0))

        # Display the menu button
        menu_img = pygame.image.load("../assets/menu_button.png").convert_alpha()
        menu_button = button.Button(self.screen.get_width() // 2 - 150, 400, menu_img, 0.5)

        if menu_button.draw(self.screen):
            self.screen_manager.change_screen(MENU)
        
        # Display the title
        title_text = self.font.render("Game Results", True, (255, 255, 255))
        title_rect = title_text.get_rect(midtop=(self.screen.get_width() // 2, 50))
        self.screen.blit(title_text, title_rect)

        # Display the score
        score_text = self.font.render(f"Score: {self.game_stats['score']}", True, (255, 255, 255))
        score_rect = score_text.get_rect(midtop=(self.screen.get_width() // 2, 150))
        self.screen.blit(score_text, score_rect)

        # Display the hit counts
        hit_counts_text = self.font.render(
            f"Perfect: {self.game_stats['perfect_count']} | Great: {self.game_stats['great_count']} | Good: {self.game_stats['good_count']} | Miss: {self.game_stats['miss_count']} | Hold: {self.game_stats['hold_count']} | Drag: {self.game_stats['drag_count']}", 
            True, (255, 255, 255)
        )
        hit_counts_rect = hit_counts_text.get_rect(midtop=(self.screen.get_width() // 2, 220))
        self.screen.blit(hit_counts_text, hit_counts_rect)

        # Display the highest combo
        combo_text = self.font.render(f"Highest Combo: {self.game_stats['highest_combo']}", True, (255, 255, 255))
        combo_rect = combo_text.get_rect(midtop=(self.screen.get_width() // 2, 290))
        self.screen.blit(combo_text, combo_rect)
        
        pygame.display.flip()

