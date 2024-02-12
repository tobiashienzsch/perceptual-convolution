import collections
import heapq


def shortestPath(edges, source, sink):
    # create a weighted DAG - {node:[(cost,neighbour), ...]}
    graph = collections.defaultdict(list)
    for l, r, c in edges:
        graph[l].append((c, r))
    # create a priority queue and hash set to store visited nodes
    queue, visited = [(0, source, [])], set()
    heapq.heapify(queue)
    # traverse graph with BFS
    while queue:
        (cost, node, path) = heapq.heappop(queue)
        # visit the node if it was not visited before
        if node not in visited:
            visited.add(node)
            path = path + [node]
            # hit the sink
            if node == sink:
                return (cost, path)
            # visit neighbours
            for c, neighbour in graph[node]:
                if neighbour not in visited:
                    heapq.heappush(queue, (cost+c, neighbour, path))
    return float("inf")


def next_step(current, block, max_block):
    if block > max_block:
        return
    print(f"{block}B {current}")

    # 1. Continuation
    if current[2] < current[1]:
        # print("Continuation")
        n = current.copy()
        n[2] += 1
        next_step(n, block+1, max_block)

    # 2. Repetition
    if current[1] == current[2]:
        # print("Repetition")
        n = current.copy()
        n[0] += n[1]
        n[2] = 1
        if n[0] < 100:
            next_step(n, block+1, max_block)

    # 3. Transition
    if current[1] == current[2]:
        # print(f"Transition {block}")
        y = current[1]*2
        n = current.copy()
        n[0] += y
        n[1] = y
        n[2] = 1
        causal = (n[0] - n[1] + 1) >= 0
        if causal:
            next_step(n, block+1, max_block)


if __name__ == "__main__":
    # edges = [
    #     ("A", "B", 7),
    #     ("A", "D", 5),
    #     ("B", "C", 8),
    #     ("B", "D", 9),
    #     ("B", "E", 7),
    #     ("C", "E", 5),
    #     ("D", "E", 15),
    #     ("D", "F", 6),
    #     ("E", "F", 8),
    #     ("E", "G", 9),
    #     ("F", "G", 11)
    # ]

    # print("Find the shortest path with Dijkstra")
    # print(edges)
    # print("A -> E:")
    # print(shortestPath(edges, "A", "E"))

    block_size = 256
    filter_size = 44100
    num_blocks = (filter_size + (block_size - 1)) // block_size
    current = [1, 1, 1]
    next_step(current, 1, num_blocks)
    # for i in range(1, num_blocks+1):
    #     print(f"{i}B {current}")
    #     if current[2] < current[1]:
    #         current[2] += 1
    #         # print("continuation")

    #     if current[1] == current[2]:
    #         current[0] += current[1]
    #         current[2] = 1
    #         # print("repeat")
