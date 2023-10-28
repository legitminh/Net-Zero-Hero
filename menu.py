import pygame
from item import Item

class Menu:
    def __init__(self, screen, width, height, BG_color, border_color, text_color, text_size):
        self.width = width
        self.height = height
        self.screen = screen
        self.slots = []

    def draw(self):
        def make_text(screen, x, y, what, size):
            font = pygame.font.SysFont('arial', int(size))
            text = font.render(str(what), True, 'white')
            text_rect = text.get_rect(topleft=(x, y))
            screen.blit(text, text_rect)
        make_text(self.screen, 10, 10, 'Purchasable buildings', 24)
        make_text(self.screen, 10, 40, '1. Wind ($1B)', 18)
        make_text(self.screen, 10, 70, '2. Solar ($2B)', 18)
        # make_text(self.screen, 10, 10, 'Purchasable buildings', 48)
        # make_text(self.screen, 20, 100, '1. Trees (1B)', 24)
        # make_text(self.screen, 20, 120, '2. Solar Panels (2B)', 24)
        # make_text(self.screen, 20, 140, '3. Nuclear Power Plant (4B)', 24)
        # make_text(self.screen, 20, 160, '4. Direct Air Capture (8B)', 24)


    def update(self, event):
        if event.key == pygame.K_1:
            return ("wind",1)
        if event.key == pygame.K_2:
            return ("solar",2)
            # elif event.key == pygame.K_2:
            #     return (Item(),2)
            # elif event.key == pygame.K_3:
            #     return (Item(),3)
            # elif event.key == pygame.K_4:
            #     return (Item(),4)
