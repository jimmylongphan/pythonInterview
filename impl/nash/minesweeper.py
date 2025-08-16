import random

IN_PROGRESS = "IN_PROGRESS"
WIN = "WIN"
LOSE = "LOSE"

class Cell:
    def __init__(self, row: int, col: int):
        self.row = row
        self.col = col
        self.bomb = 0
        self.neighbor_bomb_count = 0
        self.sweeped = False

class MineSweeper:
    def __init__(self, n: int):
        self.rows = n
        self.cols = n
        self.total_cells = n * n
        self.sweep_count = 0
        self.grid = [[Cell(r, c) for r in range(self.cols)] for c in range(self.rows)]

        max_bombs = float(self.total_cells) * 0.25
        for r in range(self.rows):
            for c in range(self.cols):
                if max_bombs > 0:
                    bomb = random.randint(0,1)
                    if bomb == 1:
                        cell = self.grid[r][c]
                        cell.bomb = bomb
                        max_bombs -= 1
                        self.update_neighbors(r, c)

    def update_neighbors(self, r: int, c: int):
        for r2 in range(r-1, r+2):
            for c2 in range(c-1, c+2):
                if r2 < 0 or r2 >= self.rows or c2 < 0 or c2 >= self.cols:
                    continue

                if r2 == r and c2 == c:
                    continue
                
                # update the neighbor
                neighbor = self.grid[r2][c2]
                neighbor.neighbor_bomb_count += 1

    def sweep_neighbors(self, r: int, c: int):
        for r2 in range(r-1, r+2):
            for c2 in range(c-1, c+2):
                if r2 < 0 or r2 >= self.rows or c2 < 0 or c2 >= self.cols:
                    continue

                if r2 == r and c2 == c:
                    continue
                
                # sweep the neighbor
                neighbor = self.grid[r2][c2]
                neighbor.sweeped = True
                self.sweep_count += 1

    def print_sweep(self):
        print("== SWEEP ==")
        for r in range(self.rows):
            line = ""
            for c in range(self.cols):
                cell = self.grid[r][c]
                if cell.sweeped == True:
                    line += f"{cell.neighbor_bomb_count}\t"
                else:
                    line += f"{[]}\t"
            print(line)

    def print_bombs(self):
        print("== BOMBS ==")
        for r in range(self.rows):
            line = ""
            for c in range(self.cols):
                line += f"{self.grid[r][c].bomb}\t"
            print(line)

    def print_neighbors(self):
        print("== NEIGHBORS ==")
        for r in range(self.rows):
            line = ""
            for c in range(self.cols):
                cell = self.grid[r][c]
                line += f"{cell.neighbor_bomb_count}\t"
            print(line)

    def click(self, r: int, c: int) -> str:
        if r < 0 or r >= self.rows or c < 0 or c >= self.cols:
            print("Invalid row and col")
            return IN_PROGRESS

        cell = self.grid[r][c]
        if cell.sweeped == True:
            print("Cell was already sweeped.")
            return IN_PROGRESS

        if cell.bomb == 1:
            print("Bomb sweeped. You Lose!")
            return LOSE

        # no bomb and not yet sweeped, so sweep it
        cell.sweeped = True
        self.sweep_count += 1

        # sweep neighbors
        self.sweep_neighbors(r, c)

        if self.sweep_count == self.total_cells:
            print("All cells have been sweeped. You Win!")
            return WIN

        return IN_PROGRESS

    def play_game(self):
        status = IN_PROGRESS
        while status == "IN_PROGRESS":
            minesweeper.print_sweep()
            print("Please enter row,col --> ", end="")
            line = input()
            row_str, col_str = line.split()
            row = int(row_str)
            col = int(col_str)
            status = self.click(row, col)

if __name__ == "__main__":
    size = 3
    minesweeper = MineSweeper(size)
    minesweeper.print_bombs()
    minesweeper.print_neighbors()
    minesweeper.play_game()
