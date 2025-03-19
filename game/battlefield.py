class Battlefield:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = [[None for _ in range(width)] for _ in range(height)]
        self.base_positions = {}  # Stores bases of both players
    
    def is_valid_move(self, position, player):
        x, y = position
        return 0 <= x < self.width and 0 <= y < self.height and self.grid[y][x] is None
    
    def place_card(self, card, position, player):
        x, y = position
        self.grid[y][x] = (card, player)
    
    def check_win(self, player):
        """ Check if a player has formed a chain from their base to the opponent's base """
        # This needs a pathfinding algorithm, such as BFS/DFS
        pass  # Placeholder for now
    
    def display(self):
        for row in self.grid:
            print([cell[0].name if cell else '.' for cell in row])
        print()