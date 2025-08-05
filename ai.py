# ai.py

import random

class AI:
    def __init__(self):
        self.memory = {}
        self.card_probabilities = {}

    def make_move(self, cards):
        self.update_probabilities(cards)
        unknown_cards = [i for i, card in enumerate(cards) if not card.revealed and not card.matched]
        if len(unknown_cards) < 2:
            return None, None

        card1 = self.select_card_based_on_probability(unknown_cards)
        unknown_cards.remove(card1)
        card2 = self.select_card_based_on_probability(unknown_cards)

        return cards[card1], cards[card2]

    def update_memory(self, card1, card2, cards):
        if card1.value not in self.memory:
            self.memory[card1.value] = []
        self.memory[card1.value].append(cards.index(card1))

        if card2.value not in self.memory:
            self.memory[card2.value] = []
        self.memory[card2.value].append(cards.index(card2))

        if card1.value == card2.value:
            self.card_probabilities[card1.value] = 0
        else:
            self.card_probabilities[card1.value] = self.card_probabilities.get(card1.value, 0) + 1
            self.card_probabilities[card2.value] = self.card_probabilities.get(card2.value, 0) + 1

    def update_probabilities(self, cards):
        for i, card in enumerate(cards):
            if not card.revealed and not card.matched:
                self.card_probabilities[i] = 1

        for card_value, positions in self.memory.items():
            if len(positions) == 2:
                for pos in positions:
                    self.card_probabilities[pos] = 0

    def select_card_based_on_probability(self, unknown_cards):
        total_prob = sum(self.card_probabilities[i] for i in unknown_cards)
        if total_prob == 0:
            return random.choice(unknown_cards)

        probabilities = [self.card_probabilities[i] / total_prob for i in unknown_cards]
        return random.choices(unknown_cards, weights=probabilities)[0]
