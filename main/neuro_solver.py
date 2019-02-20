from api.graph import GraphOriented
from api import files
import os
import json


def solve(data: list, model: str) -> str:
    if not data[0]:
        return "N"
    graph: GraphOriented
    if os.path.isfile('../models/{}'.format(model)):
        graph = files.get_graph('../models/{}'.format(model))
        res = graph.calculate_graph(graph, data=data[1:])
    else:
        graph = GraphOriented([7, 6, 4, 3], weight_range=[0.01, 0.5])
        files.write_graph('../models/{}'.format(model), graph)
        res = graph.calculate_graph(data=data[1:])
    # res = graph.calculate_graph(graph, data=data[1:])
    maxn = max(res)
    # print(res)
    # print(maxn)
    for i in range(0, res.__len__()):
        if res[i] == maxn:
            res = i
            break
    dirs = {0: 'L', 1: 'F', 2: 'R'}
    return dirs[res]
