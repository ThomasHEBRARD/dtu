import numpy as np

"""
5 3
10 7 5 3  0
1  0 2 16 15
0  1 1 11 12

76
"""
N, M = 5, 3
D = [[10, 7, 5, 3, 0], [1, 0, 2, 16, 15], [0, 1, 1, 11, 12]]
"""
2 4
6 4
10000 12
0 1
13 14

10050
"""
# N, M = 2, 4
# D = [[6, 4], [10000, 12], [0, 1], [13, 14]]
"""
10 1
100 99 14 18 0 4910 42 7654 4 0

12664
# """
# N, M = 10, 1
# D = [[100, 99, 14, 18, 0, 4910, 42, 7654, 4, 0]]

####

# N, M = input().split()
# N = int(N)
# M = int(M)
# D = []
# for _ in range(M):
#     D.append(input().split())

total = 0
C = [0, 1, 3]

# les 2 prochains, ceux qui ont le pire, cad qu'il ne vuat pas le coup de rester
tab = np.zeros(N)

for i in range(1, 3):
    for j in range(N):
        tab[j] += D[i][j]

ind = np.argpartition(tab, -4)[:3]
print(ind)

# first = np.array(D[0])
# first_indexes = list(np.argpartition(first, -4)[-4:])
# first_values = list(first[first_indexes])

# second = np.array(D[1])
# second_indexes = list(np.argpartition(second, -4)[-4:])
# second_values = list(second[second_indexes])

# indexes_to_keep = []

# for i in range(len(first_indexes)):
#     if first_indexes[i] in second_indexes:
#         indexes_to_keep.append(first_indexes[i])

# print(indexes_to_keep)

# for i in range(M):
#     total += int(D[0][C[i]])


def sol(n, m, d, total):
    if m == 1:
        for _ in range(3):
            c_max = max(d[0])
            total += c_max
            for i in range(len(d[0])):
                if d[0][i] == c_max:
                    del d[0][i]
                    break
    elif n <= m:
        return sum([sum(dd) for dd in d])
    else:
        for i in range(1, m):
            min, index = int(d[i][C[0]]), C[0]

            for j in range(1, m):
                if int(d[i][C[j]]) < min:
                    min, index = int(d[i][C[j]]), C[j]

            max_to_change_to = max(
                [int(d[i][f]) for f in [k for k in range(n) if k not in C]]
            )
            c_index_to_change = C.index(index)

            C[c_index_to_change] = d[i].index(max_to_change_to)
            total += int(d[i][C[0]]) + int(d[i][C[1]]) + int(d[i][C[2]])
    return total


print(sol(N, M, D, total))
