import random
import os
import time
import glob


# Utility function to make random maps

def generate_random_map(filename=None, width=10, height=10, wall_prob=0.2, num_goals=1, min_cost=0, max_cost=9):
    if filename is None:
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        filename = f"map_{timestamp}.txt"

    grid = []

    for y in range(height):
        row = []
        for x in range(width):
            if random.random() < wall_prob:
                row.append('N')  # Wall
            else:
                row.append(round(random.uniform(min_cost, max_cost), 2)) # Cost
        grid.append(row)

    # Add init tiles (S)
    while True:
        sx, sy = random.randint(0, width - 1), random.randint(0, height - 1)
        if grid[sy][sx] != 'W':
            grid[sy][sx] = 'S'
            break

    # Add goals (G)
    for _ in range(num_goals):
        while True:
            gx, gy = random.randint(0, width - 1), random.randint(0, height - 1)
            if grid[gy][gx] not in ('S', 'G', 'W'):
                grid[gy][gx] = 'G'
                break

    # Write to file
    with open(filename, 'w') as f:
        f.write(f"{width} {height}\n")
        for row in grid:
            f.write(" ".join(str(cell) for cell in row) + "\n")

    return os.path.abspath(filename)


def delete_map(filename=None, all_maps=False, directory='.'):
    deleted = []

    if all_maps:
        pattern = os.path.join(directory, "map_*.txt")
        for filepath in glob.glob(pattern):
            try:
                os.remove(filepath)
                deleted.append(filepath)
            except Exception as e:
                print(f"Failed to delete {filepath}: {e}")
    elif filename:
        if not os.path.isfile(filename):
            filename = os.path.join(directory, filename)
        if os.path.isfile(filename):
            try:
                os.remove(filename)
                deleted.append(filename)
            except Exception as e:
                print(f"Failed to delete {filename}: {e}")
        else:
            print(f"File not found: {filename}")
    else:
        print("No filename provided and all_maps is False.")

    return deleted
