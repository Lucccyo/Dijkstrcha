import pygame, math

pygame.init()
MAX_CELL_X = 5
MAX_CELL_Y = 5

block_size = 40
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
is_finish = False

def display_cell_grid():
  for y in range (len(cell_grid)):
    for x in range (len(cell_grid[0])):
      print(cell_grid[x][y], "\t" , end="")
    print()

def less_dist_unvisited_cell():
  ldist = math.inf
  c = None
  for y in range (len(cell_grid)):
    for x in range (len(cell_grid[0])):
      if cell_grid[x][y].is_visited == False and cell_grid[x][y].dist < ldist:
        ldist = cell_grid[x][y].dist
        c = cell_grid[x][y]
  return c

def printr(tab):
  print("unvisiteds:", end="")
  for c in tab:
    print(c, end="")
  print()

def unvisited_neighbours(cell):
  global cell_grid
  res = []
  if cell.y > 0:
    if cell_grid[cell.x][cell.y - 1].is_visited == False:
      res.append(cell_grid[cell.x][cell.y - 1])
      cell_grid[cell.x][cell.y - 1].parent = cell
  if cell.y < MAX_CELL_Y - 1:
    if cell_grid[cell.x][cell.y + 1].is_visited == False:
      res.append(cell_grid[cell.x][cell.y + 1])
      cell_grid[cell.x][cell.y + 1].parent = cell
  if cell.x > 0:
    if cell_grid[cell.x - 1][cell.y].is_visited == False:
      res.append(cell_grid[cell.x - 1][cell.y])
      cell_grid[cell.x - 1][cell.y].parent = cell
  if cell.x < MAX_CELL_X - 1:
    if cell_grid[cell.x + 1][cell.y].is_visited == False:
      res.append(cell_grid[cell.x + 1][cell.y])
      cell_grid[cell.x + 1][cell.y].parent = cell
  # printr(res)
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
  print("Wall set at : ", cell_grid[x][y])
  cell_grid[x][y].type = "wall"
  fill_cell(x, y, "gray")

def set_start(x, y):
  global cell_grid
  print("Start set at : ", cell_grid[x][y])
  cell_grid[x][y].dist = 0
  cell_grid[x][y].type = " start"
  cell_grid[x][y].is_visited = True
  fill_cell(x, y, "red")
  return cell_grid[x][y]

def set_end(x, y):
  global cell_grid
  print("End set at : ", cell_grid[x][y])
  cell_grid[x][y].type = " end"
  fill_cell(x, y, "yellow")
  return cell_grid[x][y]

def min(a, b):
  # return (if a > b: b else: a)
  if a > b: return b
  else: return a

def traceback(cell):
  global is_finish
  clock.tick(5)
  pygame.display.update()
  fill_cell(cell.x, cell.y, "blue")
  if cell.parent != cell:
    traceback(cell.parent)
  else: is_finish = True

def loop(current, end):
  global cell_grid
  fill_cell(current.x, current.y, "green")
  clock.tick(5)
  pygame.display.update()
  for neighbour in unvisited_neighbours(current):
    neighbour.dist = min(neighbour.dist, current.dist + 1)
  current.is_visited = True
  next_cell = less_dist_unvisited_cell()
  if end.is_visited == True or next_cell == None: traceback(end)
  else:
    loop(next_cell, end)

init_grid()
start = set_start(0,0)
end = set_end(3,1)


while True:
  while not is_finish:
    loop(start, end)
    print("$$")
  for event in pygame.event.get():
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
