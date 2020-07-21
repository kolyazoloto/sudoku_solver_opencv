
import numpy as np
global grid
grid = [[4, 0, 5, 8, 3, 9, 2, 0, 6],
       [0, 0, 0, 0, 0, 0, 0, 5, 4],
       [7, 2, 0, 5, 6, 4, 8, 1, 0],
       [9, 0, 8, 2, 0, 0, 3, 4, 0],
       [1, 6, 0, 0, 0, 7, 5, 0, 0],
       [2, 0, 7, 0, 4, 0, 0, 0, 0],
       [8, 0, 0, 0, 0, 3, 0, 0, 2],
       [0, 4, 0, 0, 0, 0, 0, 3, 0],
       [3, 9, 0, 0, 0, 1, 7, 0, 0]]

def possible(y,x,n):
    global grid
    for i in range(0,9):
        if grid[y][i] == n:
            return False
    for i in range(0,9):
        if grid[i][x] == n:
            return False
    x0 = (x // 3) * 3
    y0 = (y // 3) * 3
    for i in range(0,3):
        for j in range(0,3):
            if grid[y0+i][x0+j] == n:
                return False
    return True

def solve():
    global grid
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            if grid[y][x] == 0:
                for n in range(1,10):
                    if possible(y,x,n):
                        grid[y][x] = n
                        solve()
                        grid[y][x] = 0
                return
    print(np.matrix(grid))
solve()
