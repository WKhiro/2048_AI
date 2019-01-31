# Wesley Kok
# CSE 150 PA2

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
                #NOT USING DEPTH RIGHT NOW
                self.tree = Node(root_state, current_score, 'max', -1) #tree
                self.sim = Simulator() #sim
                self.sim.tileMatrix = root_state
        def growTree(self):
                for i in range(len(MOVES)):
                        lol = copy.deepcopy(self.sim.tileMatrix)
                        self.sim.move(i)
                        if lol != self.sim.tileMatrix:
                                tempNode = Node(self.sim.tileMatrix, self.sim.total_points, 'chance', i)
                                self.tree.add(copy.deepcopy(tempNode))
                        self.sim.undo()
                for i in self.tree.children:
                        self.sim.tileMatrix = i.state
                        for x in range(self.sim.board_size):
                                for y in range(self.sim.board_size):
                                        if self.sim.tileMatrix[x][y] == 0:
                                                self.sim.tileMatrix[x][y] = 2
                                                temp = Node(self.sim.tileMatrix, self.sim.total_points, 'max', -1)
                                                i.add(copy.deepcopy(temp))
                                                self.sim.tileMatrix[x][y] = 0
                for i in self.tree.children:
                        for k in i.children:
                                self.sim.tileMatrix = k.state
                                loly = copy.deepcopy(self.sim.tileMatrix)
                                for x in range(len(MOVES)):
                                        self.sim.move(x)
                                        if loly != self.sim.tileMatrix:
                                                tempx = Node(self.sim.tileMatrix, self.sim.total_points, 'chance', x)
                                                k.add(copy.deepcopy(tempx))
                                        self.sim.undo()
        # expectimax for computing best move
        def expectimax(self, node):#state):
                if len(node.children) == 0:
                        return node.score
                elif node.type == 'max':
                        value = -1
                        for n in node.children:
                                value = max(value, self.expectimax(n))
                        return value
                elif node.type == 'chance':
                        value = 0
                        haha = 0
                        for n in node.children:
                                if (len(n.children) != 0):
                                        haha = (1/len(n.children))
                                value = value + self.expectimax(n)*(haha)
                        return value
                else:
                        print("ERROR")
                        pass
        # function to return best decision to game
        def compute_decision(self):
                self.growTree()
                self.lolx = []
                for n in range(len(self.tree.children)):
                        xd = self.expectimax(self.tree.children[n])
                        #print(xd)
                        self.lolx.append(copy.deepcopy(xd))
                tester = self.lolx.index(max(self.lolx))
                nani = self.tree.children[tester].movex
                #nani = self.expectimax(self.tree)
                #print("LIST", self.lolx)
                #print("HI", nani)
##                for i in self.tree.children:
##                        print("HI", i.state)
##                        for k in i.children:
##                                print("CHANCES", k.state)
##                                for x in k.children:
##                                        print("MOVES AGAIN", x.state)
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
                return nani

class Node:
        def __init__(self, gameState, totalPoints, maxOrChance, move):
                self.state = gameState
                self.score = totalPoints
                self.type = maxOrChance
                self.children = []
                self.movex = move
        def add(self, child):
                self.children.append(child)

class Simulator:
        def __init__(self):
                self.total_points = 0
                self.default_tile = 2
                self.board_size = 4
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
        def canMove(self):
                tm = self.tileMatrix
                for i in range(0, self.board_size):
                        for j in range(1, self.board_size):
                                if tm[i][j-1] == 0 and tm[i][j] > 0:
                                        return True
                                elif (tm[i][j-1] == tm[i][j]) and tm[i][j-1] != 0:
                                        return True
                return False
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
