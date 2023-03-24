import pygame, math

pygame.init()
MAX_CELL_X = 30
MAX_CELL_Y = 30

block_size = 20
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
        self.type = "cell"
        self.is_visited = False
    def __str__(self):
      return f'Cell({self.x}, {self.y}, {self.dist}, {self.type}, {self.is_visited})'

cell_grid = []

def display_cell_grid():
  for y in range (len(cell_grid)):
    for x in range (len(cell_grid[0])):
      print(cell_grid[x][y], "\t" , end="")
    print()

def less_dist_unvisited_cell():
  d = math.inf
  c = None
  for y in range (len(cell_grid)):
    for x in range (len(cell_grid[0])):
      cell = cell_grid[x][y]
      if cell.is_visited == False and cell.dist < d:
        d = cell.dist
        c = cell
  return c

def unvisited_neighbours(cell):
  global cell_grid
  res = []
  if cell.y > 0:
    north = cell_grid[cell.x][cell.y - 1]
    if north.is_visited == False and north.type != "wall":
      res.append(north)
      north.parent = cell
  if cell.y < MAX_CELL_Y - 1:
    south = cell_grid[cell.x][cell.y + 1]
    if south.is_visited == False and south.type != "wall":
      res.append(south)
      south.parent = cell
  if cell.x > 0:
    west = cell_grid[cell.x - 1][cell.y]
    if west.is_visited == False and west.type != "wall":
      res.append(west)
      west.parent = cell
  if cell.x < MAX_CELL_X - 1:
    east = cell_grid[cell.x + 1][cell.y]
    if east.is_visited == False and east.type != "wall":
      res.append(east)
      east.parent = cell
  return res

def init_grid():
  global cell_grid
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
  global cell_grid
  cell_grid[x][y].type = "wall"
  fill_cell(x, y, "gray")

def set_start(x, y):
  global cell_grid
  cell_grid[x][y].dist = 0
  cell_grid[x][y].type = " start"
  cell_grid[x][y].is_visited = True
  fill_cell(x, y, "red")
  return cell_grid[x][y]

def set_end(x, y):
  global cell_grid
  cell_grid[x][y].type = " end"
  fill_cell(x, y, "yellow")
  return cell_grid[x][y]

def min(a, b):
  if a > b: return b
  else: return a

def traceback(cell):
  global is_finish
  clock.tick(30)
  pygame.display.update()
  fill_cell(cell.x, cell.y, "blue")
  if cell.parent != cell: traceback(cell.parent)

def loop(current, end):
  global cell_grid
  fill_cell(current.x, current.y, "green")
  clock.tick(100)
  pygame.display.update()
  for c in unvisited_neighbours(current): c.dist = min(c.dist, current.dist + 1)
  current.is_visited = True
  next_cell = less_dist_unvisited_cell()
  if end.is_visited == True or next_cell == None: traceback(end)
  else:
    loop(next_cell, end)

init_grid()
start = set_start(3,4)
end = set_end(18,23)

while True:
  for event in pygame.event.get():
    if event.type == pygame.KEYDOWN:
      if event.key == pygame.K_SPACE:
        loop(start, end)
    if event.type == pygame.MOUSEBUTTONUP:
      pos_x, pos_y = pygame.mouse.get_pos()
      x, _ = divmod(pos_x, block_size)
      y, _ = divmod(pos_y, block_size)
      set_wall(x, y)
    if event.type == pygame.QUIT:
      pygame.quit()
      sys.exit()
  clock.tick(10)
  pygame.display.update()
pygame.quit()
