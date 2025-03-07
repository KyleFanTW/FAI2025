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


import heapq
from collections import deque

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
    # call bfsUtil with start and goal
    return bfsUtil(maze, maze.getStart(), maze.getObjectives())

def bfsUtil(maze, start, target):
    """Helper function for fast: finds path from start to target using BFS"""
    
    fringe = []
    visited = set()
    
    #print(f"Start: {start}")  
    fringe.append((start, [start]))  
    visited.add(start)
    
    while fringe:
        current, path = fringe.pop(0)
        #print(f"Current: {current}, Path: {path}")  
        if current == target:
            #print("Path found:", path)  
            return path
        neighbors = maze.getNeighbors(current[0], current[1])
        #print(f"Neighbors: {neighbors}")  
        for neighbor in neighbors:
            if neighbor not in visited:
                fringe.append((neighbor, path + [neighbor]))
                visited.add(neighbor)
                #print(f"Added to fringe: {neighbor}, New Path: {path + [neighbor]}")  

    return []



def ManhattanDistance(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


def astarUtil(maze, start, target, heuristic):
    fringe = [] # Priority queue [(f_value, counter, node, path, cost)]
    visited = {}  # node -> cost
    visited[start] = 0
    tieBreaker = 0
    heapq.heappush(fringe, (heuristic(start, target), tieBreaker, start, [start], 0))
    
    while fringe:
        # Get node with lowest f-value
        _, _, current, path, cost = heapq.heappop(fringe)
        
        if current == target:
            return path
            
        # If we've found a worse path to current, skip it
        if current in visited and visited[current] < cost:
            continue
            
        for neighbor in maze.getNeighbors(current[0], current[1]):
            new_cost = cost + 1  # Assuming uniform step cost
            
            # If we found a better path to neighbor
            if neighbor not in visited or new_cost < visited[neighbor]:
                visited[neighbor] = new_cost
                tieBreaker += 1
                f = new_cost + heuristic(neighbor, target)
                heapq.heappush(fringe, (f, tieBreaker, neighbor, path + [neighbor], new_cost))
    
    return []  


def astar(maze):
    """
    Runs A star for part 1 of the assignment.

    @param maze: The maze to execute the search on.

    @return path: a list of tuples containing the coordinates of each state in the computed path
    """

    return astarUtil(maze, maze.getStart(), maze.getObjectives()[0], ManhattanDistance)
    

def getDist(p1, p2, distFrom):
    if p1 in distFrom:
        return distFrom[p1].get(p2, float('inf'))
    elif p2 in distFrom:
        return distFrom[p2].get(p1, float('inf'))
    else:
        return float('inf')

def mstCost(unvisited, mstUnderSet, distFrom):
    if len(unvisited) <= 1:
        return 0
    if unvisited in mstUnderSet:
        return mstUnderSet[unvisited]

    # build list of edges (dotA, dotB, distance)
    # unvisited is a frozenset of dot positions
    dotsList = list(unvisited)
    edges = []
    for i in range(len(dotsList)):
        for j in range(i+1, len(dotsList)):
            dA, dB = dotsList[i], dotsList[j]
            distAB = getDist(dA, dB, distFrom)
            edges.append((distAB, dA, dB))
    edges.sort(key=lambda x: x[0])

    # Kruskal's MST
    parent = {d: d for d in dotsList}
    rank = {d: 0 for d in dotsList}
    
    def find(x):
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]
    
    def union(a, b):
        rootA, rootB = find(a), find(b)
        if rootA != rootB:
            if rank[rootA] > rank[rootB]:
                parent[rootB] = rootA
            elif rank[rootA] < rank[rootB]:
                parent[rootA] = rootB
            else:
                parent[rootB] = rootA
                rank[rootA] += 1

    cost = 0
    for distVal, dA, dB in edges:
        if find(dA) != find(dB):
            union(dA, dB)
            cost += distVal
    mstUnderSet[unvisited] = cost
    return cost



