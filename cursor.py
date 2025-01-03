import pygame
from pygame.sprite import Sprite

from load_image import load_image


class Cursor(Sprite):
    def __init__(self, *group):
        super().__init__(*group)

        self.regular_image = load_image('cursor')
        self.pressed_image = load_image('cursor_pressed')
        self.image = self.regular_image

        self.pressed = False
        self.rect = self.image.get_rect()

    def update(self, render=True):
        mouse_pos = pygame.mouse.get_pos()
        mouseFocus = pygame.mouse.get_focused()

        if self.pressed:
            self.image = self.pressed_image
        else:
            self.image = self.regular_image

        if mouseFocus:
            self.rect.topleft = mouse_pos
        else:
            self.rect.topleft = (-100, -100)
