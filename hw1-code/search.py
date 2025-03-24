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


def bfsUtil(maze, start, target):    
    fringe = []
    visited = set()

    fringe.append((start, [start]))  
    visited.add(start)
    
    while fringe:
        current, path = fringe.pop(0)
        if current == target:
            #if maze.isValidPath(path) == "Valid":
            return path
        neighbors = maze.getNeighbors(current[0], current[1])
        for neighbor in neighbors:
            if neighbor not in visited:
                fringe.append((neighbor, path + [neighbor]))
                visited.add(neighbor)

    return []

def astarUtil(maze, start, target, heuristic):
    fringe = [] # Priority queue [(f_value, counter, node, path, cost)]
    visited = {}  # node -> cost
    visited[start] = 0
    tieBreaker = 0
    heapq.heappush(fringe, (heuristic(start, target), tieBreaker, start, [start], 0))
    
    while fringe:
        _, _, current, path, cost = heapq.heappop(fringe)
        if current in visited and visited[current] < cost:
            continue
        if current == target:
            return path
            
        for neighbor in maze.getNeighbors(current[0], current[1]):
            newCost = cost + 1  
            if neighbor not in visited or newCost < visited[neighbor]:
                visited[neighbor] = newCost
                tieBreaker += 1
                f = newCost + heuristic(neighbor, target)
                heapq.heappush(fringe, (f, tieBreaker, neighbor, path + [neighbor], newCost))
    
    return []  

def getDist(p1, p2, distFrom):
    if p1 in distFrom:
        return distFrom[p1].get(p2)
    elif p2 in distFrom:
        return distFrom[p2].get(p1)
    else:
        return float('inf')
    


def mstCost(unvisited, mstUnderSet, distFrom):
    if len(unvisited) <= 1:
        return 0
    if unvisited in mstUnderSet:
        return mstUnderSet[unvisited]

    dotsList = list(unvisited)
    edges = []
    for i in range(len(dotsList)):
        for j in range(i+1, len(dotsList)):
            dA, dB = dotsList[i], dotsList[j]
            distAB = getDist(dA, dB, distFrom)
            edges.append((distAB, dA, dB))

    edges.sort(key=lambda x: x[0])

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


def ManhattanDistance(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

def astar(maze):
    return astarUtil(maze, maze.getStart(), maze.getObjectives()[0], ManhattanDistance)
    
def bfs(maze):
    """
    Runs BFS for part 1 of the assignment.

    @param maze: The maze to execute the search on.

    @return path: a list of tuples containing the coordinates of each state in the computed path
    """
    return bfsUtil(maze, maze.getStart(), maze.getObjectives())

def astar_corner(maze):
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
            for neighbor in maze.getNeighbors(cur[0], cur[1]):
                if neighbor not in dist:
                    dist[neighbor] = dist[cur] + 1
                    queue.append(neighbor)
        return dist
  
    allDots = maze.getObjectives()  
    allDotsSet = frozenset(allDots)
    start = maze.getStart()

    distFrom = {}  # distFrom[src][dst]
    
    for p in allDots + [start]:
        distFrom[p] = bfsDistancesFrom(maze, p)

    mstUnderSet = {}

    def multiHeuristic(currentPos, visited): 
        unvisited = allDotsSet - visited
        if not unvisited:
            return 0
        closeDot = min(getDist(currentPos, dot, distFrom) for dot in unvisited)

        return closeDot + mstCost(frozenset(unvisited), mstUnderSet, distFrom)

    pq = [] #(f, g, currentPos, visitedSet, path)                
    visitedCosts = {}
    startVisited = frozenset()
    if start in allDots:
        startVisited = frozenset({start})
    initState = (start, startVisited)
    initH = multiHeuristic(start, startVisited)
    heapq.heappush(pq, (initH, 0, start, startVisited, [start]))
    visitedCosts[initState] = 0

    while pq:
        _, g, curPos, visitedDots, path = heapq.heappop(pq)
        if len(visitedDots) == len(allDots):
            return path
        if visitedCosts.get((curPos, visitedDots), float('inf')) < g:
            continue
        
        for neighbor in maze.getNeighbors(curPos[0], curPos[1]):
            newVisited = visitedDots
            if neighbor in allDots:
                newVisited = visitedDots | {neighbor}
            newG = g + 1
            oldCost = visitedCosts.get((neighbor, newVisited), float('inf'))
            if newG < oldCost:
                visitedCosts[(neighbor, newVisited)] = newG
                newH = multiHeuristic(neighbor, newVisited)
                newF = newG + newH
                heapq.heappush(pq, (newF, newG, neighbor, newVisited, path + [neighbor]))

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
                        key=lambda obj: ManhattanDistance(current, obj))
        unvisited.remove(nearest)
        
        subpath = bfsUtil(maze, current, nearest)
        if not subpath:  
            continue
        path.extend(subpath[1:])
        current = nearest
        
    return path
