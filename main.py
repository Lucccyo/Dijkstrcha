import pygame, math

pygame.init()
MAX_CELL_X  = 14
MAX_CELL_Y = 14

block_size = 30
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
        self.type = 'n'
          # n = none
          # w = wall
          # s = start
          # e = end

def i(x, y): return (x + y * MAX_CELL_X)
cell_grid = []

def init_grid():
  for x in range (0, WINDOW_WIDTH, block_size):
    for y in range (0, WINDOW_HEIGHT, block_size):
      r = pygame.Rect(x, y, block_size, block_size)
      pygame.draw.rect(screen, "gray", r, 1)
      cell_grid.append(Cell(x, y))

def fill_cell(x, y, color):
  r = pygame.Rect(block_size*x + 1, block_size*y + 1, inner_block, inner_block)
  pygame.draw.rect(screen, color, r)

def set_wall(x, y):
  fill_cell(x, y, "gray")
  cell_grid[i(x, y)].type = 'w'

def set_start(x, y):
  queue = [(x, y)]
  fill_cell(x, y, "red")
  cell_grid[i(x, y)].type = 's'

def set_end(x, y):
  fill_cell(x, y, "yellow")
  cell_grid[i(x, y)].type = 'e'


# def iteration(queue):
#   curr_cell = queue[0]
#   if curr_cell = target_cell: backtrace()
#   else:
#     queue.pop[0]
#     update_neighbour(curr_cell)
#     # ajout dans la liste et update de G et noter le parent
#     # if y > 0: add(north_cell, queue)
#     # if y < MAX_CELL_Y: add(south_cell, queue)
#     # if x > 0: add(west_cell, queue)
#     # if y < MAX_CELL_X: add(east_cell, queue)

init_grid()
# d = 0
set_start(0, 0)
set_end(6, 7)
while True:
  # if queue != []:
  #   iter(queue, d, 2, 2)

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