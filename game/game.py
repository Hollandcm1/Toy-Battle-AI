import random

from game.card import Card
from game.battlefield import Battlefield
from game.player import Player
from game.card import extra_draw_2, extra_move, destroy_enemy_card_field, place_anywhere, destroy_enemy_card_hand, extra_draw

def generate_deck():
    """Creates a deck of cards for a player."""
    deck = [
        Card("Skeleton", ability=extra_draw_2),
        Card("Army Soldier", ability=extra_move),
        Card("Knight", ability=destroy_enemy_card_field),
        Card("Monkey", ability=place_anywhere),
        Card("Robot", ability=destroy_enemy_card_hand),
        Card("Unicorn", ability=extra_draw),
        Card("Dinosaur", ability=None)
    ] * 3  # 3 copies of each card

    random.shuffle(deck)
    return deck

def generate_hand(deck):
    """Initializes a player's hand."""
    return [deck.pop() for _ in range(3)]

def setup_game():
    """Initializes the players and battlefield."""
    player1 = Player("Player 1", generate_deck())
    player2 = Player("Player 2", generate_deck())

    battlefield = Battlefield(5, 5)
    
    # Set base positions (assuming bases are at opposite ends)
    battlefield.base_positions[player1] = (0, 2)  # Example position
    battlefield.base_positions[player2] = (4, 2)  # Example position
    
    return player1, player2, battlefield

def game_loop(player1, player2, battlefield):
    """Main turn-based game loop."""
    players = [player1, player2]
    turn = 0

    # wait for user input
    input("Press Enter to start the game...")
    
    while True:
        current_player = players[turn % 2]
        
        print(f"\n{current_player.name}'s turn:")
        current_player.draw_card()
        current_player.show_hand()
        
        # Example move: Play the first card in hand (if available) at a random position
        if current_player.hand:
            card = current_player.hand[0]
            position = (turn % battlefield.width, turn % battlefield.height)  # Example placement logic
            current_player.play_card(card, position, battlefield)
        
        battlefield.display()
        
        # Check win condition
        if battlefield.check_win(current_player):
            print(f"{current_player.name} wins!")
            break
        
        turn += 1

        input("Press Enter to end turn...")