import json
import os
from api import graph


def get_graph(filename: str) -> graph.GraphOriented:
    file = open(filename, 'r')
    obj = json.loads(file.read().replace('\n', ''))
    gr = graph.GraphOriented.restore(obj[0], obj[1])
    return gr


def write_graph(filename: str, gr: graph.GraphOriented) -> bool:
    file = open(filename, 'w')
    file.write(json.dumps([gr.g, gr.layers]))
    return True


def make_dir(direct: str):
    if not os.path.isdir(direct):
        return os.makedirs(direct)
    return True
