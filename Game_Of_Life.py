import pygame
import sys
import random

#[Space] - Start / Pause simulation
#[Left mouse button] - Drawing live cells
#[Right mouse button] - Erasing live cells
#[R] - Randomize live cells
#[C] - Clear grid

# Define Colors
CELL_DEATH = (0, 0, 0)
CELL_ALIVE = (255, 255, 255)
GRID_COLOR = (100, 100, 100)

# Drawing grid
DRAW_GRID = True

# Grid Size
CELL_SIZE = 10
WIDTH = 1600
HEIGHT = 800
GRID_WIDTH = WIDTH // CELL_SIZE
GRID_HEIGHT = HEIGHT // CELL_SIZE

GAME_FPS = 8

# Define mouse buttons
LEFT = 1
RIGHT = 3

class Cell:
    def __init__(self):
        self.alive = False
    
    def set_alive(self, alive):
        self.alive = alive

class GameOfLife:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = [[Cell() for _ in range(height)] for _ in range(width)]
        self.paused = True

    def randomize(self):
        for row in self.grid:
            for cell in row:
                cell.set_alive(random.choice([True, False]))

    def toggle_cell(self, x, y):
        self.grid[x][y].set_alive(not self.grid[x][y].alive)

    def set_cell_alive(self, x, y, alive):
        self.grid[x][y].set_alive(alive)

    def clear(self):
        for row in self.grid:
            for cell in row:
                cell.set_alive(False)

    def update(self):
        new_grid = [[Cell() for _ in range(self.height)] for _ in range(self.width)]
        for x in range(self.width):
            for y in range(self.height):
                alive_neighbors = self.count_alive_neighbors(x, y)
                if self.grid[x][y].alive:
                    new_grid[x][y].set_alive(alive_neighbors in (2, 3))
                else:
                    new_grid[x][y].set_alive(alive_neighbors == 3)
        self.grid = new_grid

    def count_alive_neighbors(self, x, y):
        count = sum(
            self.grid[x + i][y + j].alive
            for i in (-1, 0, 1)
            for j in (-1, 0, 1)
            if (i != 0 or j != 0) and 0 <= x + i < self.width and 0 <= y + j < self.height
        )
        return count

    def count_alive_cells(self):
        return sum(cell.alive for row in self.grid for cell in row)

    def draw(self, screen):
        for x in range(self.width):
            for y in range(self.height):
                color = CELL_ALIVE if self.grid[x][y].alive else CELL_DEATH
                pygame.draw.rect(screen, color, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
                if(DRAW_GRID == True):
                    pygame.draw.rect(screen, GRID_COLOR, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Game of Life")
    clock = pygame.time.Clock()

    game = GameOfLife(GRID_WIDTH, GRID_HEIGHT)
    drawing = False  # Drawing flag
    clearing = False # Erasing flag
    last_pos = None  # Last mouse position
    game_step = 0  # Game step counter

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game.paused = not game.paused
                elif event.key == pygame.K_r:
                    game.randomize()
                elif event.key == pygame.K_c:
                    game.clear()
                    game_step = 0
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == LEFT:
                    drawing = True
                elif event.button == RIGHT:
                    clearing = True
                last_pos = pygame.mouse.get_pos()
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == LEFT:
                    drawing = False
                elif event.button == RIGHT:
                    clearing = False
                last_pos = None

        if drawing or clearing:
            mouseX, mouseY = pygame.mouse.get_pos()
            x, y = mouseX // CELL_SIZE, mouseY // CELL_SIZE
            if last_pos:
                last_x, last_y = last_pos
                last_x //= CELL_SIZE
                last_y //= CELL_SIZE
                dx = x - last_x
                dy = y - last_y
                steps = max(abs(dx), abs(dy))
                if steps > 0:
                    for i in range(steps + 1):
                        interp_x = last_x + (dx * i // steps)
                        interp_y = last_y + (dy * i // steps)
                        game.set_cell_alive(interp_x, interp_y, drawing)
            game.set_cell_alive(x, y, drawing)
            last_pos = (mouseX, mouseY)

        if not game.paused:
            game.update()
            game_step += 1
        
        screen.fill(CELL_DEATH)
        game.draw(screen)

        # Display number of alive cells on the title bar
        alive_cells = game.count_alive_cells()
        if(alive_cells == 0):
            game.paused = True
        
        pygame.display.set_caption(f"Game of Life  |  Alive Cells: {alive_cells:8}  | Step: {game_step} {'- Paused' if game.paused else ''}")

        pygame.display.flip()
        clock.tick(60 if drawing else GAME_FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
