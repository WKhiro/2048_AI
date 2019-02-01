# Wesley Kok
# CSE 150 PA2

from __future__ import absolute_import, division, print_function
import copy
import random
MOVES = {0: 'up', 1: 'left', 2: 'down', 3: 'right'}
W = [[6, 5, 4, 3], [5, 4, 3, 2], [4, 3, 2, 1], [3, 2, 1, 0]]
D = 4
class Gametree:
        """main class for the AI"""
        def __init__(self, root_state, depth_of_tree, current_score):
                #NOT USING DEPTH RIGHT NOW
                self.tree = Node(root_state, current_score, 'max') #tree
                self.sim = Simulator() #sim
                self.sim.tileMatrix = root_state
                self.depth = depth_of_tree
        def growTree(self, depth):
#        def growTree(self, node, depth):
##                if depth == 0:
##                        return
##                if depth == 3:
##                        self.sim.tileMatrix = node.state
##                        matrixCopy = copy.deepcopy(node.state)
##                        for x in range(len(MOVES)):
##                                        self.sim.move(x)
##                                        if matrixCopy != self.sim.tileMatrix:
##                                                temp = Node(self.sim.tileMatrix, self.sim.total_points, 'chance', x)
##                                                node.add(copy.deepcopy(temp))
##                                        self.sim.undo()
##                        depth = depth - 1
##                        self.growTree(node, depth)
##                elif depth % 2 == 1:
##                        depth = depth - 1
##                        for i in node.children:
##                                self.sim.tileMatrix = i.state
##                                matrixCopy = copy.deepcopy(self.sim.tileMatrix)
##                                for x in range(len(MOVES)):
##                                        self.sim.move(x)
##                                        if matrixCopy != self.sim.tileMatrix:
##                                                temp = Node(self.sim.tileMatrix, self.sim.total_points, 'chance', x)
##                                                i.add(copy.deepcopy(temp))
##                                                self.growTree(i, depth)
##                                        self.sim.undo()
##                elif depth % 2 == 0:
##                        depth = depth - 1
##                        for i in node.children:
##                                self.sim.tileMatrix = i.state
##                                for x in range(self.sim.board_size):
##                                        for y in range(self.sim.board_size):
##                                                if self.sim.tileMatrix[x][y] == 0:
##                                                        self.sim.tileMatrix[x][y] = 2
##                                                        temp = Node(self.sim.tileMatrix, self.sim.total_points, 'max')
##                                                        i.add(copy.deepcopy(temp))
##                                                        self.sim.tileMatrix[x][y] = 0
##                                                        self.growTree(i, depth)
                if depth == 0:
                        for i in range(len(MOVES)):
                                matrixCopy = copy.deepcopy(self.sim.tileMatrix)
                                self.sim.move(i)
                                if matrixCopy != self.sim.tileMatrix:
                                        temp = Node(self.sim.tileMatrix, self.sim.total_points, 'chance', i)
                                        self.tree.add(copy.deepcopy(temp))
                                self.sim.undo()
                for i in self.tree.children:
                        self.sim.tileMatrix = i.state
                        for x in range(self.sim.board_size):
                                for y in range(self.sim.board_size):
                                        if self.sim.tileMatrix[x][y] == 0:
                                                self.sim.tileMatrix[x][y] = 2
                                                temp = Node(self.sim.tileMatrix, self.sim.total_points, 'max')
                                                i.add(copy.deepcopy(temp))
                                                self.sim.tileMatrix[x][y] = 0
                for i in self.tree.children:
                        for k in i.children:
                                self.sim.tileMatrix = k.state
                                matrixCopy = copy.deepcopy(self.sim.tileMatrix)
                                for x in range(len(MOVES)):
                                        self.sim.move(x)
                                        if matrixCopy != self.sim.tileMatrix:
                                                temp = Node(self.sim.tileMatrix, self.sim.total_points, 'chance', x)
                                                k.add(copy.deepcopy(temp))
                                        self.sim.undo()
        def expectimax(self, node):
                if len(node.children) == 0:
                        score = 0
                        p = 0
                        c = 0
                        for i in range(4):
                                for j in range(4):
                                        if node.state[i][j] != 0:
                                                c += 1
                                        score += node.state[i][j]*W[i][j]
                                        if i < 3:
                                                p += abs(node.state[i][j] - node.state[i+1][j])
                                        if i > 0:
                                                p += abs(node.state[i][j] - node.state[i-1][j])
                                        if j < 3:
                                                p += abs(node.state[i][j] - node.state[i][j+1])
                                        if j > 0:
                                                p += abs(node.state[i][j] - node.state[i][j-1])
                        if c > 10:
                                c = 2
                        else:
                                c = 1
                        #return node.score
                        return (score-p)/c
                elif node.type == 'max':
                        value = -1
                        for n in node.children:
                                value = max(value, self.expectimax(n))
                        return value
                elif node.type == 'chance':
                        value = 0
                        p = 0
                        for n in node.children:
                                if (len(n.children) == 0):
                                        return value
                                else:
                                        for i in range(4):
                                                for j in range(4):
                                                        if i < 3:
                                                                p += abs(node.state[i][j] - node.state[i+1][j])
                                                        if i > 0:
                                                                p += abs(node.state[i][j] - node.state[i-1][j])
                                                        if j < 3:
                                                                p += abs(node.state[i][j] - node.state[i][j+1])
                                                        if j > 0:
                                                                p += abs(node.state[i][j] - node.state[i][j-1])
                                        p = p*5
                                        value = value + self.expectimax(n)*(1/p)#(1/(len(n.children)))
                        return value
                else:
                        print("ERROR")
        # function to return best decision to game
        def compute_decision(self):
                self.growTree(0)
                self.growTree(4)
##                self.growTree(self.tree, 3)
##                self.growTree(self.tree, 2)
                choices = []
                for n in range(len(self.tree.children)):
                        result = self.expectimax(self.tree.children[n])
                        choices.append(copy.deepcopy(result))
                maximum = choices.index(max(choices))
                optimalMove = self.tree.children[maximum].move
                #change this return value when you have implemented the function
                return optimalMove

# Generates nodes for tree      
class Node:
        def __init__(self, gameState, totalPoints, maxOrChance, move = None):
                self.state = gameState
                self.score = totalPoints
                self.type = maxOrChance
                self.move = move
                self.children = []
        # Adds children to node
        def add(self, child):
                self.children.append(child)
        def check(self):
                return self.children == []
                
# Simulator; methods utilized to simulate moves for 2048
class Simulator:
        def __init__(self):
                self.total_points = 0
                self.default_tile = 2
                self.board_size = 4
                self.tileMatrix = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
                self.undoMat = []
        # Removed placing random tiles in order to simulate moves just before said placements
        def move(self, direction):
                self.addToUndo()
                for i in range(0, direction):
                        self.rotateMatrixClockwise()
                if self.canMove():
                        self.moveTiles()
                        self.mergeTiles()
                for j in range(0, (4 - direction) % 4):
                        self.rotateMatrixClockwise()
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
