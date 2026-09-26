import time
import heapq
import sys
from collections import deque

MOVES = (('u', -1, 0),
         ('d', 1, 0),
         ('l', 0, -1),
         ('r', 0, 1))

class Solver:
    def __init__(self, width, height, walls, goals, dead=None):
        self.width = width
        self.height = height
        self.walls = walls
        self.goals = goals
        self.dead = dead or set()

    def successors(self, player, crates):
        result = []
        for char, d_row, d_col in MOVES:
            target = (player[0] + d_row, player[1] + d_col)

            if target in self.walls:
                continue

            if target not in crates:
                newState = (target, crates)
                result.append((char, newState))
            else:
                beyond = (target[0] + d_row, target[1] + d_col)
                if beyond in self.walls or beyond in crates:
                    continue
                newCrates = (crates - {target}) | {beyond}
                newState = (target, newCrates)
                result.append((char, newState))

        return result

class SokoBot:
    @staticmethod
    def isGoal(crates, goals):
        return crates <= goals

    def solveSokobanPuzzle(self, width, height, mapData, itemsData):
        # YOU NEED TO REWRITE THE IMPLEMENTATION OF THIS METHOD TO MAKE THE BOT SMARTER
        # Default stupid behavior: Think (sleep) for 3 seconds, and then return a
        # sequence
        # that just moves left and right repeatedly.
        # try:
        #     time.sleep(3)
        # except Exception as ex:
        #     print(ex)
        # return "lrlrlrlrlrlrlrlrlrlrlrlrlrlrlrlrlrlrlrlrlrlrlrlrlrlrlrlrlrlrlrlrlrlrlrlrlrlr"

        walls = set()
        goals = set()
        crates = set()
        player = None

        for i in range(height):
            for j in range(width):
                if mapData[i][j] == '#':
                    walls.add((i, j))
                elif mapData[i][j] == '.':
                    goals.add((i, j))
                if itemsData[i][j] == '$':
                    crates.add((i, j))
                elif itemsData[i][j] == '@':
                    player = ((i, j))

        solver = Solver(width, height, walls, goals)
        startState = (player, frozenset(crates))

        return ""

    
        


