from config import CARDS
import random

class Deck():
    def __init__(self, g):
        self.cards = []
        self.g = g
        self.create_deck()
       
    def create_deck(self):
        for card in CARDS:
            c = Card(card['id'], card['image'], card['wasted_image'], card['name'], card['action'], card['description'])
            for i in range(3):
                self.cards.append(c)
        random.shuffle(self.cards)
        self.give_cards()

    def give_cards(self):
        for i in range(2):
            for player in self.g.players:
                player.cards.append(self.cards[0])
                del self.cards[0]

    def new_card(self, player, past_card_action):
        for card in player.cards:
            if card.action == past_card_action:
                player.cards.remove(card)
                self.cards.append(card)
                new_card = self.cards[0]
                player.cards.append(new_card)
                self.cards.remove(new_card)
                return new_card

    def find_card_name(self, card_name, player):
        for card in player.cards:
            if card.name == card_name:
                return card
    
    def leave_card(self, card_to_leave, player):
        for card in player.cards:
            if card.name == card_to_leave.name:
                player.open_cards += ' '+card.name
                player.cards.remove(card)
                break

    def pluralizm(self, player):
        for i in range(2):
            player.cards.append(self.cards[0])
            del self.cards[0]
            
class Card():

    def __init__(self, id, image, wasted_image, name, action, description):
        self.id = id
        self.image = image
        self.wasted_image = wasted_image
        self.name = name
        self.description = description
        self.action = action


