import time
import heapq
import sys
from collections import deque

MOVES = (('u', -1, 0),
         ('d', 1, 0),
         ('l', 0, -1),
         ('r', 0, 1))

class Solver:
    def __init__(self, width, height, walls, goals):
        self.width = width
        self.height = height
        self.walls = walls
        self.goals = goals
        self.dead = set()
        self.minDist = {}
        self.buildDistanceTable()
        self.findDeadSquares()

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
                if not self.isSafePush(beyond, newCrates):
                    continue

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
        startPlayer, startCrates = startState

        startH = self.heuristic(startCrates)

        if self.isGoal(startCrates):
            return ""
        if startH == float('inf'):
            return ""

        startReach = self.reachable(startPlayer, startCrates)
        startKey = self.canonicalKey(startReach, startCrates)

        counter = 0
        frontier = [(startH, counter, 0, startState)]
        bestG = {startKey : 0}
        parent = {startKey : None}
        expanded = 0

        while frontier:
            f, _, g, state = heapq.heappop(frontier)
            player, crates = state
            reach = self.reachable(player, crates)
            key = self.canonicalKey(reach, crates)

            if g > bestG[key]:
                continue
            expanded += 1
            if self.isGoal(crates):
                return self.rebuildPath(parent, key)

            for segment, child in self.pushSuccessors(crates, reach):
                childPlayer, childCrates = child
                newG = g + len(segment)
                childReach = self.reachable(childPlayer, childCrates)
                childKey = self.canonicalKey(childReach, childCrates)

                if newG >= bestG.get(childKey, float('inf')):
                    continue

                h = self.heuristic(childCrates)
                if h == float('inf'):
                    continue

                bestG[childKey] = newG
                parent[childKey] = (key, segment)
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

    def isCorner(self, cell):
        row, col = cell
        vertCheck = False
        horiCheck = False

        if (row - 1, col) in self.walls or (row + 1, col) in self.walls:
            vertCheck = True
        if (row, col - 1) in self.walls or (row, col + 1) in self.walls:
            horiCheck = True

        if vertCheck and horiCheck:
            return True
        else:
            return False

    def isGoal(self, crates):
        return crates <= self.goals

    def isFrozenBlock(self, pos, crates):
        row, col = pos
        for i in (-1, 0):
            for j in (-1, 0):
                block = (row + i, col + j), (row + i, col + j + 1), (row + i + 1, col + j), (row + i + 1, col + j + 1)

                if not all(c in self.walls or c in crates for c in block):
                    continue
                if any(c in crates and c not in self.goals for c in block):
                    return True

        return False

    def isSafePush(self, dest, newCrates):
        if dest in self.dead:
            return False
        if self.isFrozenBlock(dest, newCrates):
            return False

        return True

    def buildDistanceTable(self):
            for goal in self.goals:
                table = self.bfsFromGoal(goal)
                for cell, d in table.items():
                    self.minDist[cell] = min(d, self.minDist.get(cell, float('inf')))

    def rebuildPath(self, parent, goalKey):
        pieces = []
        key = goalKey

        while parent[key] is not None:
            key, segment = parent[key]
            pieces.append(segment)

        pieces.reverse()
        return ''.join(pieces)

    def findDeadSquares(self):
        for row in range(self.height):
                for col in range(self.width):
                    cell = (row, col)

                    if cell not in self.walls and cell not in self.minDist:
                        self.dead.add(cell)

    def reachable(self, player, crates):
        cameFrom = {player: None}
        queue = deque([player])
        while queue:
            cell = queue.popleft()
            for char, d_row, d_col in MOVES:
                nxt = (cell[0] + d_row, cell[1] + d_col)

                if nxt in cameFrom or nxt in self.walls or nxt in crates:
                    continue

                cameFrom[nxt] = (cell, char)
                queue.append(nxt)

        return cameFrom

    def walkTo(self, cameFrom, target):
        chars = []
        cell = target

        while cameFrom[cell] is not None:
            cell, char = cameFrom[cell]
            chars.append(char)

        return "".join(reversed(chars))

    def canonicalKey(self, reach, crates):
        return (min(reach), crates)

    def pushSuccessors(self, crates, reach):
        result = []
        for crate in crates:
            for char, d_row, d_col in MOVES:
                behind = (crate[0] - d_row, crate[1] - d_col)
                if behind not in reach:
                    continue

                dest = (crate[0] + d_row, crate[1] + d_col)
                if dest in self.walls or dest in crates:
                    continue

                newCrates = (crates - {crate}) | {dest}
                if not self.isSafePush(dest, newCrates):
                    continue

                segment = self.walkTo(reach, behind) + char
                result.append((segment, (crate, newCrates)))

        return result


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

    
        


