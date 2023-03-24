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
    def __str__(self):
      return f'Cell(\'{self.x}\', {self.y}, {self.dist})'

def i(x, y): return (x + y * MAX_CELL_X)

cell_grid = []
ended = False
# queue = []

def mem(cell, queue):
  for c in queue:
    if c == cell: return True
  return False

def init_grid():
  for x in range (0, WINDOW_WIDTH, block_size):
    for y in range (0, WINDOW_HEIGHT, block_size):
      r = pygame.Rect(x, y, block_size, block_size)
      pygame.draw.rect(screen, "gray", r, 1)
      cell_grid.append(Cell((int)(x/block_size), (int)(y/block_size)))

def fill_cell(x, y, color):
  r = pygame.Rect(block_size*x + 1, block_size*y + 1, inner_block, inner_block)
  pygame.draw.rect(screen, color, r)

def set_wall(x, y):
  fill_cell(x, y, "gray")
  cell_grid[i(x, y)].type = 'w'

def add_to_queue(cell, queue):
  # global queue
  i = 0
  if queue == []:
    queue.append(cell)
    return queue
  else:
    for c in queue:
      if cell.dist > c.dist:
        queue.insert(i-1, cell)
        return queue
      i += 1
  queue.append(cell)
  return queue


def set_start(x, y, queue):
  # global queue
  fill_cell(x, y, "red")
  cell_grid[i(x, y)].type = 's'
  cell_grid[i(x, y)].dist = 0
  queue.append(cell_grid[i(x, y)])
  return queue

def set_end(x, y):
  fill_cell(x, y, "yellow")
  cell_grid[i(x, y)].type = 'e'

def backtrace(start, curr_cell, queue):
  # global queue
  queue = []
  fill_cell(curr_cell.x, curr_cell.y, "blue")
  # return queue
  if curr_cell != start:
    backtrace(start, curr_cell.parent, queue)
    # print("BACKTRACE")
  else: return queue

# def backtrace(start, curr_cell):
#   global queue
#   print("BACKTRACE")
#   queue = []
#   fill_cell(curr_cell.x, curr_cell.y, "blue")
#   if curr_cell != start:
#     return backtrace(start, curr_cell.parent)


def update_neighbour(neighbour, parent, queue):
  # global queue
  fill_cell(neighbour.x, neighbour.y, "green")
  if neighbour.dist == math.inf:
    neighbour.dist = parent.dist + 10
  elif neighbour.dist < parent.dist + 10:
    neighbour.dist = parent.dist + 10
  if not mem(neighbour, queue):
    queue = add_to_queue(neighbour, queue)
  neighbour.parent = parent
  return queue

def iteration(start_cell, end_cell, queue):
  # global queue
  # if queue == []: return queue
  # else:
  curr_cell = queue[0]
  if curr_cell == end_cell: return backtrace(start_cell, end_cell, queue)
  else:
    queue.pop(0)
    fill_cell(curr_cell.x, curr_cell.y, "pink")
    if curr_cell.y > 0:
      queue = update_neighbour(cell_grid[i(curr_cell.x, curr_cell.y - 1)], curr_cell, queue)
      print("len de queue :", len(queue))
    if curr_cell.y < MAX_CELL_Y:
      queue = update_neighbour(cell_grid[i(curr_cell.x, curr_cell.y + 1)], curr_cell, queue)
      print("len de queue :", len(queue))
    if curr_cell.x > 0:
      queue = update_neighbour(cell_grid[i(curr_cell.x - 1, curr_cell.y)], curr_cell, queue)
      print("len de queue :", len(queue))
    if curr_cell.y < MAX_CELL_X:
      queue = update_neighbour(cell_grid[i(curr_cell.x + 1, curr_cell.y)], curr_cell, queue)
      print("len de queue :", len(queue))
    print("len de queue a la fin :", len(queue))
    return queue

init_grid()
queue = []
set_start(0, 0, queue)
set_end(3, 3)

while True:
  if queue != []:
    queue = iteration(cell_grid[i(0, 0)], cell_grid[i(3, 3)], queue)

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
