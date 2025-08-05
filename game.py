# game.py

import pygame
import random
from card import Card
from ai import AI
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, GRID_SIZE, CARD_WIDTH, CARD_HEIGHT, BACKGROUND_COLOR, TEXT_COLOR, POINTS_COLOR

CARD_IMAGES = {
    1:["images/dragon.jpg", "images/potion.jpg", "images/crystal.png", "images/witch_hat.png",
     "images/wand.jpeg", "images/book.jpg", "images/mirror.jpeg", "images/crown.jpg"],
    2:["images/elf.jpeg", "images/unicorn.jpg", "images/fairy.jpeg", "images/treasure.jpg",
     "images/griffin.jpeg", "images/phoenix.png", "images/sword.jpg", "images/shield.png"],
    3:["images/forest.jpg", "images/castle.jpeg", "images/river.jpg", "images/mountain.jpeg",
     "images/portal.jpg", "images/dragon_egg.jpeg", "images/goblin.jpg", "images/troll.jpg"],
    4:["images/starmap.png", "images/constellation.jpg", "images/tellescope.jpg", "images/moon.jpg",
     "images/sun.jpeg", "images/astral_gate.jpeg", "images/shooting_star.png", "images/planet.png"],
    5:["images/royal_seal.jpg", "images/scroll.png", "images/artifact.jpg", "images/banner.jpeg",
     "images/coin.jpg", "images/guard_gate.jpg", "images/tapestry.jpg", "images/emblem.jpg"]
}

GOLDEN_CARDS = {
    1: "images\mapp.jpg",
    2: "images\wisdom.jpg",
    3: "images\compass.png",
    4: "images\crown1.png",
    5: "images\mirror1.jpg"
}

MEMORIES = {
    1 : "The forgotten map holds the secrets of a lost village, hidden deep in the forest.\nWith every step on its ancient trails, the map reveals paths that lead to untold treasures.",
    2 : "This glowing potion is said to grant its drinker unparalleled wisdom and insight.\nA sip from the Potion of Wisdom will unlock the mysteries of the world, one thought at a time.",
    3 : "The celestial compass points not just to the north, but to the heart of the cosmos.\nIt’s said that the compass can guide you to your true destiny, if you know how to listen.",
    4 : "The ancient crown was once worn by the rulers of a mighty kingdom, now lost to time.\nForged from the finest metals, it glows with the power of a forgotten dynasty.",
    5 : "The enchanted mirror shows not only reflections but glimpses into parallel worlds.\nThose who dare look into the mirror may see their true selves or the future that awaits them.",
}


# Colors for buttons and messages
BUTTON_COLOR = (50, 150, 50)  
WINNER_COLOR = (255, 215, 0)  
BUTTON_TEXT_COLOR = (255, 255, 255)  
CARD_BORDER_COLOR = (200, 200, 200)  


