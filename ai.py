from __future__ import absolute_import, division, print_function
import copy
import random
MOVES = {0: 'up', 1: 'left', 2: 'down', 3: 'right'}

class Gametree:
	"""main class for the AI"""
	# Hint: Two operations are important. Grow a game tree, and then compute minimax score.
	# Hint: To grow a tree, you need to simulate the game one step.
	# Hint: Think about the difference between your move and the computer's move.
	def __init__(self, root_state, depth_of_tree, current_score):
                self.root = root_state
                self.depth = depth_of_tree
                self.score = current_score
                self.sim = Simulator()
	# expectimax for computing best move
	def expectimax(self, state):
		pass
	# function to return best decision to game
	def compute_decision(self):
                self.sim.tileMatrix = self.root
                self.tree = Node(self.root, self.score) #SELF.SIM
                for i in range(0, 4):
                        self.sim.move(i)
                        tempNode = Node(self.sim.tileMatrix, self.sim.total_points)
                        self.tree.add(copy.deepcopy(tempNode))
                        self.sim.undo()
                for i in range(0, 4):
                        for x in range(0, self.sim.board_size):
                                for y in range(0, self.sim.board_size):
                                        if self.tree.children[i].state[x][y] == 0:
                                                self.tree.children[i].state[x][y] = 2
                                                temp = Node(self.tree.children[i].state, self.tree.children[i].score)
                                                self.tree.children[i].add(copy.deepcopy(temp))
                                                self.tree.children[i].state[x][y] = 0
                for i in self.tree.children:
                        for k in i.children:
                                k.state.move(0)
                                tempx = Node(k.state, k.score)
                                k.add(copy.deepcopy(tempx))
                                k.state.undo()
                #print("MAX", self.tree.children[0].state)
                #for x in self.tree.children[0].children:
                        #print(x.state)
                        #print(x.score)
                #print("MAX", self.tree.children[1].state)
                #for x in self.tree.children[1].children:
                        #print(x.state)
                        #print(x.score)
                #change this return value when you have implemented the function
                #pass
                return 0

class Node:
        def __init__(self, gameState, totalPoints):
                self.state = gameState
                self.children = []
                self.score = totalPoints 
        def add(self, child):
                self.children.append(child)

class Simulator:
        def __init__(self):
                self.total_points = 0
                self.default_tile = 2
                self.board_size = 4
                #pygame.init()
                #self.surface = pygame.display.set_mode((400, 500), 0, 32)
                #pygame.display.set_caption("2048")
                #self.myfont = pygame.font.SysFont("arial", 40)
                #self.scorefont = pygame.font.SysFont("arial", 30)
                self.tileMatrix = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
                self.undoMat = []
        def move(self, direction):
                self.addToUndo()
                for i in range(0, direction):
                        self.rotateMatrixClockwise()
                if self.canMove():
                        self.moveTiles()
                        self.mergeTiles()
                        #self.placeRandomTile()
                for j in range(0, (4 - direction) % 4):
                        self.rotateMatrixClockwise()
                #return self
                #self.printMatrix()
        def placeRandomTile(self):
                while True:
                        i = random.randint(0,self.board_size-1)
                        j = random.randint(0,self.board_size-1)
                        if self.tileMatrix[i][j] == 0:
                                break
                self.tileMatrix[i][j] = 2
        def moveTiles(self):
                tm = self.tileMatrix
                for i in range(0, self.board_size):
                        for j in range(0, self.board_size - 1):
                                while tm[i][j] == 0 and sum(tm[i][j:]) > 0:
                                        for k in range(j, self.board_size - 1):
                                                tm[i][k] = tm[i][k + 1]
                                        tm[i][self.board_size - 1] = 0
        def mergeTiles(self):
                tm = self.tileMatrix
                for i in range(0, self.board_size):
                        for k in range(0, self.board_size - 1):
                                if tm[i][k] == tm[i][k + 1] and tm[i][k] != 0:
                                        tm[i][k] = tm[i][k] * 2
                                        tm[i][k + 1] = 0
                                        self.total_points += tm[i][k]
                                        self.moveTiles()
        def checkIfCanGo(self):
                tm = self.tileMatrix
                for i in range(0, self.board_size ** 2):
                        if tm[int(i / self.board_size)][i % self.board_size] == 0:
                                return True
                for i in range(0, self.board_size):
                        for j in range(0, self.board_size - 1):
                                if tm[i][j] == tm[i][j + 1]:
                                        return True
                                elif tm[j][i] == tm[j + 1][i]:
                                        return True
                return False
        def reset(self):
                self.total_points = 0
                self.surface.fill(BLACK)
                self.tileMatrix = [[0 for i in range(self.board_size)] for j in range(self.board_size)]
                self.loop()
        def canMove(self):
                tm = self.tileMatrix
                for i in range(0, self.board_size):
                        for j in range(1, self.board_size):
                                if tm[i][j-1] == 0 and tm[i][j] > 0:
                                        return True
                                elif (tm[i][j-1] == tm[i][j]) and tm[i][j-1] != 0:
                                        return True
                return False
        def saveGameState(self):
                f = open("savedata", "w")
                line1 = " ".join([str(self.tileMatrix[int(x / self.board_size)][x % self.board_size])
                            for x in range(0, self.board_size**2)])
                f.write(line1 + "\n")
                f.write(str(self.board_size)  + "\n")
                f.write(str(self.total_points))
                f.close()
        def loadGameState(self):
                f = open("savedata", "r")
                m = (f.readline()).split(' ', self.board_size ** 2)
                self.board_size = int(f.readline())
                self.total_points = int(f.readline())
                for i in range(0, self.board_size ** 2):
                        self.tileMatrix[int(i / self.board_size)][i % self.board_size] = int(m[i])
                f.close()
                self.loop(True)
        def rotateMatrixClockwise(self):
                tm = self.tileMatrix
                for i in range(0, int(self.board_size/2)):
                        for k in range(i, self.board_size- i - 1):
                                temp1 = tm[i][k]
                                temp2 = tm[self.board_size - 1 - k][i]
                                temp3 = tm[self.board_size - 1 - i][self.board_size - 1 - k]
                                temp4 = tm[k][self.board_size - 1 - i]
                                tm[self.board_size - 1 - k][i] = temp1
                                tm[self.board_size - 1 - i][self.board_size - 1 - k] = temp2
                                tm[k][self.board_size - 1 - i] = temp3
                                tm[i][k] = temp4
        def isArrow(self, k):
                return(k == pygame.K_UP or k == pygame.K_DOWN or k == pygame.K_LEFT or k == pygame.K_RIGHT)
        def getRotations(self, k):
                if k == pygame.K_UP:
                        return 0
                elif k == pygame.K_DOWN:
                        return 2
                elif k == pygame.K_LEFT:
                        return 1
                elif k == pygame.K_RIGHT:
                        return 3
        def convertToLinearMatrix(self):
                m = []
                for i in range(0, self.board_size ** 2):
                        m.append(self.tileMatrix[int(i / self.board_size)][i % self.board_size])
                m.append(self.total_points)
                return m
        def addToUndo(self):
                self.undoMat.append(self.convertToLinearMatrix())
        def undo(self):
                if len(self.undoMat) > 0:
                        m = self.undoMat.pop()
                        for i in range(0, self.board_size ** 2):
                                self.tileMatrix[int(i / self.board_size)][i % self.board_size] = m[i]
                        self.total_points = m[self.board_size ** 2]
                        #self.printMatrix()
