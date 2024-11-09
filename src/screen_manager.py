from constants import MENU

class ScreenManager:
    def __init__(self):
        self.current_screen = MENU

    def change_screen(self, new_screen):
        self.current_screen = new_screen