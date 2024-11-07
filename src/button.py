import pygame

class Button:
    def __init__(self, x, y, image, scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False

    def draw(self, surface):
        action = False
        pos = pygame.mouse.get_pos()
        
        # Check if the button is hovered over
        if self.rect.collidepoint(pos):
            # Check if the button is clicked
            if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
                print("Button clicked")
                self.clicked = True
                action = True
        
        # Reset the clicked flag when the mouse button is released
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False
        
        surface.blit(self.image, (self.rect.x, self.rect.y))
        return action