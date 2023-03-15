import pygame

pygame.init()
MAX_CELL_X  = 14
MAX_CELL_Y = 14

block_size = 30
WINDOW_HEIGHT = MAX_CELL_Y*block_size
WINDOW_WIDTH  = MAX_CELL_X*block_size
inner_block = block_size - 2

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pygame.time.Clock()

grid = []
# n = none
# w = wall
# s = start
# e = end

def i(x, y): return (x + y * MAX_CELL_X)

def init_grid():
  for x in range (0, WINDOW_WIDTH, block_size):
    for y in range (0, WINDOW_HEIGHT, block_size):
      r = pygame.Rect(x, y, block_size, block_size)
      pygame.draw.rect(screen, "gray", r, 1)
      grid.append('n')
      # grid[(x, y)] = 'n'; # Add new entry

def fill_cell(x, y, color):
  r = pygame.Rect(block_size*x + 1, block_size*y + 1, inner_block, inner_block)
  pygame.draw.rect(screen, color, r)

def set_wall(x, y):
  fill_cell(x, y, "gray")
  grid[i(x, y)] = 'w'

while True:
  init_grid()
  # set start
  grid[i(0, 0)] = 's'
  fill_cell(0, 0, "red")
  # set end
  grid[i(4, 4)] = 'e'
  fill_cell(4, 4, "blue")

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