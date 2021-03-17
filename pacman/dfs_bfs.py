import pacman

def DepthFirstSearch(problem):
    # emtpy container for visited nodes 
    visited_nodes = []
    # empty dictionary for transitions
    transitions = {}
    # stack
    stack = Stack
    stack.push(problem.getStartState())
    while not stack.isEmpty(): 
        current_node = stack.pop()
        if problem.isGoalState(current_node):
            return path(current_node, transitions)
            visited_nodes.append(current_node)

        for i in problem.getSuccessors(current_node):
            if not i in visited_nodes:
                stack.push(i)
                transitions.update({current_node:i})


    backwards_path = []
    current_node = goal

    while current in dictionary:
        backwards_path.append(current_node)
        current_node = dictionary.pop()

    forwards_path = backwards_path.reverse
    return forwards_path



def BreadthFirtsSearch(problem):
    # emtpy container for visited nodes 
    visited_nodes = []
    # empty dictionary for transitions
    transitions = {}
    # queue
    queue = Queue
    queue.enqueue(problem.getStartState())
    while not queue.isEmpty():
        current_node = queue.dequeue()
        if problem.isGoalState(current_node):
            return path(current_node, transitions)
            visited_nodes.append(current_node)
        
        for i in problem.getSuccessors(current_node):
            if not i in visited:
                queue.enqueue(i)
                transitions.update({current_node:i})


    backwards_path = []
    current_node = goal

    while current_node in dictionary:
        backwards_path.append(current_node)
        current = dictionary.pop()

    forwards_path = backwards_path.reverse
    return forwards_path