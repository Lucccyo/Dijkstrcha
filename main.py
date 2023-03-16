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

grid = []
dist = []
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
      dist.append(math.inf)

def fill_cell(x, y, color):
  r = pygame.Rect(block_size*x + 1, block_size*y + 1, inner_block, inner_block)
  pygame.draw.rect(screen, color, r)

def set_wall(x, y):
  fill_cell(x, y, "gray")
  grid[i(x, y)] = 'w'


# def djikstra_h(x, y, xe, ye, prev_val):
#   if x == xe and y == ye:
#     print("return")
#     return 0

#   val = prev_val + 1
#   if t[i(x, y)] == math.inf:
#     print("new explored node")
#     fill_cell(x, y, "green")
#     t[i(x, y)] = val
#   if x == 0 and y == 0:
#     print("on est a ", x, y)
#     if y > 0: djikstra_h(x, y-1, xe, ye, val)
#     if x > 0: djikstra_h(x-1, y, xe, ye, val)
#     if y < MAX_CELL_Y: djikstra_h(x, y+1, xe, ye, val)
#     if x < MAX_CELL_X: djikstra_h(x+1, y, xe, ye, val)
#   return 0
#   # else:
#   #   print("else")




# def djikstra_h(x, y, xe, ye, dpred):
#   print("on est dans ", x, y)
#   if x == xe and y == ye:
#     fill_cell(x, y, "blue")
#   else:
#     if t[i(x, y)] != math.inf:
#       if t[i(x, y)] > dpred + 1:
#         t[i(x, y)] = dpred + 1
#     else:
#       t[i(x, y)] = dpred + 1
#       fill_cell(x, y, "green")
#     # if y > 0:
#       # return djikstra_h(x, y-1, xe, ye, dpred + 1)
#     if y < MAX_CELL_Y-1:
#       return djikstra_h(x, y+1, xe, ye, dpred + 1)
#       # fill_cell(x, y, "blue")
#     # if x > 0:          return djikstra_h(x-1, y, xe, ye, dpred + 1)
#     # if x < MAX_CELL_X: return djikstra_h(x+1, y, xe, ye, dpred + 1)


# def djikstra(xs, ys, xe, ye):
#   t[i(xs, ys)] = 0
#   return(djikstra_h(xs, ys, xe, ye, 0))





init_grid()
# set start
grid[i(0, 0)] = 's'
fill_cell(0, 0, "red")
# set end
grid[i(4, 4)] = 'e'
fill_cell(4, 4, "blue")

# print(t[i(0,0)] != math.inf)

# print("v")


def iter(queue, d, x1, y1):
  x, y = queue[0]
  dist[i(x,y)] = d
  fill_cell(x, y, "green")
  if x == x1 and y == y1:
    fill_cell(x, y, "blue")
    return
  else:
    d = d + 1
    queue.pop(0)
    if y > 0:
      queue.append((x,y-1))
      if dist[i(x,y-1)]== math.inf: fill_cell(x,y-1, "red")
    if y < MAX_CELL_Y-1:
      queue.append((x,y+1))
      if dist[i(x,y+1)] == math.inf: fill_cell(x,y+1, "red")
    if x > 0:
      queue.append((x-1,y))
      if dist[i(x-1,y)] == math.inf: fill_cell(x-1,y, "red")
    if x < MAX_CELL_X-1:
      queue.append((x+1,y))
      if dist[i(x+1,y)] == math.inf: fill_cell(x+1,y, "red")

d = 0
queue = [(0, 0)]

while True:
  if queue != []:
    iter(queue, d, 2, 2)

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