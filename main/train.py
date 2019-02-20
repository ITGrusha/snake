import getopt
import sys
import random
from api.graph import GraphOriented
from api import files
from main import main as snake


def main(argv):
    GENERATIONS: int
    INDIVIDUALS: int
    VERSION: str
    try:
        opts, args = getopt.getopt(argv, 'hg:n:V:', ['generations=', 'individuals-number=', 'model-version='])
    except getopt.GetoptError:
        print('train.py -g <generations> -n <test-number>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('train.py -g <generations> -n <test-number>')
            sys.exit()
        elif opt in ['-g', '--generations']:
            GENERATIONS = int(arg)
        elif opt in ['-n', '--individuals-number']:
            INDIVIDUALS = int(arg)
        elif opt in ['-V', '--model-version']:
            VERSION = arg

    files.make_dir('../models/{}'.format(VERSION))
    results: dict = {}
    for i in range(INDIVIDUALS):
        filename = '{}/graph0{}.json'.format(VERSION, i)
        res = snake(['-g', 'false', '-a', 'true', '--model={}'.format(filename)])
        results[filename] = res
    for i in range(1, GENERATIONS):
        for j in range(INDIVIDUALS):
            a, b = random.choices(list(results.keys()), k=2)
            graph_a = files.get_graph('../models/{}'.format(a))
            graph_b = files.get_graph('../models/{}'.format(b))
            graph = GraphOriented.merge_graphs_random([graph_a, graph_b])
            #
            # MUTATION
            #
            if random.random() < 0.2:
                y = random.randrange(0, graph.neurons_number - graph.layers[-1])
                x = random.randrange(0, graph.g[y].__len__())
                graph.g[y][x][1] = 1 - graph.g[y][x][1]
            filename = '../models/{}/graph{}{}.json'.format(VERSION, i, j)
            files.write_graph(filename, graph)
            filename = '{}/graph{}{}.json'.format(VERSION, i, j)
            # res = snake(['-g', 'false', '-a', 'true', '--model={}'.format(filename)])
            results[filename] = [0, 0]
        for j in range(results.__len__()):
            filename = list(results.keys())[j]
            res = snake(['-g', 'false', '-a', 'true', '--model={}'.format(filename)])
            results[filename] = res

        results = dict(sorted(results.items(), key=lambda l: l[1][1], reverse=True))
        results = dict(sorted(results.items(), key=lambda l: l[1][0], reverse=True)[:INDIVIDUALS])
        results = results
        print(results)


def check(version, generation, population):
    results = dict({})
    for i in range(population):
        filename = '{}/graph{}{}.json'.format(version, generation, i)
        res = snake(['-g', 'false', '-a', 'true', '--model={}'.format(filename)])
        results[filename] = res
    results = dict(sorted(results.items(), key=lambda l: l[1][1], reverse=True))
    results = dict(sorted(results.items(), key=lambda l: l[1][0], reverse=True)[:population])
    print(results)


if __name__ == '__main__':
    main(sys.argv[1:])
