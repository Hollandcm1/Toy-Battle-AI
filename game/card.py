
class Card:
    def __init__(self, name, ability=None):
        self.name = name

    def activate_ability(self, battlefield, position, player):
        """Activates the card's special ability if it has one."""
        if self.ability:
            self.ability(battlefield, position, player)
    
    def __repr__(self):
        return self.name
    

def extra_draw(battlefield, position, player):
    """ Grants the player an extra card draw when played. """
    print(f"{player.name} gains an extra card draw!")
    player.draw_card()

def extra_draw_2(battlefield, position, player):
    """ Grants the player 2 extra card draws when played. """
    print(f"{player.name} gains 2 extra card draws!")
    player.draw_card()
    player.draw_card()

def extra_move(battlefield, position, player):
    """ Grants the player an extra move when played. """
    print(f"{player.name} gains an extra move!")

def destroy_enemy_card_field(battlefield, position, player):
    """ Destroys an enemy card when played. """
    print(f"{player.name} destroys an enemy card!")

def destroy_enemy_card_hand(battlefield, position, player):
    """ Destroys an enemy card from their hand when played. """
    print(f"{player.name} destroys an enemy card from their hand!")

def place_anywhere(battlefield, position, player):
    """ Allows the player to place the card anywhere on the battlefield. """
    print(f"{player.name} can place the card anywhere!")