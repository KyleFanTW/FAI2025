# search.py
# ---------------
# Licensing Information:  You are free to use or extend this projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to the University of Illinois at Urbana-Champaign
#
# Created by Michael Abir (abir2@illinois.edu) on 08/28/2018
# Modified by Shang-Tse Chen (stchen@csie.ntu.edu.tw) on 03/03/2022

"""
This is the main entry point for HW1. You should only modify code
within this file -- the unrevised staff files will be used for all other
files and classes when code is run, so be careful to not modify anything else.
"""
# Search should return the path.
# The path should be a list of tuples in the form (row, col) that correspond
# to the positions of the path taken by your search algorithm.
# maze is a Maze object based on the maze from the file specified by input filename
# searchMethod is the search method specified by --method flag (bfs,dfs,astar,astar_multi,fast)

def search(maze, searchMethod):
    return {
        "bfs": bfs,
        "astar": astar,
        "astar_corner": astar_corner,
        "astar_multi": astar_multi,
        "fast": fast,
    }.get(searchMethod)(maze)

def bfs(maze):
    """
    Runs BFS for part 1 of the assignment.

    @param maze: The maze to execute the search on.

    @return path: a list of tuples containing the coordinates of each state in the computed path
    """
    fringe = []
    visited = set()
    start = maze.getStart()
    print(f"Start: {start}")  # Debug print
    fringe.append((start, [start]))  # Store the path along with the current position
    visited.add(start)
    
    while fringe:
        current, path = fringe.pop(0)
        print(f"Current: {current}, Path: {path}")  # Debug print
        if maze.isObjective(current[0], current[1]):
            print("Path found:", path)  # Debug print
            return path
        neighbors = maze.getNeighbors(current[0], current[1])
        print(f"Neighbors: {neighbors}")  # Debug print
        for neighbor in neighbors:
            if neighbor not in visited:
                fringe.append((neighbor, path + [neighbor]))
                visited.add(neighbor)
                print(f"Added to fringe: {neighbor}, New Path: {path + [neighbor]}")  # Debug print

    return []


def astar(maze):
    """
    Runs A star for part 1 of the assignment.

    @param maze: The maze to execute the search on.

    @return path: a list of tuples containing the coordinates of each state in the computed path
    """
    # TODO: Write your code here
    # Use manhattan distance as heuristic
    # f(n) = g(n) + h(n)

    import heapq

    def heuristic(pos, goal):
        return abs(pos[0] - goal[0]) + abs(pos[1] - goal[1])
    
    # Get objective for heuristic calculation
    objectives = maze.getObjectives()
    if not objectives:
        return []
    goal = objectives[0]  # Using first objective for single-goal A*
    
    fringe = []  # Priority queue [(f_value, counter, node, path, cost)]
    visited = {}  # Dictionary to store cost to reach each node
    start = maze.getStart()
    counter = 0  # Tiebreaker for equal f-values
    
    # Initial f-value = 0 (cost so far) + heuristic(start, goal)
    f_value = 0 + heuristic(start, goal)
    heapq.heappush(fringe, (f_value, counter, start, [start], 0))
    visited[start] = 0
    
    while fringe:
        # Get node with lowest f-value
        f, _, current, path, cost = heapq.heappop(fringe)
        
        if current == goal:
            return path
            
        # If we've found a worse path to current, skip it
        if current in visited and visited[current] < cost:
            continue
            
        for neighbor in maze.getNeighbors(current[0], current[1]):
            new_cost = cost + 1  # Assuming uniform step cost
            
            # If we found a better path to neighbor
            if neighbor not in visited or new_cost < visited[neighbor]:
                visited[neighbor] = new_cost
                counter += 1
                f_value = new_cost + heuristic(neighbor, goal)
                heapq.heappush(fringe, (f_value, counter, neighbor, path + [neighbor], new_cost))
    
    return []  # No path found

def astar_corner(maze):
    """
    Runs A star for part 2 of the assignment in the case where there are four corner objectives.

    @param maze: The maze to execute the search on.

    @return path: a list of tuples containing the coordinates of each state in the computed path
        """
    # TODO: Write your code here
    return []

def astar_multi(maze):
    """
    Runs A star for part 3 of the assignment in the case where there are
    multiple objectives.

    @param maze: The maze to execute the search on.

    @return path: a list of tuples containing the coordinates of each state in the computed path
    """
    # TODO: Write your code here
    return []


def fast(maze):
    """
    Runs suboptimal search algorithm for part 4.

    @param maze: The maze to execute the search on.

    @return path: a list of tuples containing the coordinates of each state in the computed path
    """
    # TODO: Write your code here
    return []