CARD_SPACING_HORIZONTAL = 20
CARD_SPACING_VERTICAL = 10
LEFT_PADDING = 30  
TOP_PADDING = 40   

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.level = 1
        self.points = 0
        self.cards = self.shuffle_cards()
        self.player_turn = True
        self.selected_cards = []
        self.ai = AI()
        self.player_score = 0
        self.ai_score = 0
        self.golden_cards_collected = []
        self.max_levels = 5
        self.exit_button = pygame.Rect(SCREEN_WIDTH - 100, SCREEN_HEIGHT - 40, 80, 30)
        self.redo_button = None
        self.next_level_button = None
        self.show_message = False
        self.message_text = ""
        self.turn_message = "Player's Turn"  
        self.golden_card_x = SCREEN_WIDTH // 2 - 50  
        self.golden_card_y = SCREEN_HEIGHT // 2 - 100 

        
        pygame.mixer.init()
        pygame.mixer.music.load("images/1310_Cartoon.mp3")  
        pygame.mixer.music.play(-1)  

    def shuffle_cards(self):
        num_pairs = GRID_SIZE * GRID_SIZE // 2
        
        level_images = CARD_IMAGES.get(self.level, [])
        
        if level_images:
            
            selected_images = random.sample(level_images, num_pairs)
            images = selected_images * 2  
            random.shuffle(images)

            cards = []
            for row in range(GRID_SIZE):
                for col in range(GRID_SIZE):
                    image = images.pop()
                    value = image
                    
                    x = LEFT_PADDING + col * (CARD_WIDTH + CARD_SPACING_HORIZONTAL)
                    y = TOP_PADDING + row * (CARD_HEIGHT + CARD_SPACING_VERTICAL)
                    cards.append(Card(x, y, image, value))
            return cards
        else:
            return []  

    
    def update(self):
        if self.show_message:
            return  

        if self.player_turn:
            self.turn_message = "Player's Turn"
            if pygame.mouse.get_pressed()[0]:  
                mouse_x, mouse_y = pygame.mouse.get_pos()
                for card in self.cards:
                    if (card.x < mouse_x < card.x + CARD_WIDTH and
                        card.y < mouse_y < card.y + CARD_HEIGHT and
                        not card.revealed and not card.matched):
                        card.revealed = True
                        self.selected_cards.append(card)

                        if len(self.selected_cards) == 2:
                            
                            self.draw()
                            pygame.display.flip()
                            pygame.time.delay(500)  

                            
                            if self.selected_cards[0].value == self.selected_cards[1].value:
                                for matched_card in self.selected_cards:
                                    matched_card.matched = True
                                self.player_score += 1
                                self.points += 10
                            else:
                                pygame.time.delay(500)  
                                for card in self.selected_cards:
                                    card.revealed = False
                            self.selected_cards = []
                            self.player_turn = False  
                            pygame.time.delay(500)  
        else:
            
            self.turn_message = "Witch's Turn"
            ai_card1, ai_card2 = self.ai.make_move(self.cards)
            if ai_card1 and ai_card2:
                
                ai_card1.revealed = True
                self.draw()  
                pygame.display.flip()
                pygame.time.delay(1000)  

                
                ai_card2.revealed = True
                self.draw()  
                pygame.display.flip()
                pygame.time.delay(1000)  

                
                if ai_card1.value == ai_card2.value:
                    ai_card1.matched = True
                    ai_card2.matched = True
                    self.ai_score += 1
                else:
                    ai_card1.revealed = False
                    ai_card2.revealed = False

                self.ai.update_memory(ai_card1, ai_card2, self.cards)
                self.player_turn = True  
                pygame.time.delay(500)  

       
        if all(card.matched for card in self.cards):
            self.check_level_completion()

    
    def check_level_completion(self):
        if self.player_score > self.ai_score:
        
            golden_card = GOLDEN_CARDS.get(self.level)
            if golden_card:
                self.golden_cards_collected.append(golden_card)
            self.level += 1
            if self.level > self.max_levels:
                self.show_message = True
                self.message_text = "All memories restored! You have won the game!"
            else:
                self.show_message = True
                self.message_text = "You won the level! Golden card collected."
        else:
            self.show_message = True
            self.message_text = "The Witch won! Try again."
        
        
        self.redo_button = pygame.Rect(SCREEN_WIDTH // 2 - 180, SCREEN_HEIGHT // 2 + 20, 100, 40)
        self.next_level_button = pygame.Rect(SCREEN_WIDTH // 2 + 160, SCREEN_HEIGHT // 2 + 20, 100, 40)

    def reset_game(self):
        """ Reset the game state to start over """
        self.level = 1
        self.points = 0
        self.player_score = 0
        self.ai_score = 0
        self.cards = self.shuffle_cards()
        self.golden_cards_collected = []
        self.player_turn = True
        self.selected_cards = []
        self.show_message = False

    
    def reset_level(self):
        """ Reset the current level while keeping the same level number and new set of images """
        
        level_images = CARD_IMAGES.get(self.level, [])
        
        if level_images:
            
            num_pairs = GRID_SIZE * GRID_SIZE // 2
            images = random.sample(level_images, num_pairs)
            images = images * 2  
            random.shuffle(images)

            self.cards = []
            for row in range(GRID_SIZE):
                for col in range(GRID_SIZE):
                    image = images.pop()
                    value = image
                    
                    x = LEFT_PADDING + col * (CARD_WIDTH + CARD_SPACING_HORIZONTAL)
                    y = TOP_PADDING + row * (CARD_HEIGHT + CARD_SPACING_VERTICAL)
                    self.cards.append(Card(x, y, image, value))
        
        self.player_score = 0
        self.ai_score = 0
        self.player_turn = True
        self.selected_cards = []

    def draw(self):
        self.screen.fill(BACKGROUND_COLOR)
        
       
        if not self.show_message:
            self.draw_grid()  
        
        font = pygame.font.Font(None, 36)
        points_text = font.render(f"Points: {self.points}", True, POINTS_COLOR)
        level_text = font.render(f"Level: {self.level}", True, TEXT_COLOR)
        player_score_text = font.render(f"Player Score: {self.player_score}", True, TEXT_COLOR)
        ai_score_text = font.render(f"AI Score: {self.ai_score}", True, TEXT_COLOR)
        golden_text = font.render(f"Golden Cards: {len(self.golden_cards_collected)}", True, TEXT_COLOR)
        turn_text = font.render(self.turn_message, True, WINNER_COLOR)
        exit_text = font.render("Exit", True, TEXT_COLOR)

        
        self.screen.blit(turn_text, (SCREEN_WIDTH // 2 - turn_text.get_width() // 2, 10))
        self.screen.blit(points_text, (SCREEN_WIDTH - 200, 10))
        self.screen.blit(level_text, (SCREEN_WIDTH - 200, 50))
        self.screen.blit(player_score_text, (SCREEN_WIDTH - 200, 90))
        self.screen.blit(ai_score_text, (SCREEN_WIDTH - 200, 130))
        self.screen.blit(golden_text, (SCREEN_WIDTH - 200, 170))
        pygame.draw.rect(self.screen, TEXT_COLOR, self.exit_button, 2)
        self.screen.blit(exit_text, (SCREEN_WIDTH - 90, SCREEN_HEIGHT - 35))

        if self.show_message:
            self.draw_message()


    def draw_message(self):
        font = pygame.font.Font(None, 36)
        button_font = pygame.font.Font(None, 30) 

        y_offset = SCREEN_HEIGHT // 2 - 60  

        if self.level > 5:  
            final_message = "You have successfully restored the memories of all the lost souls and unlocked their deepest secrets.\nThe journey of rediscovery has come to an end, but the adventure can always begin anew."
            wrapped_final_message = self.wrap_text(final_message, SCREEN_WIDTH - 40)  
            for line in wrapped_final_message:
                final_message_rendered = font.render(line, True, (255, 255, 255))  
                final_message_x = SCREEN_WIDTH // 2 - final_message_rendered.get_width() // 2
                self.screen.blit(final_message_rendered, (final_message_x, y_offset))
                y_offset += final_message_rendered.get_height() + 10  

            self.show_end_buttons(y_offset)  

        else:
            message_text = font.render(self.message_text, True, WINNER_COLOR)
            message_x = SCREEN_WIDTH // 2 - message_text.get_width() // 2
            self.screen.blit(message_text, (message_x, y_offset))
            y_offset += message_text.get_height() + 20  

            if self.golden_cards_collected and self.player_score > self.ai_score:  # Only show the golden card and memory if player won
                card_index = self.level - 1 
                
                golden_card_image = pygame.image.load(GOLDEN_CARDS[card_index + 1])
                golden_card_image = pygame.transform.scale(golden_card_image, (CARD_WIDTH, CARD_HEIGHT))
                golden_card_x = SCREEN_WIDTH // 2 - CARD_WIDTH // 2 
                golden_card_y = y_offset  
                self.screen.blit(golden_card_image, (golden_card_x, golden_card_y))
                y_offset += CARD_HEIGHT + 40  

                memory_text = MEMORIES[card_index + 1]
                wrapped_memory_text = self.wrap_text(memory_text, SCREEN_WIDTH - 40)  
                for line in wrapped_memory_text:
                    memory_rendered = font.render(line, True, (255, 255, 255))  
                    memory_x = SCREEN_WIDTH // 2 - memory_rendered.get_width() // 2
                    self.screen.blit(memory_rendered, (memory_x, y_offset))
                    y_offset += memory_rendered.get_height() + 10  

            if self.redo_button and self.next_level_button:
                self.show_buttons(y_offset)  

    def show_end_buttons(self, y_offset):
        """Display Exit and Restart buttons after all levels are completed"""
        button_font = pygame.font.Font(None, 30)

       
        exit_text = button_font.render("Exit Game", True, BUTTON_TEXT_COLOR)
        pygame.draw.rect(self.screen, BUTTON_COLOR, self.exit_button)
        pygame.draw.rect(self.screen, TEXT_COLOR, self.exit_button, 2)
        self.screen.blit(exit_text, (self.exit_button.x + (self.exit_button.width - exit_text.get_width()) // 2, 
                                    self.exit_button.y + (self.exit_button.height - exit_text.get_height()) // 2))

      
        restart_text = button_font.render("Restart", True, BUTTON_TEXT_COLOR)
        pygame.draw.rect(self.screen, BUTTON_COLOR, self.restart_button)
        pygame.draw.rect(self.screen, TEXT_COLOR, self.restart_button, 2)
        restart_x = self.exit_button.x + self.exit_button.width + 50  
        self.screen.blit(restart_text, (restart_x + (self.restart_button.width - restart_text.get_width()) // 2, 
                                    self.restart_button.y + (self.restart_button.height - restart_text.get_height()) // 2))

    def show_buttons(self, y_offset):
        """Display the redo and next level buttons"""
        font = pygame.font.Font(None, 30)
        
       
        redo_text = font.render("Redo", True, BUTTON_TEXT_COLOR)
        pygame.draw.rect(self.screen, BUTTON_COLOR, self.redo_button)
        pygame.draw.rect(self.screen, TEXT_COLOR, self.redo_button, 2)
        self.screen.blit(redo_text, (self.redo_button.x + (self.redo_button.width - redo_text.get_width()) // 2, 
                                    self.redo_button.y + (self.redo_button.height - redo_text.get_height()) // 2))

       
        next_level_text = font.render("Next Level", True, BUTTON_TEXT_COLOR)
        
        pygame.draw.rect(self.screen, BUTTON_COLOR, self.next_level_button)
        pygame.draw.rect(self.screen, TEXT_COLOR, self.next_level_button, 2)

        button_gap = 100  
        next_level_x = self.redo_button.x + self.redo_button.width + button_gap  
        self.screen.blit(next_level_text, (next_level_x + (self.next_level_button.width - next_level_text.get_width()) // 2 + 140, 
                                        self.next_level_button.y + (self.next_level_button.height - next_level_text.get_height()) // 2))

    def wrap_text(self, text, width):
        """Wraps text to fit within a given width."""
        words = text.split(' ')
        wrapped_lines = []
        current_line = ""

        for word in words:
           
            test_line = current_line + ' ' + word if current_line else word
            test_surface = pygame.font.Font(None, 36).render(test_line, True, (255, 255, 255))
            
            if test_surface.get_width() <= width:
                current_line = test_line  
            else:
                if current_line:  
                    wrapped_lines.append(current_line)
                current_line = word  

        if current_line:  
            wrapped_lines.append(current_line)
        
        return wrapped_lines



    def draw_grid(self):
        for card in self.cards:
            card.draw(self.screen)
           
            pygame.draw.rect(self.screen, CARD_BORDER_COLOR, (card.x, card.y, CARD_WIDTH, CARD_HEIGHT), 2)

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN and self.exit_button.collidepoint(event.pos):
                    running = False
                elif self.show_message and event.type == pygame.MOUSEBUTTONDOWN:
                    if self.redo_button and self.redo_button.collidepoint(event.pos):
                        self.reset_level()
                        self.show_message = False
                    elif self.next_level_button and self.next_level_button.collidepoint(event.pos):
                        self.reset_level()
                        self.show_message = False

            self.update()
            self.draw()
            pygame.display.flip()
        pygame.quit()