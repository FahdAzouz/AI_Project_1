# eightpuzzle.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Azbbeel (pabbeel@cs.berkeley.edu).


import search
import random
import math

# Module Classes

class EightPuzzleState:
    """
    The Eight Puzzle is described in the course textbook on
    page 64.

    This class defines the mechanics of the puzzle itself.  The
    task of recasting this puzzle as a search problem is left to
    the EightPuzzleSearchProblem class.
    """

    def __init__( self, numbers ):
        """
          Constructs a new eight puzzle from an ordering of numbers.

        numbers: a list of integers from 0 to 8 representing an
          instance of the eight puzzle.  0 represents the blank
          space.  Thus, the list

            [1, 0, 2, 3, 4, 5, 6, 7, 8]

          represents the eight puzzle:
            -------------
            | 1 |   | 2 |
            -------------
            | 3 | 4 | 5 |
            -------------
            | 6 | 7 | 8 |
            ------------

        The configuration of the puzzle is stored in a 2-dimensional
        list (a list of lists) 'cells'.
        """
        self.cells = []
        numbers = numbers[:] # Make a copy so as not to cause side-effects.
        numbers.reverse()
        for row in range(3):
            self.cells.append([])
            for col in range(3):
                if numbers:
                    self.cells[row].append(numbers.pop())
                else:
                    raise ValueError("Invalid initial state: not enough numbers.")

                if self.cells[row][col] == 0:
                    self.blankLocation = row, col

    def isGoal( self ):
        """
          Checks to see if the puzzle is in its goal state.

            -------------
            |   | 1 | 2 |
            -------------
            | 3 | 4 | 5 |
            -------------
            | 6 | 7 | 8 |
            -------------

        >>> EightPuzzleState([0, 1, 2, 3, 4, 5, 6, 7, 8]).isGoal()
        True

        >>> EightPuzzleState([1, 0, 2, 3, 4, 5, 6, 7, 8]).isGoal()
        False
        """
        current = 0
        for row in range( 3 ):
            for col in range( 3 ):
                if current != self.cells[row][col]:
                    return False
                current += 1
        return True

    def legalMoves( self ):
        """
          Returns a list of legal moves from the current state.

        Moves consist of moving the blank space up, down, left or right.
        These are encoded as 'up', 'down', 'left' and 'right' respectively.

        >>> EightPuzzleState([0, 1, 2, 3, 4, 5, 6, 7, 8]).legalMoves()
        ['down', 'right']
        """
        moves = []
        row, col = self.blankLocation
        if(row != 0):
            moves.append('up')
        if(row != 2):
            moves.append('down')
        if(col != 0):
            moves.append('left')
        if(col != 2):
            moves.append('right')
        return moves

    def result(self, move):
        """
          Returns a new eightPuzzle with the current state and blankLocation
        updated based on the provided move.

        The move should be a string drawn from a list returned by legalMoves.
        Illegal moves will raise an exception, which may be an array bounds
        exception.

        NOTE: This function *does not* change the current object.  Instead,
        it returns a new object.
        """
        row, col = self.blankLocation
        if(move == 'up'):
            newrow = row - 1
            newcol = col
        elif(move == 'down'):
            newrow = row + 1
            newcol = col
        elif(move == 'left'):
            newrow = row
            newcol = col - 1
        elif(move == 'right'):
            newrow = row
            newcol = col + 1
        else:
            raise "Illegal Move"

        # Create a copy of the current eightPuzzle
        newPuzzle = EightPuzzleState([0, 0, 0, 0, 0, 0, 0, 0, 0])
        newPuzzle.cells = [values[:] for values in self.cells]
        # And update it to reflect the move
        newPuzzle.cells[row][col] = self.cells[newrow][newcol]
        newPuzzle.cells[newrow][newcol] = self.cells[row][col]
        newPuzzle.blankLocation = newrow, newcol

        return newPuzzle

    # Utilities for comparison and display
    def __eq__(self, other):
        """
            Overloads '==' such that two eightPuzzles with the same configuration
          are equal.

          >>> EightPuzzleState([0, 1, 2, 3, 4, 5, 6, 7, 8]) == \
              EightPuzzleState([1, 0, 2, 3, 4, 5, 6, 7, 8]).result('left')
          True
        """
        for row in range( 3 ):
            if self.cells[row] != other.cells[row]:
                return False
        return True

    def __hash__(self):
        return hash(str(self.cells))
    

    def __getAsciiString(self):
        """
          Returns a display string for the maze
        """
        lines = []
        horizontalLine = ('-' * (13))
        lines.append(horizontalLine)
        for row in self.cells:
            rowLine = '|'
            for col in row:
                if col == 0:
                    col = ' '
                rowLine = rowLine + ' ' + col.__str__() + ' |'
            lines.append(rowLine)
            lines.append(horizontalLine)
        return '\n'.join(lines)
    
    def __str__(self):
        return self.__getAsciiString()

