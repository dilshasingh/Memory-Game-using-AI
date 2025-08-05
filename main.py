# main.py

import pygame
from constants import SCREEN_WIDTH, SCREEN_HEIGHT
from game import Game
from story import Story
# def main():
#     pygame.init()
#     screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
#     pygame.display.set_caption("Memory Mystery Island")
#     clock = pygame.time.Clock()

#     game = Game(screen)

#     running = True
#     while running:
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 running = False

#         game.update()
#         game.draw()
        
#         pygame.display.flip()
#         clock.tick(60)

#     pygame.quit()

# if __name__ == "__main__":
#     main()

# main.py

# import pygame
# from story import Story

def main():
    pygame.init()
    
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Fantasy Memory Match Game")

    # Create the Story instance
    story = Story(screen)
    story.run()  # Start the storyline display

if __name__ == "__main__":
    main()
