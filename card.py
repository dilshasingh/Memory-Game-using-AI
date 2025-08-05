# card.py

import pygame
from constants import CARD_WIDTH, CARD_HEIGHT, TEXT_COLOR

class Card:
    def __init__(self, x, y, image, value):
        self.x = x
        self.y = y
        self.image = pygame.image.load(image)
        self.image = pygame.transform.scale(self.image, (CARD_WIDTH, CARD_HEIGHT))
        self.value = value
        self.revealed = False
        self.matched = False

    def draw(self, screen):
        if self.revealed or self.matched:
            screen.blit(self.image, (self.x, self.y))
        else:
            pygame.draw.rect(screen, (100, 100, 100), (self.x, self.y, CARD_WIDTH, CARD_HEIGHT))
