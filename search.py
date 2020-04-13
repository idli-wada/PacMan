# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).
    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state
        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state
        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take
        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()

def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.
    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.
    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:
    """

    from util import Stack

    # stackXY: ((x,y),[path]) #
    stackXY = Stack()

    visited = [] # Visited states
    path = [] # Every state keeps it's path from the starting state

    
    if problem.isGoalState(problem.getStartState()):
        return []

    # Start from the beginning and find a solution, path is an empty list #
    stackXY.push((problem.getStartState(),[]))

    while(True):
        if stackXY.isEmpty():
            return []

        
        xy,path = stackXY.pop() # Take position and path
        visited.append(xy)
       
        if problem.isGoalState(xy):
            print path
            return path

        # Get successors of current state #
        successor = problem.getSuccessors(xy)

        # Add new states in stack and with newpath
        if successor:
            for item in successor:
                if item[0] not in visited:
                    newPath = path + [item[1]] # Calculate new path
                    stackXY.push((item[0],newPath))
                    # print item[1]

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"

    from util import Queue

    
    queueXY = Queue()

    visited = []
    path = [] 
    
    if problem.isGoalState(problem.getStartState()):
        return []

    
    queueXY.push((problem.getStartState(),[]))

    while(True):
        if queueXY.isEmpty():
            return []
        xy,path = queueXY.pop()
        visited.append(xy)

        if problem.isGoalState(xy):
            return path
        successor = problem.getSuccessors(xy)
        if successor:
            for item in successor:
                if item[0] not in visited and item[0] not in (state[0] for state in queueXY.list):

                    
                    # if problem.isGoalState(item[0]):
                    #   return path + [item[1]]

                    newPath = path + [item[1]] 
                    queueXY.push((item[0],newPath))

def uniformCostSearch(
    problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"

    from util import PriorityQueue

    # queueXY: ((x,y),[path],priority) 
    queueXY = PriorityQueue()

    visited = [] 
    path = [] 

    
    if problem.isGoalState(problem.getStartState()):
        return []
                                     
    queueXY.push((problem.getStartState(),[]),0)

    while(True):
        if queueXY.isEmpty():
            return []
        xy,path = queueXY.pop() 
        visited.append(xy)
        if problem.isGoalState(xy):
            return path
        
        succ = problem.getSuccessors(xy)
        if succ:
            for item in succ:
                if item[0] not in visited and (item[0] not in (state[2][0] for state in queueXY.heap)):
                    # queueXY.heap is a list where pushed elements are stored
                    # state = single element in priority queue
                    # format of state is (priority, count, ((vertex),path)))

                    newPath = path + [item[1]]
                    pri = problem.getCostOfActions(newPath)

                    queueXY.push((item[0],newPath),pri)
                    # for state in queueXY.heap:
                    #     print "STATE is ", state
                    # return []

                # State is in queue. Check if current path is cheaper from the previous one 
                elif item[0] not in visited and (item[0] in (state[2][0] for state in queueXY.heap)):
                    for state in queueXY.heap:
                        if state[2][0] == item[0]:
                            oldPri = problem.getCostOfActions(state[2][1])

                    newPri = problem.getCostOfActions(path + [item[1]])

                    # State is cheaper with his hew father 
                    if oldPri > newPri:
                        newPath = path + [item[1]]
                        queueXY.update((item[0],newPath),newPri)
                        
    

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

from util import PriorityQueue
class MyPriorityQueueWithFunction(PriorityQueue):
    
    # Implements a priority queue with the same push/pop signature of the
    # Queue and the Stack classes. This is designed for drop-in replacement for
    # those two classes. The caller has to provide a priority function, which
    # extracts each item's priority.
    
    def  __init__(self, problem, priorityFunction):
        "priorityFunction (item) -> priority"
        self.priorityFunction = priorityFunction
        PriorityQueue.__init__(self)       
        self.problem = problem
    def push(self, item, heuristic):
        "Adds an item to the queue with priority from the priority function"
        PriorityQueue.push(self, item, self.priorityFunction(self.problem,item,heuristic))

# Calculate f(n) = g(n) + h(n) 
def f(problem,state,heuristic):

    return problem.getCostOfActions(state[1]) + heuristic(state[0],problem)

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"

    # queueXY: ((x,y),[path]) #
    queueXY = MyPriorityQueueWithFunction(problem,f)
    path = [] 
    visited = []     
    if problem.isGoalState(problem.getStartState()):
        return []

    element = (problem.getStartState(),[])

    queueXY.push(element,heuristic)

    while(True):
        if queueXY.isEmpty():
            return []

        xy,path = queueXY.pop()
        if xy in visited:
            continue

        visited.append(xy)

        
        if problem.isGoalState(xy):
            return path
        succ = problem.getSuccessors(xy)
        if succ:
            for item in succ:
                if item[0] not in visited:
                    newPath = path + [item[1]] 
                    element = (item[0],newPath)
                    queueXY.push(element,heuristic)
        
# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch

        
        

        
        

        
       

    
    
        
        
        

        
        

        
        

        
        

        

        

        

        
        

        

        
        
                    
                     

                    

   


    
        
        
        
                
                    



