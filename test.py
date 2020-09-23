from collections import deque
import time
import heapq as hq

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
    while node in node_dict:
        if (node == start):
            line = [node[0], node[1], node[2], 0]

            path.append(line)
            return path, cost
        else:
            line = [node[0], node[1], node[2], 1]

            parent = node_dict[node]
            path.append(line)
            node = parent
            cost += 1

    return path, cost


# BFS
# unit path cost = 1
def bfs(start, end):
    queue = deque()
    node_dict = {start: start}
    path = []
    v_set = set()  # visited set

    queue.append(start)

    while len(queue) > 0:
        node = queue.popleft()
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
                child = adj_list[i]
                if (child not in v_set):
                    # v_set.add(child)
                    queue.append(child)
                    node_dict[child] = node

    output.write("FAIL")



def adj_cost_cal(point):
    adj_list = []
    # have limit action
    if point in actions:
        act_dir = actions[point]
        for i in range(len(act_dir)):
            code_num = act_dir[i]
            move = decode_dict[code_num]
            adj_node = tuple_add(point, move)

            if (code_num <= 6):
                adj_cost = 10
            else:
                adj_cost = 14
            adj_list.append((adj_cost, adj_node))

    return adj_list


# UCS
# straight = 10 , diagnal = 14
def ucs(start, end):
    open = [(0, start, 0, [(start, 0)])]  # heap (total cost, loc, real cost, path)
    close = {}  # close node:cost

    while len(open) > 0:
        cost, node, real_cost, path = hq.heappop(open)
        close[node] = cost

        if node == end:
            output.write(str(cost) + '\n')
            output.write(str(len(path)) + '\n')
            print(path)
            for i in range(len(path)):
                output.write(' '.join([str(elem) for elem in path[i][0]]))
                output.write(" ")
                output.write(str(path[i][1]))
                output.write('\n')
            output.truncate(output.tell() - 1)
            return path

        else:
            adj_cost_list = adj_cost_cal(node)
            for i in range(len(adj_cost_list)):
                adj_cost, adj_node = adj_cost_list[i][0], adj_cost_list[i][1]
                if adj_node not in close:
                    hq.heappush(open, ((cost + adj_cost), adj_node, adj_cost, path + [(adj_node, adj_cost)]))

    output.write("FAIL")



def future_cost(node, end):
    return 0


# A*
def a_star(start, end):
    open = [(0, start, 0, [(start, 0)])]  # heap (total cost, loc, real cost, path)
    close = {}  # close node:cost

    while len(open) > 0:
        cost, node, real_cost, path = hq.heappop(open)
        close[node] = cost

        if node == end:
            output.write(str(cost) + '\n')
            output.write(str(len(path)) + '\n')
            for i in range(len(path)):
                output.write(' '.join([str(elem) for elem in path[i][0]]))
                output.write(" ")
                output.write(str(path[i][1]))
                output.write('\n')
            output.truncate(output.tell() - 1)
            return path

        else:
            adj_cost_list = adj_cost_cal(node)
            for i in range(len(adj_cost_list)):
                adj_cost, adj_node = adj_cost_list[i][0], adj_cost_list[i][1]
                if adj_node not in close:
                    final_cost = cost + adj_cost + future_cost(adj_node, end)
                    hq.heappush(open, (final_cost, adj_node, adj_cost, path + [(adj_node, adj_cost)]))

    output.write("FAIL")


# read file
input = open("sample/input6.txt", 'r')
lines = input.readlines()

# line 1 : name of algorithm
algorithm = lines[0].rstrip('\n')

# line 2 : 3 dimension
dimensions = list(map(int, lines[1].rstrip('\n').split(' ')))

# line 3 : entrance grid location
start = tuple(map(int, lines[2].rstrip('\n').split(' ')))

# line 4 : exit grid location
end = tuple(map(int, lines[3].rstrip('\n').split(' ')))

# line 5 : num of grids in the maze where there are action available
num = list(map(int, lines[4].rstrip('\n').split(' ')))[0]

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
output = open("sample/test/output_6.txt", "w")

start_time = time.time()
if (algorithm == "BFS"):
    bfs(start, end)
elif (algorithm == "UCS"):
    ucs(start, end)
else:
    a_star(start, end)

end_time = time.time()

print("-------%s seconds ---------" % (end_time - start_time))

output.close()

