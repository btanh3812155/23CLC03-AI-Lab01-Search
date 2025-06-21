
import pygame
import sys
from map_util import generate_random_map
from main import parse_map, run_with_metrics, bfs, dfs, ucs, a_star, iddfs, bidirectional_bfs, beam_search, ida_star

# Cấu hình
WIDTH, HEIGHT = 640, 480
FPS = 60
MARGIN = 1

# Màu sắc
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
GREY = (200, 200, 200)

# Load map
map_file = generate_random_map(width=20, height=20)
city_map, starts, goals = parse_map(map_file)
start = starts[0]
goal = goals[0]

rows = len(city_map)
cols = len(city_map[0])
CELL_W = WIDTH // cols
CELL_H = HEIGHT // rows

# Thuật toán
algorithms = {
    "1": ("BFS", bfs),
    "2": ("DFS", dfs),
    "3": ("UCS", ucs),
    "4": ("A*", a_star),
    "5": ("IDDFS", iddfs),
    "6": ("Bidirectional BFS", bidirectional_bfs),
    "7": ("Beam Search", beam_search),
    "8": ("IDA*", ida_star),
}
selected_key = "1"

# Khởi tạo Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT + 50))
pygame.display.set_caption("Maze Solver Visualizer")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 24)

def reset_map(width=15, height=15):
    filename = generate_random_map(width=width, height=height)
    city_map, starts, goals = parse_map(filename)
    return city_map, starts[0], goals[0]

def draw_grid(path=[], visited=[]):
    for i in range(rows):
        for j in range(cols):
            cell = city_map[i][j]
            rect = pygame.Rect(j * CELL_W, i * CELL_H, CELL_W - MARGIN, CELL_H - MARGIN)
            color = WHITE
            if (i, j) == start:
                color = GREEN
            elif (i, j) == goal:
                color = RED
            elif (i, j) in path:
                color = BLUE
            elif (i, j) in visited:
                color = YELLOW
            elif cell is None:
                color = BLACK
            pygame.draw.rect(screen, color, rect)
    pygame.draw.rect(screen, GREY, (0, HEIGHT, WIDTH, 50))
    name, _ = algorithms[selected_key]
    text = font.render(f"Selected: {name} | Press SPACE to run | Keys 1–8 to switch | R = New Map", True, (0, 0, 0))
    screen.blit(text, (10, HEIGHT + 10))
def animate_search(visited_order, final_path):
    visited = set()
    for pos in visited_order:
        visited.add(pos)
        draw_grid(path=[], visited=visited)
        pygame.event.pump()              # Cập nhật event queue
        pygame.display.update()         # Cập nhật hiển thị
        pygame.time.wait(50)            # Đợi một chút để người dùng thấy được hiệu ứng

    # Sau khi duyệt xong, vẽ đường đi ngắn nhất
    draw_grid(path=final_path, visited=visited)
    pygame.display.update()

def main():
    global selected_key
    global city_map, start, goal, rows, cols, CELL_W, CELL_H, selected_key
    city_map, start, goal = reset_map(width=20, height=20)
    rows = len(city_map)
    cols = len(city_map[0])
    CELL_W = WIDTH // cols
    CELL_H = HEIGHT // rows
    path = []
    visited = []
    stats = None
    running = True

    while running:
        clock.tick(FPS)
        screen.fill(WHITE)
        draw_grid(path, visited)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    _, algo = algorithms[selected_key]
                    stats = run_with_metrics(algo, city_map, start, goal)
                    path = stats['path'] if stats['path'] else []
                    visited_order = stats['visited_order']
                    animate_search(visited_order, path)
                    visited = visited_order
                    print(f"Algorithm: {algorithms[selected_key][0]}")
                    print(f"Steps: {stats['steps']} | Cost: {stats['cost']} | Nodes: {stats['nodes_explored']}")
                    print(f"Time: {stats['time_seconds']:.4f}s | Memory: {stats['memory_bytes'] / 1024:.2f} KB")
                
                elif event.key == pygame.K_r:
                    city_map, start, goal = reset_map(width=20, height=20)
                    rows = len(city_map)
                    cols = len(city_map[0])
                    CELL_W = WIDTH // cols
                    CELL_H = HEIGHT // rows
                    path = []
                    visited = []
                    draw_grid(path=[], visited=[])
                    pygame.display.flip()
                    print("✅ Đã tạo bản đồ mới.")


                elif event.unicode in algorithms:
                    selected_key = event.unicode

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
