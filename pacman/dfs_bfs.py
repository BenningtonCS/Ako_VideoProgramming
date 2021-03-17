class Stack:
     def __init__(self):
         self.items = []

     def isEmpty(self):
         return self.items == []

     def push(self, item):
         self.items.append(item)

     def pop(self):
         return self.items.pop()

     def peek(self):
         return self.items[len(self.items)-1]

     def size(self):
         return len(self.items)

stack = Stack
visited_nodes1 = []
dictionary1 = dict()
tree1 = {"A": ["D", "C", "B"], "B": ["E"], "C": ["F"], "D": ["G"], "E": ["H"]}

def DepthFirstSearch(goal, stack):
    stack.push(tree1[0])
    while stack is not 0:
        stack = stack.pop()
        if goal is stack:
            break
        else: 
            visited_nodes1.append

        for i in tree1:
            if i is not visited_nodes1:
                stack.push(tree1[i])
                dictionary1.append({i}:{i + 1})
    backwards_path = []
    current = goal

    while current is in dictionary1:
        backwards_path.append(current)
        current = dictionary1.pop()

    forwards_path = backwards_path.reverse
    return forwards_path


class Queue:
    def __init__(self):
        self.items = []

    def isEmpty(self):
        return self.items == []

    def enqueue(self, item):
        self.items.insert(0,item)

    def dequeue(self):
        return self.items.pop()

    def size(self):
        return len(self.items)


queue = Queue
visited_nodes2 = []
dictionary2 = dict()
tree2 = {"A": ["D", "C", "B"], "B": ["E"], "C": ["F"], "D": ["G"], "E": ["H"]}

def BreadthFirtsSearch(goal, queue):
    queue.push(tree2[0])
    while queue is not 0:
        queue = queue.dequeue()
        if goal is queue:
            break
        else: 
            visited_nodes2.append
        
        for i in tree2:
            if i is not visited_nodes2:
                queue.enqueue(tree2[i])
                dictionary2.append({i}:{i + 1})
    backwards_path = []
    current = goal

    while current is in dictionary2:
        backwards_path.append(current)
        current = dictionary2.pop()

    forwards_path = backwards_path.reverse
    return forwards_path