import random


class GraphOriented(object):
    layers = None
    g = []
    neurons_number = 0

    def __init__(self, layers: list, weight_range=None):
        if weight_range is None:
            weight_range = [0, 1]

        neurons_number = 0
        for i in layers:
            neurons_number += i
        self.neurons_number = neurons_number
        self.layers = layers
        self.g = list(map(lambda x: [[] for _ in range(neurons_number)], [0]))[0]
        # pprint(self.g)
        n_before = 0
        neuron = -1
        for i in range(layers.__len__() - 1):
            for j in range(layers[i]):
                neuron += 1
                for k in range(layers[i + 1]):
                    self.g[neuron].append(list([n_before + layers[i] + k,
                                                random.uniform(weight_range[0], weight_range[1])]))
            n_before += layers[i]
        # print(self.g)

    @classmethod
    def restore(cls, g: list, layers: list):
        cls.layers = layers
        cls.g = g

        neurons_number = 0
        for i in layers:
            neurons_number += i

        cls.neurons_number = neurons_number
        return cls

    @classmethod
    def merge_graphs_random(cls, graphs: list):
        cls.layers = graphs[0].layers
        cls.neurons_number = graphs[0].neurons_number
        cls.g = graphs[0].g
        for i in range(cls.neurons_number):
            for j in range(cls.g[i].__len__()):
                cls.g[i][j] = random.choice([g.g[i][j] for g in graphs])
        return cls

    def calculate_graph(self, data) -> list:
        res = [0 for _ in range(self.neurons_number)]
        for i in range(self.layers[0]):
            res[i] = data[i]
        for i in range(0, self.neurons_number):
            # print(self.g)
            for j in range(self.g[i].__len__()):
                res[self.g[i][j][0]] += res[i] * self.g[i][j][1]
        # print(data)
        # print(res)
        return res[-self.layers[self.layers.__len__() - 1]:]
