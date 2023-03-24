import pygame, math

pygame.init()
MAX_CELL_X = 5
MAX_CELL_Y = 5

block_size = 70
WINDOW_HEIGHT = MAX_CELL_Y*block_size
WINDOW_WIDTH  = MAX_CELL_X*block_size
inner_block = block_size - 2

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pygame.time.Clock()

class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.dist = math.inf
        self.parent = self
    def __str__(self):
      return f'Cell(\'{self.x}\', {self.y}, {self.dist})'

cell_grid = []

# def get_cell(x,y): return cell_grid[x][y]

def display_cell_grid():
  for y in range (len(cell_grid)):
    for x in range (len(cell_grid[0])):
      print(cell_grid[x][y], end="")
    print()

def init_grid():
  for x in range (0, WINDOW_WIDTH, block_size):
    tmp = []
    for y in range (0, WINDOW_HEIGHT, block_size):
      r = pygame.Rect(x, y, block_size, block_size)
      pygame.draw.rect(screen, "gray", r, 1)
      tmp.append(Cell((int)(x/block_size), (int)(y/block_size)))
    cell_grid.append(tmp)

def fill_cell(x, y, color):
  r = pygame.Rect(block_size*x + 1, block_size*y + 1, inner_block, inner_block)
  pygame.draw.rect(screen, color, r)

def set_wall(x, y):
  print(cell_grid[x][y])
  fill_cell(x, y, "gray")

def set_start(x, y):
  global cell_grid
  print(cell_grid[x][y].dist)
  cell_grid[x][y].dist = 0
  fill_cell(x, y, "red")




















init_grid()
set_start(0,1)
display_cell_grid()
while True:
  for event in pygame.event.get():
    if event.type == pygame.MOUSEBUTTONUP:
      pos_x, pos_y = pygame.mouse.get_pos()
      x, _ = divmod(pos_x, block_size)
      y, _ = divmod(pos_y, block_size)
      set_wall(x, y)
    if event.type == pygame.QUIT:
      pygame.quit()
      sys.exit()
  clock.tick(60)
  pygame.display.update()
pygame.quit()
