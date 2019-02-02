# Wesley Kok
# CSE 150 PA2
#
# NOTE: 2048.py currently requests a depth '5' tree.

from __future__ import absolute_import, division, print_function
import copy
import random
MOVES = {0: 'up', 1: 'left', 2: 'down', 3: 'right'}
WEIGHTS = [[6, 5, 4, 3], [5, 4, 3, 2], [4, 3, 2, 1], [3, 2, 1, 0]] # Weighted tile matrix

# Constructs game tree and computes optimal moves
class Gametree:
        """main class for the AI"""
        def __init__(self, root_state, depth_of_tree, current_score):
                self.tree = Node(root_state, current_score, 'max')      # Root node (MAX player)
                self.depth = depth_of_tree                              # Depth of desired tree
                self.sim = Simulator()                                  # Game simulator 
        # Grows out a tree of simulated moves from the root game state
        # PERSONAL NOTE: Uses loops rather than recursion; recursion took up too
        #                stack space, resulting in extremely slow computations
        def growTree(self, depth = None):
                # Expand the root node
                if depth == self.depth:
                        # Get the current node state
                        self.sim.tileMatrix = self.tree.state
                        for i in range(len(MOVES)):
                                # Make a copy of the board before simulating moves
                                matrixCopy = copy.deepcopy(self.sim.tileMatrix)
                                self.sim.move(i)
                                # Add the node as a child if the board changes whatsoever
                                if matrixCopy != self.sim.tileMatrix:
                                        # Records the move as well (i)
                                        temp = Node(self.sim.tileMatrix, 'chance', i)
                                        self.tree.add(copy.deepcopy(temp))
                                self.sim.undo()
                # Expand the CHANCE player nodes
                for i in self.tree.children:
                        # Make a copy of the board before simulating random tile placements
                        self.sim.tileMatrix = i.state
                        for x in range(self.sim.board_size):
                                for y in range(self.sim.board_size):
                                        # Add all possible random tile placements as child nodes
                                        if self.sim.tileMatrix[x][y] == 0:
                                                self.sim.tileMatrix[x][y] = 2
                                                temp = Node(self.sim.tileMatrix, 'max')
                                                i.add(copy.deepcopy(temp))
                                                self.sim.tileMatrix[x][y] = 0
                # Expand the MAX player nodes for CHANCE player nodes
                for i in self.tree.children:
                        for k in i.children:
                                # Make a copy of the board before simulating moves
                                self.sim.tileMatrix = k.state
                                matrixCopy = copy.deepcopy(self.sim.tileMatrix)
                                for x in range(len(MOVES)):
                                        self.sim.move(x)
                                        # Add the node as a child if the board changes whatsoever
                                        if matrixCopy != self.sim.tileMatrix:
                                                # Records the move as well (x)
                                                temp = Node(self.sim.tileMatrix, 'chance', x)
                                                k.add(copy.deepcopy(temp))
                                        self.sim.undo()
        # Returns a payoff penalty based on board smoothness
        def smoothness(self, node, x, y):
                smoothnessPenalty = 0
                # Check for the smoothness between the current node and all of its neighboring nodes
                if x < (self.sim.board_size - 1):
                        smoothnessPenalty += abs(node.state[x][y] - node.state[x+1][y])
                if x > 0:
                        smoothnessPenalty += abs(node.state[x][y] - node.state[x-1][y])
                if y < (self.sim.board_size - 1):
                        smoothnessPenalty += abs(node.state[x][y] - node.state[x][y+1])
                if y > 0:
                        smoothnessPenalty += abs(node.state[x][y] - node.state[x][y-1])
                return smoothnessPenalty
        # Calculates the payoff of moves from bottom-up in the game tree
        def expectimax(self, node):
                # Check for terminal (leaf) nodes
                if len(node.children) == 0:
                        # Calculate payoff
                        weightedScore, occupiedTiles, smoothnessPenalty = 0, 0, 0
                        for x in range(self.sim.board_size):
                                for y in range(self.sim.board_size):
                                        # Count the number of non-free tiles
                                        if node.state[x][y] != 0:
                                                occupiedTiles += 1
                                        # Increase payoff based on having bigger valued tiles
                                        # near the top left corner
                                        weightedScore += node.state[x][y]*WEIGHTS[x][y]
                                        # Calculate smoothness of the board
                                        smoothnessPenalty += self.smoothness(node, x, y)
                        # Calculate the payoff based on the number of free tiles, weights,
                        # and smoothness. Smoothness is deducted as a penalty value, while
                        # an overabundance of occupied tiles splits payoff in half
                        if occupiedTiles > 10:
                                return (weightedScore - smoothnessPenalty)/2
                        else:
                                return (weightedScore - smoothnessPenalty)
                # Calculate payoff for MAX player nodes
                elif node.type == 'max':
                        value = -1
                        # Get the highest payoff from the CHANCE child nodes
                        for n in node.children:
                                value = max(value, self.expectimax(n))
                        return value
                # Calculate payoff for CHANCE player nodes
                elif node.type == 'chance':
                        value, smoothnessPenalty = 0, 0
                        for n in node.children:
                                # Check if there's any children nodes
                                if (len(n.children) == 0):
                                        return value
                                else:
                                        # Calculate the selection chance based on board smoothness
                                        for x in range(self.sim.board_size):
                                                for y in range(self.sim.board_size):
                                                        smoothnessPenalty += self.smoothness(n, x, y)
                                        # Added weight to the smoothness penalty
                                        smoothnessPenalty *= 5
                                        # Safety prevention of division by '0'
                                        if smoothnessPenalty == 0:
                                                smoothnessPenalty = 1
                                        # Return the payoff of the node
                                        value = value + self.expectimax(n)*(1/smoothnessPenalty)
                        return value
                else:
                        return
        # Function to return best decision to game
        def compute_decision(self):
                possibleMoves = []
                # Grow to a depth '3' tree
                self.growTree(self.depth)
                # Grow to a depth '5' tree if specified
                if (self.depth == 5):
                        self.growTree()
                # Get the payoff of all rational moves from the root state
                for n in range(len(self.tree.children)):
                        payoff = self.expectimax(self.tree.children[n])
                        possibleMoves.append(copy.deepcopy(payoff))
                # Get the maximum payoff, and return the move associated with said payoff
                maximumPayoff = possibleMoves.index(max(possibleMoves))
                optimalMove = self.tree.children[maximumPayoff].move
                return optimalMove

# Generates nodes for tree      
class Node:
        def __init__(self, gameState, maxOrChance, move = None):
                self.state = gameState          # Node's game state (tile matrix)
                self.type = maxOrChance
                self.move = move
                self.children = []
        # Adds children to node
        def add(self, child):
                self.children.append(child)
                
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
