from collections import deque
import time

# Act Code
# x+:1 x-:2 y+:3 y-:4 z+:5 z-:6
# x+y+:7 x+y-:8 x-y+:9 x-y-:10
# x+z+:11 x+z-:12 x-z+:13 x-z-:14
# y+z+:15 y+z-:16 y-z+:17 y-z-:18

decode_dict = {1: (1, 0, 0), 2: (-1, 0, 0),
               3: (0, 1, 0), 4: (0, -1, 0),
               5: (0, 0, 1), 6: (0, 0, -1),
               7: (1, 1, 0), 8: (1, -1, 0), 9: (-1, 1, 0), 10: (-1, -1, 0),
               11: (1, 0, 1), 12: (1, 0, -1), 13: (-1, 0, 1), 14: (-1, 0, -1),
               15: (0, 1, 1), 16: (0, 1, -1), 17: (0, -1, 1), 18: (0, -1, -1)
               }


def tuple_add(point, move):
    x = point[0] + move[0]
    y = point[1] + move[1]
    z = point[2] + move[2]
    adj_node = (x, y, z)

    return adj_node


def get_neighbor(point):
    adj_list = []
    # have limit action
    if point in actions:
        act_dir = actions[point]
        for i in range(len(act_dir)):
            move = decode_dict[act_dir[i]]
            adj_node = tuple_add(point, move)
            adj_list.append(adj_node)
    return adj_list

# (node,parent) dict
# given node to find his parent
def backtrace(node, node_dict, path, cost):


    while (node != start):
        if (node in node_dict):
            line = [node[0], node[1], node[2], 1]
            path.append(line)
            parent = node_dict[node]
            node = parent
            cost += 1
        else:
            return "FAIL"
    line = [node[0], node[1], node[2], 0]
    path.append(line)
    return path, cost



# BFS
# unit path cost = 1
def bfs(dim, start, end, actions):
    queue = deque()
    node_dict = {start: start}
    path = []
    v_set = set()  # visited set

    queue.append(start)

    while len(queue) > 0:
        node = queue.pop()
        v_set.add(node)

        if (node == end):
            bt = backtrace(node, node_dict, path, 0)
            path = bt[0]
            path.reverse()
            cost = str(bt[1])
            output.write(cost + '\n')
            output.write(str(len(path)) + '\n')
            for i in range(len(path)):
                output.write(' '.join([str(elem) for elem in path[i]]))
                output.write('\n')
            output.truncate(output.tell() - 1)
            return "SUCCESS"
        else:
            adj_list = get_neighbor(node)
            for i in range(len(adj_list)):
                if (adj_list[i] not in v_set) and (adj_list[i] not in queue) and (adj_list[i][0] < dimensions[0]) and (adj_list[i][1] < dimensions[1]) and (adj_list[i][2] < dimensions[2]):
                    queue.append(adj_list[i])
                    node_dict[adj_list[i]] = node

    output.write("FAIL")
    return "FAIL"


# UCS
# straight = 10 , diagnal = 14
def ucs(dim, start, end, actions):
    return "UCS"


# A*

def a_star(dim, start, end, actions):
    return "A*"


# read file
input = open("sample/input5.txt", 'r')
lines = input.readlines()
# print("lines: ", lines)

# line 1 : name of algorithm
algorithm = lines[0].rstrip('\n')
print("algorithm : ", algorithm)

# line 2 : 3 dimension
dimensions = list(map(int, lines[1].rstrip('\n').split(' ')))
print("dimensions: ", dimensions)

# line 3 : entrance grid location
start = tuple(map(int, lines[2].rstrip('\n').split(' ')))
# print("entrance: ", start)

# line 4 : exit grid location
end = tuple(map(int, lines[3].rstrip('\n').split(' ')))
# print("exit: ", end)

# line 5 : num of grids in the maze where there are action available
num = list(map(int, lines[4].rstrip('\n').split(' ')))[0]
# print("num: ", num)

actions = {}
# line N : location of grid, list of available actions
for i in range(5, len(lines)):
    # loc:actions
    act_list = list(map(int, lines[i].rstrip('\n').split(' ')))
    loc = (act_list[0], act_list[1], act_list[2])
    acts = act_list[3:]
    actions[loc] = acts
input.close()

# write to output
output = open("sample/test/output_test.txt", "w")
print("file name: ", output.name)

# print(actions)


start_time = time.time()
if (algorithm == "BFS"):
    bfs(dimensions, start, end, actions)
elif (algorithm == "UCS"):
    ucs(dimensions, start, end, actions)
else:
    a_star(dimensions, start, end, actions)

end_time = time.time()

print("-------%s seconds ---------" % (end_time - start_time))

output.close()
