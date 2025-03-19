from game.game import generate_deck, setup_game, game_loop

if __name__ == "__main__":
    player1, player2, battlefield = setup_game()
    game_loop(player1, player2, battlefield)