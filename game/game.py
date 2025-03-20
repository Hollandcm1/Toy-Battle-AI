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

    battlefield = Battlefield()
    
    # Set base positions (assuming bases are at opposite ends)
    battlefield.base_positions[player1] = (0, 2)  # Example position
    battlefield.base_positions[player2] = (4, 2)  # Example position
    
    return player1, player2, battlefield

def game_loop(player1, player2, battlefield):
    """Main turn-based game loop."""
    players = [player1, player2]
    turn = 0

    # Initialize Pygame and wait for first event to start the game
    import pygame
    pygame.init()
    
    while True:
        current_player = players[turn % 2]
        
        # Clear screen and render battlefield for current turn
        battlefield.render()
        print(f"\n{current_player.name}'s turn. Choose an action using the buttons below.")
        current_player.show_hand()
        # Get the current screen
        screen = pygame.display.get_surface()
        if screen is None:
            screen = pygame.display.set_mode((800,600))
        width, height = screen.get_size()
        # Define buttons
        draw_button = pygame.Rect(50, height - 100, 150, 50)
        play_button = pygame.Rect(250, height - 100, 150, 50)
        font = pygame.font.SysFont(None, 24)
        # Draw buttons
        pygame.draw.rect(screen, (0, 128, 0), draw_button)
        pygame.draw.rect(screen, (0, 0, 128), play_button)
        draw_text = font.render("Draw Cards", True, (255,255,255))
        play_text = font.render("Play Card", True, (255,255,255))
        screen.blit(draw_text, draw_text.get_rect(center=draw_button.center))
        screen.blit(play_text, play_text.get_rect(center=play_button.center))
        pygame.display.flip()

        waiting_for_action = True
        while waiting_for_action:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    click_pos = pygame.mouse.get_pos()
                    if draw_button.collidepoint(click_pos):
                        current_player.draw_card()
                        current_player.draw_card()
                        waiting_for_action = False
                        break
                    elif play_button.collidepoint(click_pos):
                        if not current_player.hand:
                            print("No cards to play.")
                            waiting_for_action = False
                            break
                        card = current_player.hand[0]
                        print(f"Automatically selected card: {card}")
                        print("Click on a tile to place the card.")
                        waiting_for_tile = True
                        while waiting_for_tile:
                            for tile_event in pygame.event.get():
                                if tile_event.type == pygame.MOUSEBUTTONDOWN and tile_event.button == 1:
                                    click_pos = pygame.mouse.get_pos()
                                    print("Tile click at:", click_pos)
                                    for tile, pos in battlefield.tile_positions.items():
                                        tile_rect = pygame.Rect(pos[0], pos[1], 100, 100)
                                        if tile_rect.collidepoint(click_pos):
                                            print(f"Clicked within tile {tile.id} at rect {tile_rect}")
                                        print(f"Target tile: {tile.id}, Card: {tile.card}, Connections: {[n.id for n in tile.connections]}")
                                        print(f"Current player: {current_player.name}")
                                        if tile.card is None and battlefield.is_valid_move(tile, current_player):
                                                current_player.play_card(card, tile, battlefield)
                                                waiting_for_tile = False
                                                waiting_for_action = False
                                                break
                                    else:
                                        print("Invalid tile. Click on a valid tile.")
                            pygame.time.delay(100)
                        break
            pygame.time.delay(100)
        
        # Removed old tile-click handling; placement is now handled within the Play Card button logic.
        
        # Check win condition
        if battlefield.check_win(current_player):
            print(f"{current_player.name} wins!")
            break
        
        turn += 1

        # End turn automatically after action is taken