def astar_corner(maze):
    """
    Solve with specialized astar_multi for 4 corners.
    """
    return astar_multi(maze)


def astar_multi(maze):
    def bfsDistancesFrom(maze, startPos):
        """Return dict mapping cell -> distance from startPos."""
        dist = {}
        queue = deque()
        dist[startPos] = 0
        queue.append(startPos)
        
        while queue:
            cur = queue.popleft()
            for nbr in maze.getNeighbors(cur[0], cur[1]):
                if nbr not in dist:
                    dist[nbr] = dist[cur] + 1
                    queue.append(nbr)
        return dist
  
    # 1) Get all dot positions
    allDots = maze.getObjectives()  # a list of (row,col) for each dot
    allDotsSet = frozenset(allDots)
    start = maze.getStart()

    # 2) Precompute BFS distances from each dot to all cells (or at least dot-to-dot)
    #    Also BFS from the start to all cells, so we can get dist(start, dot).
    #    For example:
    distFrom = {}  # distFrom[pos][cell] = BFS distance from pos to cell
    # Because pos can be start or any dot
    pointsToCompute = allDots + [start]
    for p in pointsToCompute:
        distFrom[p] = bfsDistancesFrom(maze, p)

    mstUnderSet = {}

    # 5) Define our heuristic:
    def multiHeuristic(currentPos, visited):
        # unvisited dots
        unvisited = allDotsSet - visited
        if not unvisited:
            return 0
        # distance to the *closest* unvisited dot
        dist_to_closest = min(getDist(currentPos, dot, distFrom) for dot in unvisited)
        # plus the MST over unvisited
        return dist_to_closest + mstCost(frozenset(unvisited), mstUnderSet, distFrom)

    # 6) A* Search
    # Priority queue holds (f, g, currentPos, visitedSet, path)
    pq = []
    visitedCosts = {}
    startVisited = frozenset([d for d in allDots if d == start])  # if start is itself a dot
    initState = (start, startVisited)
    initH = multiHeuristic(start, startVisited)
    heapq.heappush(pq, (initH, 0, start, startVisited, [start]))
    visitedCosts[initState] = 0

    while pq:
        f, g, curPos, visitedDots, path = heapq.heappop(pq)
        
        # If outdated cost, skip
        if visitedCosts.get((curPos, visitedDots), float('inf')) < g:
            continue
        
        # Goal check
        if len(visitedDots) == len(allDots):
            # Found path visiting all dots
            return path
        
        # Expand neighbors
        for nbr in maze.getNeighbors(curPos[0], curPos[1]):
            newVisited = visitedDots
            if nbr in allDots:
                # Mark it visited
                newVisited = visitedDots | {nbr}
            newG = g + 1
            oldCost = visitedCosts.get((nbr, newVisited), float('inf'))
            if newG < oldCost:
                visitedCosts[(nbr, newVisited)] = newG
                newH = multiHeuristic(nbr, newVisited)
                newF = newG + newH
                heapq.heappush(pq, (newF, newG, nbr, newVisited, path + [nbr]))

    return []  



def fast(maze):
    """
    Runs suboptimal search algorithm for part 4.
    
    @param maze: The maze to execute the search on.
    
    @return path: a list of tuples containing the coordinates of each state in the computed path
    """
    objectives = maze.getObjectives()
    
    current = maze.getStart()
    path = [current]
    unvisited = set(objectives)
    
    while unvisited:

        nearest = min(unvisited, 
                        key=lambda obj: abs(obj[0] - current[0]) + abs(obj[1] - current[1]))
        unvisited.remove(nearest)
        
        # Find path to this nearest objective using BFS
        subpath = bfsUtil(maze, current, nearest)
        if not subpath:  # If no path found (unlikely)
            continue
            
        # Add the path to the nearest objective (excluding the starting point)
        path.extend(subpath[1:])
        current = nearest
        
    return path
