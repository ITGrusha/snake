from itertools import repeat
from pprint import pprint

if __name__ == '__main__':
    # matrix = [[0 for i in range(25)] for j in range(25)]
    matrix = list(repeat(list(repeat(0, 25)).copy(), 25)).copy()
    (matrix[0])[0] = 1
    pprint(matrix)
    print(matrix[16].__len__(), matrix[16][12] + 1)
