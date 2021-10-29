import itertools

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
#     D.append(list(map(int, input().split())))


# To remove cause i need to test every possible entry


def list_exclude(to_exclude):
    return [i for i in range(N) if i not in to_exclude]


def sol(cri, current_total):
    if cri == M:
        return current_total
    else:
        d = D[cri]

        case_2_values = [
            d[pi] if pi in list_exclude([C[cri][0], C[cri][1]]) else None
            for pi in range(N)
        ]
        case_2_max = max(case_2_values)
        case_2_index = case_2_values.index(case_2_max)

        case_3_values = [
            d[pi] if pi in list_exclude([C[cri][0], C[cri][2]]) else None
            for pi in range(N)
        ]
        case_3_max = max(case_3_values)
        case_3_index = case_3_values.index(case_3_max)

        case_4_values = [
            d[pi] if pi in list_exclude([C[cri][1], C[cri][2]]) else None
            for pi in range(N)
        ]
        case_4_max = max(case_4_values)
        case_4_index = case_4_values.index(case_4_max)

        case_C = [
            [C[cri][0], C[cri][1], C[cri][2]],
            [C[cri][0], C[cri][1], case_2_index],
            [C[cri][0], case_3_index, C[cri][2]],
            [case_4_index, C[cri][1], C[cri][2]],
        ]

        case_1 = current_total + d[C[cri][0]] + d[C[cri][1]] + d[C[cri][2]]
        case_2 = current_total + d[C[cri][0]] + d[C[cri][1]] + d[case_2_index]
        case_3 = current_total + d[C[cri][0]] + d[case_3_index] + d[C[cri][2]]
        case_4 = current_total + d[case_4_index] + d[C[cri][1]] + d[C[cri][2]]

        cases = [case_1, case_2, case_3, case_4]

        current_total = max(cases)
        max_case_index = cases.index(current_total)

        C.append(case_C[max_case_index])

        return sol(cri + 1, max(case_1, case_2, case_3, case_4))


# [0, 1, 3]
# [0, 3, 4]
# [2, 3, 4]


if M == 1:
    d = D[0]
    total = 0
    for _ in range(3):
        c_max = max(d)
        total += c_max
        for i in range(len(d)):
            if d[i] == c_max:
                del d[i]
                break
    print(total)
elif N <= M:
    print(sum([sum(dd) for dd in D]))
else:
    # initial_C = [[0, 1, 3]]
    initial_C = list(set(itertools.combinations(range(N), 3)))
    solutions = []
    for initial_c in initial_C:
        C = [list(initial_c)]
        solution = sol(0, 0)
        solutions.append(solution)
        print(solution, C)
    print(max(solutions))
