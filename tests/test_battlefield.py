# test the battlefield module
from game.battlefield import Battlefield
from game.player import Player
from game.card import Card
from game.card import extra_draw_2, extra_move, destroy_enemy_card_field, place_anywhere, destroy_enemy_card_hand, extra_draw

def test_battlefield():
    battlefield = Battlefield(5, 5)
    player1 = Player("Player 1", [])
    player2 = Player("Player 2", [])
    
    # Set base positions (assuming bases are at opposite ends)
    battlefield.base_positions[player1] = (0, 2)  # Example position
    battlefield.base_positions[player2] = (4, 2)  # Example position
    
    # Test initial state
    assert battlefield.is_valid_move((0, 0), player1) == True
    assert battlefield.is_valid_move((0, 2), player1) == False
    assert battlefield.is_valid_move((4, 2), player1) == True
    assert battlefield.is_valid_move((5, 5), player1) == False
    
    # Test card placement
    card = Card("Test Card")
    battlefield.place_card(card, (1, 1), player1)
    assert battlefield.grid[1][1][0] == card
    assert battlefield.grid[1][1][1] == player1
    
    # Test win condition
    assert battlefield.check_win(player1) == False
    assert battlefield.check_win(player2) == False
    
    battlefield.place_card(Card("Test Card"), (1, 2), player1)
    battlefield.place_card(Card("Test Card"), (1, 3), player1)
    assert battlefield.check_win(player1) == True
    assert battlefield.check_win(player2) == False

    print("All tests pass")

test_battlefield()