# TODO: Implement The methods in this class

class EightPuzzleSearchProblem(search.SearchProblem):
    """
    Implementation of a SearchProblem for the Eight Puzzle domain.
    Each state is represented by an instance of an eightPuzzle.
    """
    def __init__(self, puzzle):
        "Creates a new EightPuzzleSearchProblem which stores search information."
        self.puzzle = puzzle

    def getStartState(self):
        return self.puzzle

    def isGoalState(self, state):
        return state.isGoal()

    def getSuccessors(self, state):
        """
        Returns a list of (successor, action, stepCost) pairs where
        each successor is either left, right, up, or down
        from the original state, and the cost is 1.0 for each.
        """
        succ = []
        for a in state.legalMoves():
            succ.append((state.result(a), a, 1))
        return succ
    """Start Change Task 1 h3"""
    def getCostOfActions(self, actions):
        """
        actions: A list of actions to take.

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        return len(actions)

    def h1_heuristic(self, state, problem):
        # Number of missplaced tiles
        goal_state = [[0, 1, 2], [3, 4, 5], [6, 7, 8]]
        n_missplaced = 0
        for row in range (3) :
            for col in range (3) :
                if state.cells[row][col] != goal_state[row][col]:
                    n_missplaced += 1
        return n_missplaced         

    def h2_heuristic(self, state, problem):
        # Sum of Euclidean distances of the tiles from their goal position
        goal_positions = {0: (0, 0), 1: (0, 1), 2: (0, 2), 3: (1, 0), 4: (1, 1), 5: (1, 2), 6: (2, 0), 7: (2, 1), 8: (2, 2)} #we map each tile value to its goal position
        total_distance = 0
        for i in range(3):
            for j in range(3):
                tile = state.cells[i][j] 
                goal_i, goal_j = goal_positions[tile]
                distance = math.sqrt((i - goal_i)**2 + (j - goal_j)**2)
                total_distance += distance
        return total_distance

    def h3_heuristic(self, state, problem):
        """
        A heuristic function for the eight puzzle problem.
        The heuristic is the sum of the Manhattan distances
        of each tile from its solved position.
        """
        total = 0
        for row in range(3):
            for col in range(3):
                value = state.cells[row][col]
                if value != 0:
                    goal_row, goal_col = divmod(value - 1, 3)
                    total += abs(row - goal_row) + abs(col - goal_col)
        return total

    def h4_heuristic(self, state, problem):
        """
        A heuristic function for the eight puzzle problem.
        The heuristic is the sum of the number of tiles out of row
        and the number of tiles out of column.
        """
        total_out_of_row = 0
        total_out_of_col = 0

        for row in range(3):
            for col in range(3):
                value = state.cells[row][col]
                if value != 0:
                    goal_row, goal_col = divmod(value - 1, 3)
                    total_out_of_row += abs(row - goal_row)
                    total_out_of_col += abs(col - goal_col)

        return total_out_of_row + total_out_of_col

    def aStarSearch(self):
        """
        A* search using the provided heuristic function.
        """
        # Prompt the user to choose an algorithm
        print("Choose an algorithm:")
        print("1. A* Search with Number of missplaced tiles")
        print("2. A* Seaarch with Sum of Euclidean distances of the tiles from their goal position")
        print("3. A* Search with Manhattan Distance Heuristic")
        print("4. A* Seaarch with Number of tiles out of row + Number of tiles out of colum")
        choice = input("Enter the number of your choice: ")
        if choice == "1":
            return search.aStarSearch(self, heuristic=self.h1_heuristic)
        if choice == "2":
            return search.aStarSearch(self, heuristic=self.h2_heuristic)
        if choice == "3":
            return search.aStarSearch(self, heuristic=self.h3_heuristic)
        if choice == "4":
            return search.aStarSearch(self, heuristic=self.h4_heuristic)
        else:
            print("Invalid choice. Please try again.")
            return self.aStarSearch()

    """End Change Task 1 h4"""

def createRandomEightPuzzle(moves=100):
    """
      moves: number of random moves to apply

      Creates a random eight puzzle by applying
      a series of 'moves' random moves to a solved
      puzzle.
    """
    puzzle = EightPuzzleState([0,1,2,3,4,5,6,7,8])
    for i in range(moves):
        # Execute a random legal move
        puzzle = puzzle.result(random.sample(puzzle.legalMoves(), 1)[0])
    return puzzle

if __name__ == '__main__':
    puzzle = createRandomEightPuzzle(25)
    print('A random puzzle:')
    print(puzzle)

    problem = EightPuzzleSearchProblem(puzzle)
    path = problem.aStarSearch()

    print('A* found a path of %d moves: %s' % (len(path), str(path)))
    curr = puzzle
    i = 1
    for a in path:
        curr = curr.result(a)
        print(f'After {i} move{"s" if i > 1 else ""}: {a}')
        print(curr)

        input("Press return for the next state...")  # wait for key stroke
        i += 1
