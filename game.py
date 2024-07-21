import random
import os
import time
import sys
import tty
import termios
import select

def initialize_grid(rows, cols):
    return [[random.randint(0, 1) for _ in range(cols)] for _ in range(rows)]

def print_grid(grid):
    os.system('cls' if os.name == 'nt' else 'clear')
    print("Game of Life")
    for row in grid:
        print(' '.join(['#' if cell else '.' for cell in row]))
    print("\nPress '+' to increase speed, '-' to decrease speed, 'q' to quit.")

def count_neighbors(grid, row, col):
    neighbors = [
        (-1, -1), (-1, 0), (-1, 1),
        (0, -1),         (0, 1),
        (1, -1), (1, 0), (1, 1)
    ]
    count = 0
    rows = len(grid)
    cols = len(grid[0])
    for dr, dc in neighbors:
        r, c = row + dr, col + dc
        if 0 <= r < rows and 0 <= c < cols:
            count += grid[r][c]
    return count

def update_grid(grid):
    new_grid = [[0 for _ in range(len(grid[0]))] for _ in range(len(grid))]
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            live_neighbors = count_neighbors(grid, r, c)
            if grid[r][c] == 1:
                new_grid[r][c] = 1 if live_neighbors in [2, 3] else 0
            else:
                new_grid[r][c] = 1 if live_neighbors == 3 else 0
    return new_grid

def load_grid_from_file(filename):
    with open(filename, 'r') as f:
        grid = [[int(cell) for cell in line.strip()] for line in f if line.strip()]
    return grid

def get_user_grid():
    print("Enter your grid row by row (0 for dead cell, 1 for live cell).")
    print("When finished, enter an empty line.")
    grid = []
    while True:
        line = input()
        if line == "":
            break
        grid.append([int(cell) for cell in line.strip()])
    return grid

def list_text_files_in_directory():
    files = [f for f in os.listdir() if os.path.isfile(f) and f.lower().endswith('.txt')]
    return files

def read_char():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

def main():
    print("Choose game mode:")
    print("1. Load grid from file")
    print("2. Enter grid manually")
    user_choice = input("Enter 1 or 2: ")

    if user_choice == '1':
        files = list_text_files_in_directory()
        if not files:
            print("No text files found in the current directory.")
            return
        
        print("Available text files:")
        for i, filename in enumerate(files):
            print(f"{i + 1}. {filename}")
        file_choice = int(input("Choose a file by number: ")) - 1
        if 0 <= file_choice < len(files):
            filename = files[file_choice]
            grid = load_grid_from_file(filename)
        else:
            print("Invalid choice.")
            return
    elif user_choice == '2':
        grid = get_user_grid()
    else:
        print("Invalid choice.")
        return

    delay = 0.5
    while True:
        print_grid(grid)
        grid = update_grid(grid)
        time.sleep(delay)

        # Handle speed control and quit option
        i, _, _ = select.select([sys.stdin], [], [], 0.1)
        if i:
            key = read_char()
            if key == '+':
                delay = max(0.1, delay - 0.1)
            elif key == '-':
                delay += 0.1
            elif key == 'q':
                return

if __name__ == '__main__':
    main()
