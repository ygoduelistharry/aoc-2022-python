from aocd.get import get_data
from aocd.post import submit
import _utils as util
import re
import os

day = int(util.get_file_name(__file__))
year = int(os.path.dirname(__file__).split('\\')[-1])
data = get_data(day=day, year=year)
print(data)
clean_data = data.split("\n")


class Node():
    def __init__(self, name, value = None, op = None, left = None, right = None, feeds_left = None, feeds_right = None):
        self.name = name
        self.value = value
        self.op = op
        self.left = left
        self.right = right
        if feeds_left is None:
            self.feeds_left = []
        if feeds_right is None:
            self.feeds_right = []


def process_nodes(data:list[str]) -> dict[str,Node]:
    nodes:dict[str,Node] = {}
    for n in data:
        name = n[0:4]
        value = re.findall(util.re_get_ints, n)
        if value:
            value = int(value[0])
            nodes.update({name:Node(name, value=value)})
        else:
            op = n[11]
            left = n[6:10]
            right = n[13:17]
            nodes.update({name:Node(name, op=op, left=left, right=right)})
    
    for name, node in nodes.items():
        if node.left is not None:
            nodes[node.left].feeds_left.append(name)
        if node.right is not None:
            nodes[node.right].feeds_right.append(name)

    return nodes


def reduce_tree(nodes:dict[str, Node]):
    # reduce the tree starting from childless leaf nodes (i.e. the nodes that start with values)
    # do a breadth first iteration over all the nodes
    # mutates in place
    node_queue = [name for name, node in nodes.items() if node.value is not None]
    index = 0
    while index < len(node_queue):
        # get the current node name
        curr_node_name = node_queue[index]
        # increment the index for next time
        index += 1

        # if we have processed the node already, continue
        if curr_node_name not in nodes:
            continue
        
        # otherwise, set the current node
        curr_node = nodes[curr_node_name]

        # if the node has left and right integer values, we can process it
        if isinstance(curr_node.left, int) and isinstance(curr_node.right, int):
            match curr_node.op:
                case '*':
                    curr_node.value = int(curr_node.left * curr_node.right)
                case '+':
                    curr_node.value = int(curr_node.left + curr_node.right)
                case '-':
                    curr_node.value = int(curr_node.left - curr_node.right)
                case '/':
                    curr_node.value = int(curr_node.left / curr_node.right)
                case _:
                    pass
        
        # if the current node has an integer value, update the nodes it feeds
        # the remove the current node from the tree (it has been reduced!)
        # unless it is the root node! otherwise it the tree will be empty
        if isinstance(curr_node.value, int):

            for n in curr_node.feeds_left:
                nodes[n].left = curr_node.value
                node_queue.append(n)
            
            for n in curr_node.feeds_right:
                nodes[n].right = curr_node.value
                node_queue.append(n)
            
            if curr_node_name != 'root':
                nodes.pop(curr_node_name)
    
    return


def propogate_from_root(nodes:dict[str, Node]):
    # starting the root node, apply the inverse operations to find the missing values
    # mutates in place
    node_queue = [nodes['root']]
    index = 0
    while index < len(node_queue):
        curr_node = node_queue[index]
        index += 1

        if curr_node.left is None and curr_node.right is None:
            break


        if isinstance(curr_node.left, int):
            next_node = nodes[curr_node.right]
            match curr_node.op:
                case '*':
                    next_node.value = int(curr_node.value / curr_node.left)
                case '+':
                    next_node.value = int(curr_node.value - curr_node.left)
                case '-':
                    next_node.value = int(curr_node.left - curr_node.value)
                case '/':
                    next_node.value = int(curr_node.left / curr_node.value)
                case '=':
                    next_node.value = int(curr_node.left)
        

        if isinstance(curr_node.right, int):
            next_node = nodes[curr_node.left]
            match curr_node.op:
                case '*':
                    next_node.value = int(curr_node.value / curr_node.right)
                case '+':
                    next_node.value = int(curr_node.value - curr_node.right)
                case '-':
                    next_node.value = int(curr_node.right + curr_node.value)
                case '/':
                    next_node.value = int(curr_node.right * curr_node.value)
                case '=':
                    next_node.value = int(curr_node.right)
        
        node_queue.append(next_node)

    return


#part 1:
all_nodes1 = process_nodes(clean_data)
reduce_tree(all_nodes1)
ans1 = int(all_nodes1['root'].value)
# submit(ans1,1,day,year)

#part 2:
all_nodes2 = process_nodes(clean_data)
all_nodes2['humn'].value = None
all_nodes2['root'].op = '='
reduce_tree(all_nodes2)
propogate_from_root(all_nodes2)
ans2 = all_nodes2['humn'].value
# submit(ans2,2,day,year)

pass