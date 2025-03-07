import random
import sys
sys.setrecursionlimit(150000)  # Increase as needed, but be careful

from collections import deque

def generate_maze(rows, cols, num_objectives=None):
    # Ensure dimensions are odd.
    if rows % 2 == 0:
        rows -= 1
    if cols % 2 == 0:
        cols -= 1

    # Initialize maze filled with walls.
    maze = [['%'] * cols for _ in range(rows)]
    
    # Define start and goal coordinates.
    start = (1, 1)
    goal = (rows - 2, cols - 2)
    sx, sy = start
    gx, gy = goal

    # Mark start as open.
    maze[sx][sy] = ' '
    
    # Iterative DFS to carve a perfect maze.
    stack = [start]
    while stack:
        x, y = stack[-1]
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        random.shuffle(directions)
        carved = False
        for dx, dy in directions:
            nx, ny = x + dx*2, y + dy*2
            if 1 <= nx < rows - 1 and 1 <= ny < cols - 1 and maze[nx][ny] == '%':
                # Carve a passage between (x,y) and (nx,ny)
                maze[x + dx][y + dy] = ' '
                maze[nx][ny] = ' '
                stack.append((nx, ny))
                carved = True
                break
        if not carved:
            stack.pop()
    
    # Check if the goal is reachable via BFS.
    def is_reachable(maze, start, goal, rows, cols):
        q = deque([start])
        visited = {start}
        while q:
            cx, cy = q.popleft()
            if (cx, cy) == goal:
                return True
            for dx, dy in [(0,1), (1,0), (0,-1), (-1,0)]:
                nx, ny = cx + dx, cy + dy
                if 0 <= nx < rows and 0 <= ny < cols and maze[nx][ny] != '%' and (nx, ny) not in visited:
                    visited.add((nx, ny))
                    q.append((nx, ny))
        return False

    if not is_reachable(maze, start, goal, rows, cols):
        # Get the entire reachable region from start.
        q = deque([start])
        reachable = {start}
        while q:
            cx, cy = q.popleft()
            for dx, dy in [(0,1), (1,0), (0,-1), (-1,0)]:
                nx, ny = cx + dx, cy + dy
                if 0 <= nx < rows and 0 <= ny < cols and maze[nx][ny] != '%' and (nx, ny) not in reachable:
                    reachable.add((nx, ny))
                    q.append((nx, ny))
        # Find the reachable cell closest to the goal.
        closest = None
        min_dist = float('inf')
        for cell in reachable:
            dist = abs(cell[0] - gx) + abs(cell[1] - gy)
            if dist < min_dist:
                min_dist = dist
                closest = cell
        # Carve a randomized corridor from 'closest' to the goal.
        cx, cy = closest
        while (cx, cy) != goal:
            # Calculate differences.
            diff_x = gx - cx
            diff_y = gy - cy
            options = []
            if diff_x != 0:
                options.append(('x', 1 if diff_x > 0 else -1))
            if diff_y != 0:
                options.append(('y', 1 if diff_y > 0 else -1))
            random.shuffle(options)
            axis, step = options[0]
            if axis == 'x':
                cx += step
            else:
                cy += step
            maze[cx][cy] = ' '
    
    # Add extra objectives.
    # If no number is provided, choose a random count between 3 and 7.
    # wall count is % in maze 

    wall_count = sum(row.count('%') for row in maze)
    max_objectives = (rows * cols) - wall_count - 2
    if num_objectives is None:
        num_objectives = random.randint(1, max_objectives)
        # num_objectives = random.randint(60, 110)
    
    # Collect open cells (avoid overwriting start and the goal).
    open_cells = []
    for i in range(rows):
        for j in range(cols):
            if maze[i][j] == ' ' and (i, j) != start and (i, j) != goal:
                open_cells.append((i, j))
    
    # Shuffle and select a subset to place objectives (using '.' as the marker).
    random.shuffle(open_cells)
    objectives = open_cells[:num_objectives]
    for (i, j) in objectives:
        maze[i][j] = '.'
    
    # Restore the start marker.
    maze[sx][sy] = 'P'
    # Ensure the goal marker remains as '.'.
    maze[gx][gy] = '.'
    # --- Modification: Turn 5% of inner wall cells into air ---
    for i in range(1, rows-1):
        for j in range(1, cols-1):
            if maze[i][j] == '%' and random.random() < 0.10:
                maze[i][j] = ' '

    return maze

def print_maze(maze):
    for row in maze:
        print("".join(row))

import argparse 
# Example usage: Generate a 50x50 maze with random extra objectives ('.').
rows, cols = random.randint(5, 30), random.randint(5, 30)
maze = generate_maze(rows, cols)
print_maze(maze)


# 215 change objective number
# 248 change map size
# 238 change the probability of randomly removing walls in the maze to increase complexity
