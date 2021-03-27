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
    # make a dictionary for transitions
    transitions = {}
    # make a dictionary for costs
    costs = {}
    visited_nodes = []
    # make a priority queue
    pq = util.PriorityQueue()
    full_cost = 0
    # add the starting state to the PQ with cost 0
    pq.push(problem.getStartState())
    # while PQ is not empty:
    while not pq.isEmpty():
	    # pop curr_node off of state
        current_node = pq.pop()
	    # if curr_node is the goal:
        if problem.isGoalState(current_node):
		    # backtrack through the transitions dictionary and return
            return find_path(current_node, transitions)
	    # for next_node, direction, cost in successors of curr_node:
        for i, direction, cost in problem.getSuccessors(current_node):
		    # full cost of next node = full cost of curr node + cost
            full_cost = full_cost[current_node] + cost
		    # if next_node in transitions: 
            if i in transitions:
			    # if stored cost to next node > full cost of next node:
                if full_cost[i] > full_cost:
				    # update transitions dictionary
                    transitions[i] = full_cost[i] = full_cost
				    # update full cost dictionary
			    # continue
            
		    # else:
            else:
			    # add next_node to cost dictionary
                full_cost.update({i})
			    # add next_node to transitions dictionary
                transitions[i] = (current_node, direction)
			    # add next_node to PQ
                pq.push(i)