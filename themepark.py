
def solve(N,X,Y,O,C,U,T):


def read_input():
    N = [int(i) for i in input().split()]
    teleporters = [[int(i) for i in input().split()] for _ in range(K)]
    edges = defaultdict(list)
    for i in range(N):
        u, v, c = [int(i) for i in input().split()]
        edges[u].append((v, c))
        edges[v].append((u, c))
    return N, K, M, teleporters, edges


def main():
    N, K, M, teleporters, edges = read_input()
    cost = solve(N, K, M, teleporters, edges)
    print(cost)


if __name__ == '__main__':
    main()
