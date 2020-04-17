from typing import List
import math
Vector = List[float]
Matrix = List[Vector]


def zero_matrix(rows, cols, initial=0.):
    return [[initial] * cols for i in range(rows)]


def tnh(vertex: Matrix):
    return [[math.tanh(x) for x in row] for row in vertex]


def rlu(vertex: Matrix, alpha: float):
    return [[max(x, x * alpha) for x in row] for row in vertex]


def mul(vertex1: Matrix, vertex2: Matrix):
    rowsA = len(vertex1)
    colsA = len(vertex1[0])
    rowsB = len(vertex2)
    colsB = len(vertex2[0])
    res = zero_matrix(rowsA, colsB)
    for i in range(rowsA):
        for j in range(colsB):
            total = 0
            for ii in range(colsA):
                total += vertex1[i][ii] * vertex2[ii][j]
            res[i][j] = total

    return res


def sum_v(vertices: List[Matrix]):
    n, rows, cols = len(vertices), len(vertices[0]), len(vertices[0][0])
    res = zero_matrix(rows, cols)
    for i in range(rows):
        for j in range(cols):
            for k in range(n):
                res[i][j] += vertices[k][i][j]
    return res


def had(vertices: List[Matrix]):
    n, rows, cols = len(vertices), len(vertices[0]), len(vertices[0][0])
    res = zero_matrix(rows, cols, 1.0)
    for i in range(rows):
        for j in range(cols):
            for k in range(n):
                res[i][j] *= vertices[k][i][j]
    return res


n, m, k = map(int, input().split())
variables = [[int(x) for x in input().split()[1:]] for i in range(m)]
commands = []
for i in range(n - m):
    data = input().split()
    command = (data[0], list(map(int, data[1:])))
    commands.append(command)

vertices, diffVertices = [], []
for i in range(m):
    rows, cols = variables[i][0], variables[i][1]
    vertices.append([[float(x) for x in input().split()] for i in range(rows)])
    diffVertices.append(zero_matrix(rows, cols))

if k + m > n:
    for i in range(n - k, m + 1):
        diffVertices[i] = list(map(float, input().split()))
        print(*vertices[i])

for i in range(n - m):
    cmd = commands[i]
    vertex = None

    if cmd[0] == 'tnh':
        idx = cmd[1][0] - 1
        vertex = tnh(vertices[idx])
    elif cmd[0] == 'rlu':
        alpha = 1.0 / cmd[1][0]
        idx = cmd[1][1] - 1
        vertex = rlu(vertices[idx], alpha)
    elif cmd[0] == 'mul':
        idx1 = cmd[1][0] - 1
        idx2 = cmd[1][1] - 1
        vertex = mul(vertices[idx1], vertices[idx2])
    elif cmd[0] == 'sum':
        vertices_to_sum = [vertices[i - 1] for i in cmd[1][1:]]
        vertex = sum_v(vertices_to_sum)
    elif cmd[0] == 'had':
        vertices_to_had = [vertices[i - 1] for i in cmd[1][1:]]
        vertex = had(vertices_to_had)
    else:
        raise Exception(f'Unknown command "{cmd[0]}"')

    vertices.append(vertex)
    r, c = len(vertices[-1]), len(vertices[-1][0])
    if i < n - k - m:
        diffVertices.append(zero_matrix(r, c))
    else:
        print(*vertex)
        diffVertices.append([float(x) for x in input().split()] for i in range(r))