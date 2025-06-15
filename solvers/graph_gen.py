from math import lcm

M1 = (
    (12, 15, 16, 18, 24),
    (10, 15, 18, 20, 21),
    (10, 12, 15, 20, 25),
    (12, 14, 18, 21, 36),
    (12, 14, 16, 18, 21),
    (10, 12, 16, 18, 27),
    (10, 12, 15, 18, 20)
)

M2 = (
    (1, 2, 3, 8, 9),
    (1, 2, 3, 5, 6),
    (1, 2, 3, 4, 7),
    (1, 2, 4, 6, 7),
    (1, 3, 6, 8, 9)
)


def gen_hasse(v: list) -> list:
    edges = []
    dividers = {i: [] for i in v}
    v.sort()

    for v1 in reversed(v):
        for v2 in reversed(v):
            prime_divider = all([d % v2 for d in dividers[v1]])
            if v1 != v2 and v1 % v2 == 0 and prime_divider:
                edges.append((v2, v1))
                dividers[v1].append(v2)

    edges.sort()
    return edges


def gen_lcm(vertex: list) -> int:
    lcm_vertex = 1
    for i in range(len(vertex)):
        lcm_vertex = lcm(lcm_vertex, vertex[i])
    return lcm_vertex


def gen_graph(n: int) -> tuple[list, list]:
    """
    :param n: number in journal
    :return: tuple of vertex and edges
    """
    vertex = list(M1[n % 7] + M2[n // 7])
    vertex.append(gen_lcm(vertex))
    edges = gen_hasse(vertex)
    return vertex, edges


if __name__ == "__main__":
    print(gen_graph(2))
