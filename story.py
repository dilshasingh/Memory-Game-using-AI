import pygame
import sys
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, TEXT_COLOR
from game import Game

class Story:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 32)  # Adjusted for readability
        self.story_text = [
            "Welcome to the Fantasy Mystery Island!",
            "Long ago, a wicked witch cast a spell on this land.",
            "The people here have lost their memory and can't recall their past.",
            "To restore their memories, you must embark on a journey.",
            "As you play, you'll unlock memory cards.",
            "Defeat the witch to win back the memories of the people!",
            "Press ENTER to start your adventure!"
        ]
        self.background_image = pygame.image.load("images/back.jpg")  # Replace with your image path

    def run(self):
        while True:
            self.screen.fill((0, 0, 0))  # Fill screen with black to avoid artifacts if no background
            self.display_background()
            self.display_story()
            self.check_for_exit()
            pygame.display.flip()

    def display_background(self):
        self.screen.blit(self.background_image, (0, 0))  # Position the background at the top-left corner

    def display_story(self):
        for i, line in enumerate(self.story_text):
            text = self.font.render(line, True, TEXT_COLOR)
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, 80 + i * 40))
            self.screen.blit(text, text_rect)

    def check_for_exit(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                self.start_game()

    def start_game(self):
        game = Game(self.screen)
        game.run()
