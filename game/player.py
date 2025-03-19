class Player:
    def __init__(self, name, deck):
        self.name = name
        self.deck = deck  # List of Card objects
        self.hand = []
        self.hand_starting_size = 4
        self.hand_limit = 8
        self.base_position = None  # To be set based on battlefield size
        self.draw_starting_hand()
    
    def draw_card(self):
        if self.deck:
            if len(self.hand) >= self.hand_limit:
                print(f"{self.name}'s hand is full!")
                return
            card = self.deck.pop(0)
            self.hand.append(card)
            print(f"{self.name} draws {card}")
        else:
            print(f"{self.name}'s deck is empty!")

    def draw_starting_hand(self):
        """Draws an initial hand of cards at the start of the game."""
        print(f"{self.name} draws their starting hand:")
        for _ in range(self.hand_starting_size):
            self.draw_card()
    
    def play_card(self, card, position, battlefield):
        if card in self.hand and battlefield.is_valid_move(position, self):
            battlefield.place_card(card, position, self)
            self.hand.remove(card)
            print(f"{self.name} plays {card} at {position}")
        else:
            print(f"Invalid move by {self.name}")

    def show_hand(self):
        print(f"{self.name}'s hand: {self.hand}")