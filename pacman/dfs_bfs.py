import pacman
import util

def find_path(goal, transitions):
    backwards_path = []
    current_node = goal

    while current_node in transitions and transitions[current_node]:
        backwards_path.append(transitions[current_node][1])
        current_node = transitions[current_node][0]

    backwards_path.reverse()
    return list(backwards_path)

def DepthFirstSearch(problem):
    visited_nodes = []
    transitions = {}
    s = util.Stack()
    s.push(problem.getStartState())
    while not s.isEmpty(): 
        current_node = s.pop()
        visited_nodes.append(current_node)
        if problem.isGoalState(current_node):
            path = find_path(current_node, transitions)
            return find_path(current_node, transitions)
            

        for i, direction, cost in problem.getSuccessors(current_node):
            if not i in visited_nodes:
                s.push(i)
                transitions[i] = (current_node, direction)





def BreadthFirtsSearch(problem):
    visited_nodes = []
    transitions = {}
    q = util.Queue()
    q.push(problem.getStartState())
    while not q.isEmpty(): 
        current_node = q.pop()
        visited_nodes.append(current_node)
        if problem.isGoalState(current_node):
            path = find_path(current_node, transitions)
            return find_path(current_node, transitions)
            

        for i, direction, cost in problem.getSuccessors(current_node):
            if not i in visited_nodes:
                q.push(i)
                transitions[i] = (current_node, direction)

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    visited_nodes = []
    transitions = {}
    costs = {}
    pq = PriorityQueue()
    pq.push(problem.getStartState(cost = 0))
    while not pq.isEmpty():
        current_node = pq.pop()
        visited_nodes.append(current_node)
        if problem.isGoalState(current_node):
            return find_path(current_node, transitions)
            
        
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



'''
uniformCostSearch pseudocode
make a dictionary for transitions
make a dictionary for costs
make a priority queue
add the starting state to the PQ with cost 0
while PQ is not empty:
	pop curr_node off of state
	if curr_node is the goal:
		backtrack through the transitions dictionary and return
	for next_node, direction, cost in successors of curr_node:
		full cost of next node = full cost of curr node + cost
		if next_node in transitions: 
			if stored cost to next node > full cost of next node:
				update transitions dictionary
				update full cost dictionary
			continue
		else:
			add next_node to cost dictionary
			add next_node to transitions dictionary
			add next_node to PQ
'''