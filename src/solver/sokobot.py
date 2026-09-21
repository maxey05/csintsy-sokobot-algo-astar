import time
import copy 

class SokoBot:
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
                    crates.add(i, j)
                elif itemsData[i][j] == '@':
                    player = ((i, j))

        start = (player, frozenset(crates))

    
        


