import pacman
import util

def DepthFirstSearch(problem):
    # emtpy container for visited nodes 
    visited_nodes = []
    # empty dictionary for transitions
    transitions = {}
    # stack
    s = Stack()
    s.push(problem.getStartState())
    while not s.isEmpty(): 
        current_node = s.pop()
        if problem.isGoalState(current_node):
            return find_path(current_node, transitions)
            visited_nodes.append(current_node)

        for i in problem.getSuccessors(current_node):
            if not i in visited_nodes:
                s.push(i)
                transitions.update({current_node:i})

    def find_path(goal, transition):
        backwards_path = []
        current_node = goal

        while current_node in transitions:
            backwards_path.append(current_node)
            current_node = transitions[current_node]

        forwards_path = backwards_path.reverse
        return forwards_path



def BreadthFirtsSearch(problem):
    # emtpy container for visited nodes 
    visited_nodes = []
    # empty dictionary for transitions
    transitions = {}
    # queue
    q = Queue()
    q.enqueue(problem.getStartState())
    while not q.isEmpty():
        current_node = q.dequeue()
        if problem.isGoalState(current_node):
            return find_path(current_node, transitions)
            visited_nodes.append(current_node)
        
        for i in problem.getSuccessors(current_node):
            if not i in visited_nodes:
                q.enqueue(i)
                transitions.update({current_node:i})

    def find_path(goal, transition):

        backwards_path = []
        current_node = goal

        while current_node in transitions:
            backwards_path.append(current_node)
            current_node = transitions[current_node]

        forwards_path = backwards_path.reverse
        return forwards_path


def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    # emtpy container for visited nodes 
    visited_nodes = []
    # empty dictionary for transitions
    transitions = {}
    # priority queue
    pq = PriorityQueue()
    pq.push(problem.getStartState())
    while not pq.isEmpty():
        current_node = pq.pop()
        if problem.isGoalState(current_node):
            return find_path(current_node, transitions)
            visited_nodes.append(current_node)
        
        for i in problem.getSuccessors(current_node):
            if not i in visited_nodes:
                pq.push(i)
                transitions.update({current_node:i})

    def find_path(goal, transition):

        backwards_path = []
        current_node = goal

        while current_node in transitions:
            backwards_path.append(current_node)
            current_node = transitions[current_node]

        forwards_path = backwards_path.reverse
        return forwards_path
