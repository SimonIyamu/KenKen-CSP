import csp
import itertools
import time
from math import sqrt
from collections import defaultdict

# 3x3
puzzle1 = ( "0 1 1 " +
            "0 2 3 "+
            "4 2 3","3 1 1 3 3","+ - - / =") 

# 6x6 (from the project's instructions)
puzzle2 = ( "0 1 1 2 3 3 "+
            "0 4 4 2 5 3 "+
            "6 6 7 7 5 3 "+
            "6 6 8 9 10 10 "+
            "11 11 8 9 9 12 "+
            "13 13 13 14 14 12",
            "11 2 20 6 3 3 240 6 6 7 30 6 9 8 2",
            "+ / * * - / * * * + * * + + /")


# 8x8 
puzzle3 = ( "0 1 1 2 2 3 4 4 " +
            "0 0 5 6 6 3 7 4 " +
            "8 9 5 10 6 11 7 12 "+
            "8 9 13 10 14 11 15 12 "+
            "16 16 13 17 14 18 15 19 "+
            "20 21 21 17 22 18 23 19 "+
            "20 24 24 25 22 26 23 27 "+
            "28 28 28 25 25 26 27 27 ",
            "96 4 3 9 24 4 13 1 12 5 5 9 3 4 3 21 20 2 8 9 21 11 3 2 3 17 2 80 16",
            "* - - + * / + - * - - + / / / * * - * + * + / / - + / * +")

# 9x9
puzzle5 = ( "0 1 2 3 4 4 5 6 6 " + 
            "0 1 2 3 7 8 5 9 10 " + 
            "11 11 12 12 7 8 13 9 10 " + 
            "14 15 16 16 17 17 13 9 18 " + 
            "14 15 19 20 20 21 22 22 18 " + 
            "23 19 19 24 24 21 25 22 26 " + 
            "23 23 27 27 24 28 25 29 26 " + 
            "30 31 31 32 32 28 29 29 29 " + 
            "30 33 33 34 34 35 35 36 36",
            "2 1 3 56 4 11 2 2 72 17 3 7 24 2 14 12 11 9 54 90 11 3 320 15 16 5 9 7 3 45 4 2 13 2 1 3 1",
            "/ - / * - + / - * + / - * / + * + + * * + / * + * - + * / * - - + / - - -")

cageGoal = {}
blocks = defaultdict(list)

def kenken_constraint(A, a, B, b):
    val = {}
    for i,(x,y) in enumerate(blocks[A]):
        val[(x,y)] = a[i]

    for i,(x,y) in enumerate(blocks[B]):
        val[(x,y)] = b[i]

    for (x1,y1) in blocks[A]:
        for(x2,y2) in blocks[B]:
            if val[(x1,y1)] == val[(x2,y2)] and (x1==x2 or y1==y2):
                return False
    return True

def operationSatisfyingValues(A,l):
    """
    A is a variable and l is a list of the values it can take
    """
    operation = (cageGoal[A])[1]
    goalValue = (cageGoal[A])[0]
    
    satValues = [];
    for a in l:
        if operation == '+':
            if sum(a) == goalValue:
                satValues.append(a)
            continue
        if operation == '-':
            if a[0] - a[1] == goalValue or a[1] - a[0] == goalValue:
                satValues.append(a)
            continue
        if operation == '*':
            product = 1;
            for x in a:
                product *=x
            if product == goalValue:
                satValues.append(a)
            continue
        if operation == '/':
            if (a[0] != 0 and a[1]!=0):
                if ( a[0] / a[1] == goalValue or a[1] / a[0] == goalValue):
                    satValues.append(a)
            continue
        if operation == '=':
            if a[0] == goalValue:
                satValues.append(a)

    return satValues

class KenKen(csp.CSP):
    """
    The KenKen Problem.
    Example execution:
    >>> s=KenKen(puzzle2)
    >>> a = csp.backtracking_search(s, select_unassigned_variable=csp.mrv, inference=csp.forward_checking)
    >>> s.display(a)
    5 6 3 4 1 2 
    6 1 4 5 2 3 
    4 5 2 3 6 1 
    3 4 1 2 5 6 
    2 3 6 1 4 5 
    1 2 5 6 3 4 
    """

    def __init__(self,grid):
        """
            A tuple of three strings is passed as argument.
            The first string of the tupple, indicates the cage of each cell.
            The second and the third string show the goal number and the operation of each cage respectively.
        """
        cageSequence = grid[0].split()
        self.numOfCages = numOfCages = len(grid[1].split())
        n = int(sqrt(len(cageSequence)))
        print(n,numOfCages,len(grid[2].split()))

        self.n = n
        self.cage = {} # e.x. cage[(0,1)] = 1

        # self.cage is a dictionary that maps the position of a block to a cage
        # blocks is the reverse
        for i,cageIndex in enumerate(grid[0].split()):
            self.cage[(i//n,i%n)] = int(cageIndex)
            blocks[int(cageIndex)].append( (i//n,i%n) )
        #self.printCages();


        # cageGoal is a dictionary that maps a cage with an operation and goal value
        for i in range(numOfCages):
            cageGoal[i] = ( int(grid[1].split()[i]),grid[2].split()[i])

        # Count how many blocks each cage has.
        numOfBlocks = {}
        for i in range(numOfCages):
            numOfBlocks[i] = len(blocks[i]);

        # Find the domain of each variable (cage).
        domain = {}
        x = [ n for n in range(1,n+1)] # Block's value can be 1,2,...,n
        for i in range(numOfCages):
            permutationsWithRepetition = [p for p in itertools.product(x, repeat=numOfBlocks[i])] 
            domain[i] = operationSatisfyingValues(i,permutationsWithRepetition)
            #print(i,":",domain[i])
        
        # Finding the neighbours of each cage
        neighbours = defaultdict(list)
        for cageIndex in range(numOfCages):
            for (x,y) in blocks[cageIndex]:
                for i in range(n):
                    if self.cage[(i,y)] != cageIndex and self.cage[(i,y)] not in neighbours[cageIndex]:
                        neighbours[cageIndex].append(self.cage[(i,y)])
                    if self.cage[(x,i)] != cageIndex and self.cage[(x,i)] not in neighbours[cageIndex]:
                        neighbours[cageIndex].append(self.cage[(x,i)])


        csp.CSP.__init__(self,range(numOfCages), domain, neighbours, kenken_constraint)
    
    def display(self, assignment):
        """
        Print assignment in a readable way
        """
        if assignment is None:
            return

        # blockAssignment is a dictionary that maps a position to its value according to the assignment
        blockAssignment = {}
        for cage in range(self.numOfCages):
            for i,(x,y) in enumerate(blocks[cage]):
                blockAssignment[(x,y)] = assignment[cage][i]
        for x in range(self.n):
            for y in range(self.n):
                print(blockAssignment[(x,y)],end=' ')
            print()
 
    def printCages(self):
        """
        Prints the cage index of each block in the grid
        """
        for i in range(self.n):
            for j in range(self.n):
                print (self.cage[(i,j)],end=' ')
            print ()

"""
s=KenKen(puzzle2)
start_time = time.time()
a = csp.backtracking_search(s, select_unassigned_variable=csp.mrv, inference=csp.forward_checking)
end_time = time.time()
s.display(a)
print("CPU time : ",end_time-start_time)
print("Assignments :", s.nassigns)
"""
