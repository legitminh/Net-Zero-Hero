import pygame
from copy import copy
from box import Box, TextBox
from uiClass import Direction, OverflowingOptions


def Menu:
    def __init__(self, screen, width, height, BG_color, border_color, text_color, text_size):
        self.width = width
        self.height = height
        self.screen
        self.slots = []
        self.BG_box = Box(
            screen, 
            lambda x, y: (x / 2 - width, y - height),
            lambda x, y: (width, height),
            background_color=BG_color,
            focused_color=BG_color,
            corner_rounding_amount=10,
            border_color,
            border_size=10,
            Direction.topleft,
            True,
        )
        selection_box_template = TextBox(
            text="TEMP",
            text_color=text_color,
            text_size=text_size,
            text_font="arial",
            text_wrap=True,
            text_justifiaction=Direction.center,
            if_overflowing_text=OverflowingOptions.resize_box_down,
            resize_box_to_text=False,
            margin=10,
            
            box=copy(BG_box)
        )
        self.selection_boxes = [
            copy(selection_box_template).set_text("1. Trees (10)"),
            copy(selection_box_template).set_text("2. Solar Panels (25)"),
            copy(selection_box_template).set_text("3. Nuclear Power plant (100)"),
            copy(selection_box_template).set_text("4. Direct Air Capture (250)"),
        ]

    def draw(self):
        self.BG_box.draw()
        for selection_box in selection_boxes:
            selection_box.draw()

    def update(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                return 1
            elif event.key == pygame.K_2:
                return 2
            elif event.key == pygame.K_3:
                return 3
            elif event.key == pygame.K_4:
                return 4
