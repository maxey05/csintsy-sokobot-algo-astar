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
        self.minDist = {}
        self.buildDistanceTable()

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

    def manhattanH(self, crates):
        total = 0

        for crate in crates:
            best = float('inf')
            for goal in self.goals:
                dist = abs(crate[0] - goal[0]) + abs(crate[1] - goal[1])
                if dist < best:
                    best = dist

            total += best

        return total

    def bfsFromGoal(self, goal):
        dist = {goal: 0}
        queue = deque([goal])

        while queue:
            cell = queue.popleft()
            for _, d_row, d_col in MOVES:
                newCell = (cell[0] - d_row, cell[1] - d_col)
                playerCell = (cell[0] - 2 * d_row, cell[1] - 2 * d_col)

                if not (self.isValidCell(newCell) and self.isValidCell(playerCell)):
                    continue
                if newCell in dist:
                    continue

                dist[newCell] = dist[cell] + 1
                queue.append(newCell)

        return dist

    def aStar(self, startState):
        startCrates = startState[1]

        startH = self.heuristic(startCrates)

        if self.isGoal(startCrates):
            return ""
        if startH == float('inf'):
            return ""

        counter = 0

        frontier = []
        heapq.heappush(frontier, (startH, counter, 0, startState))

        bestG = {startState: 0}
        parent = {startState: None}
        expanded = 0

        while frontier:
            f, _, g, state = heapq.heappop(frontier)
            if g > bestG[state]:
                continue

            expanded += 1

            if self.isGoal(state[1]):
                print("expanded", expanded, file=sys.stderr)
                return self.rebuildPath(parent, state)

            player, crates = state

            for moveChar, child in self.successors(player, crates):
                newG = g + 1
                if not newG < bestG.get(child, float('inf')):
                    continue

                h = self.heuristic(child[1])
                if h == float('inf'):
                    continue

                bestG[child] = newG
                parent[child] = (state, moveChar)

                counter += 1

                heapq.heappush(frontier, (newG + h, counter, newG, child))

        return ""

    def heuristic(self, crates):
        total = 0
        for crate in crates:
            d = self.minDist.get(crate)

            if d == None:
                return float('inf')

            total += d

        return total

    def isValidCell(self, cell):
        row, col = cell
        if not (0 <= row < self.height and 0 <= col < self.width):
            return False
        if cell in self.walls:
            return False

        return True

    def buildDistanceTable(self):
        for goal in self.goals:
            table = self.bfsFromGoal(goal)
            for cell, d in table.items():
                self.minDist[cell] = min(d, self.minDist.get(cell, float('inf')))

    def isGoal(self, crates):
        return crates <= self.goals

    def rebuildPath(self, parent, goalState):
        moves = []
        state = goalState

        while parent[state] is not None:
            previousState, moveChar = parent[state]
            moves.append(moveChar)
            state = previousState

        moves.reverse()
        return ''.join(moves)


class SokoBot:
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

        return solver.aStar(startState)

    
        


