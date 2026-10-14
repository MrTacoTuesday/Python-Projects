import pygame

black = (0, 0, 0)
grey = (50, 50, 50)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
brown = (150, 75, 0)
COLORS = (white, red, green, blue, black, grey, brown)

WIDTH = 24
HEIGHT = 24
MARGIN = 2
grid = []
for row in range(10):
    grid.append([])
    for _ in range(10):
        grid[row].append(0) 
grid[1][5] = 1
pygame.init()
window_size = [260, 260]
scr = pygame.display.set_mode(window_size)
pygame.display.set_caption("Grid")
done = False
clock = pygame.time.Clock()
while not done:
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT: 
            done = True 
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            column = pos[0] // (WIDTH + MARGIN)
            row = pos[1] // (HEIGHT + MARGIN)
            grid[row][column] = (grid[row][column] + 1) % 7
            print("Click ", pos, "Grid coordinates: ", row, column)
    scr.fill(black)
    for row in range(10):
        for column in range(10):
            color = COLORS[grid[row][column]]
            pygame.draw.rect(scr,
                             color,
                             [(MARGIN + WIDTH) * column + MARGIN,
                              (MARGIN + HEIGHT) * row + MARGIN,
                              WIDTH,
                              HEIGHT])
    clock.tick(50)
    pygame.display.flip()
pygame.quit()

