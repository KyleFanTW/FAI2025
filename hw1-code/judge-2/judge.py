# usage: python3 judge.py
# custom testcases credit to B11902130

dir_to_method = {
    "single": "astar",
    "corner": "astar_corner",
    "custom": "astar_multi",
}

file_to_method = {
    "./testcases/multi/tinySearch.txt": "astar_multi",
    "./testcases/multi/smallSearch.txt": "astar_multi",
    "./testcases/multi/mediumSearch.txt": "astar_multi",
    "./testcases/multi/greedySearch.txt": "astar_multi",
    "./testcases/multi/mediumDottedMaze.txt": "astar_multi",

    "./testcases/multi/bigSearch.txt": "fast",
    "./testcases/multi/oddSearch.txt": "fast",
    "./testcases/multi/mediumSearch_prev.txt": "fast",
    "./testcases/multi/openSearch.txt": "fast",
}

answer = {
    "tinyMaze.txt": 9,
    "smallMaze.txt": 20,
    "mediumMaze.txt": 69,
    "bigMaze.txt": 211,
    "openMaze.txt": 55,
    "bigCorners.txt": 163,
    "mediumCorners.txt": 107,
    "tinyCorners.txt": 29,
    "mediumSearch.txt": 169,
    "mediumDottedMaze.txt": 75,
    "smallSearch.txt": 35,
    "tinySearch.txt": 28,
    "greedySearch.txt": 17,
    "custom1.txt": 674,
    "custom2.txt": 586,
    "custom3.txt": 503,
    "custom4.txt": 171,
    "custom5.txt": 47,
    "custom6.txt": 107,
    "custom7.txt": 143,
    "custom8.txt": 145
}

hw1_root = ".."

import sys
sys.path.append(hw1_root)

from os import listdir, path
from maze import Maze
from search import search
import time

if __name__ == "__main__":
    # for each of the dir under maps/ run the method assigned 
    
    for dir in listdir("./testcases/"):
        method = dir_to_method[dir] if dir in dir_to_method else "astar_multi/fast"
        print(f"=====================\nJudging {dir} with {method}\n=====================")
        # for each file under dir 

        for file in listdir(f"./testcases/{dir}"):
            filename = path.join("./testcases/", dir, file)
            maze = Maze(path.abspath(filename))
            method = dir_to_method[dir] if dir in dir_to_method else file_to_method[filename]
            
            # print green pass if using bfs and the assigned method gives same path length 
            # print red fail if using bfs and the assigned method gives different path length 

            print(f"{file}: ", end="")
            t1 = time.time()
            answer_val = answer[file] if file in answer else -1
            ans_path = search(maze, method)
            method_len = len(ans_path)
            elapsed = time.time() - t1

            if answer_val == -1 and 'custom' not in file:
                if elapsed > 1:
                    print(f"\033[93mSLOW\033[0m (elapsed: {elapsed:.2f}s)")
                else:
                    if(maze.isValidPath(ans_path) == "Valid"):
                        print(f"\033[93mFAST and CORRECT\033[0m (elapsed: {elapsed:.2f}s)")
                    else:
                        print(f"\033[93mFAIL\033[0m (elapsed: {elapsed:.2f}s)")
            elif answer_val == method_len:
                print(f"\033[92mPASS\033[0m (elapsed: {elapsed:.2f}s, expanded: {maze.getStatesExplored()})")
            else:
                print(f"\033[91mFAIL\033[0m (ans: {answer_val}, {method}: {method_len})")