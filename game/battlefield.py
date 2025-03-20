import pygame

class Tile:
    def __init__(self, id):
        self.id = id
        self.connections = []
        self.card = None  # To store the placed card, if any

class Battlefield:
    # def __init__(self, width, height):
    #     self.width = width
    #     self.height = height
    #     self.grid = [[None for _ in range(width)] for _ in range(height)]
    #     self.base_positions = {}  # Stores bases of both players

    def __init__(self):
        # Create the tiles
        base1 = Tile("Base1")
        first_row = [Tile("Row1_1"), Tile("Row1_2")]
        second_row = [Tile("Row2_1"), Tile("Row2_2")]
        third_row = [Tile("Row3_1"), Tile("Row3_2"), Tile("Row3_3")]
        fourth_row = [Tile("Row4_1"), Tile("Row4_2")]
        fifth_row = [Tile("Row5_1"), Tile("Row5_2")]
        base2 = Tile("Base2")
        
        # Set up connections
        base1.connections = first_row
        first_row[0].connections = [second_row[0]]
        first_row[1].connections = [second_row[1]]
        second_row[0].connections = [third_row[0], third_row[1]]
        second_row[1].connections = [third_row[1], third_row[2]]
        third_row[0].connections = [fourth_row[0]]
        third_row[1].connections = [fourth_row[0], fourth_row[1]]
        third_row[2].connections = [fourth_row[1]]
        fourth_row[0].connections = [fifth_row[0]]
        fourth_row[1].connections = [fifth_row[1]]
        fifth_row[0].connections = [base2]
        fifth_row[1].connections = [base2]
        
        # Store all tiles in a list or dict for easy reference
        self.tiles = [base1] + first_row + second_row + third_row + fourth_row + fifth_row + [base2]
        self.base_positions = {base1: "Player1", base2: "Player2"}
    
    def is_valid_move(self, target_tile, player):
        print(f"Validating move for player {player.name} on tile {target_tile.id}")
        card_check = target_tile.card is None
        print(f"Tile {target_tile.id} card is None: {card_check}")

        # If target_tile is directly connected to the player's base, consider move valid.
        if hasattr(player, 'base_position') and player.base_position is not None:
            if target_tile in player.base_position.connections:
                print(f"Tile {target_tile.id} is directly connected to player's base. Move valid.")
                return card_check

        neighbor_valid = False
        for neighbor in target_tile.connections:
            if neighbor.card is not None:
                owner = getattr(neighbor.card, 'owner', None)
                owner_name = owner.name if owner else None
                print(f"Neighbor {neighbor.id} has card {neighbor.card} with owner {owner_name}")
                if owner == player:
                    neighbor_valid = True
            else:
                print(f"Neighbor {neighbor.id} has no card.")
        valid = card_check and neighbor_valid
        print(f"Overall move valid: {valid}")
        return valid
    
    def place_card(self, card, position, player):
        print(f"Placing card {card} for player {player.name} on tile {position.id}")
        position.card = card
        card.owner = player
    
    def check_win(self, player):
        """ Check if a player has formed a chain from their base to the opponent's base """
        # This needs a pathfinding algorithm, such as BFS/DFS
        pass  # Placeholder for now
    
    def render(self):
        pygame.init()

        # Define tile layout: rows with specific number of tiles
        row_lengths = [1, 2, 2, 3, 2, 2, 1]
        tile_size = 100
        margin = 20
        rows = len(row_lengths)
        cols = max(row_lengths)
        width = cols * (tile_size + margin) + margin
        height = rows * (tile_size + margin) + margin
        screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Battlefield")

        # Map each tile to a (x, y) position based on the layout
        positions = {}
        tile_index = 0
        for row_index, num_tiles in enumerate(row_lengths):
            row_width = num_tiles * (tile_size + margin) - margin
            start_x = (width - row_width) // 2
            y = margin + row_index * (tile_size + margin)
            for i in range(num_tiles):
                x = start_x + i * (tile_size + margin)
                if tile_index < len(self.tiles):
                    positions[self.tiles[tile_index]] = (x, y)
                    tile_index += 1
        self.tile_positions = positions
        print("Tile positions mapped:", {tile.id: pos for tile, pos in positions.items()})

        # Fill background
        screen.fill((255, 255, 255))

        # Draw connections between tiles
        for tile in self.tiles:
            start_pos = positions[tile]
            for neighbor in tile.connections:
                if neighbor in positions:
                    end_pos = positions[neighbor]
                    pygame.draw.line(screen, (0, 0, 0),
                                     (start_pos[0] + tile_size//2, start_pos[1] + tile_size//2),
                                     (end_pos[0] + tile_size//2, end_pos[1] + tile_size//2), 2)

        # Draw each tile
        for tile in self.tiles:
            x, y = positions[tile]
            rect = pygame.Rect(x, y, tile_size, tile_size)
            # Use different colors for base, occupied, and regular tiles
            if tile.id.startswith("Base"):
                color = (200, 200, 200)
            elif tile.card:
                color = (255, 200, 200)
            else:
                color = (200, 255, 200)
            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, (0, 0, 0), rect, 2)

            # If the tile has a card, draw the card's name inside the tile
            if tile.card:
                font = pygame.font.SysFont(None, 24)
                text = font.render(str(tile.card), True, (0, 0, 0))
                text_rect = text.get_rect(center=rect.center)
                screen.blit(text, text_rect)

        pygame.display.flip()

        # Draw once and return control to the main game loop
        return