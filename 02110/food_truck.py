"""
5 3
10 7 5 3  0
1  0 2 16 15
0  1 1 11 12

76
"""
D = [[10, 7, 5, 3, 0], [1, 0, 2, 16, 15], [0, 1, 1, 11, 11]]
# D = [
#     [1000000, 0, 1000000, 0, 1000001],
#     [1000000, 0, 0, 1000000, 1000001],
#     [1000000, 0, 1000000, 0, 1000001],
#     [1000000, 0, 0, 1000000, 1000001],
#     [1000000, 0, 1000000, 0, 1000001],
#     [1000000, 0, 0, 1000000, 1000001],
#     [1000000, 0, 1000000, 0, 1000001],
#     [1000000, 0, 0, 1000000, 1000001],
#     [1000000, 0, 1000000, 0, 1000001],
#     [1000000, 0, 0, 1000000, 1000001],
#     [1000000, 0, 1000000, 0, 1000001],
#     [1000000, 0, 0, 1000000, 1000001],
#     [1000000, 0, 0, 1000000, 1000001],
#     [1000000, 0, 1000000, 0, 1000001],
# ]
N, M = len(D[0]), len(D)
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
import itertools
from collections import defaultdict

# N, M = input().split()
# N = int(N)
# M = int(M)
# D = []
# for _ in range(M):
# D.append(list(map(int, input().split())))


def list_duplicates(seq):
    tally = defaultdict(list)
    for i, item in enumerate(seq):
        tally[item].append(i)
    return ((key, locs) for key, locs in tally.items() if len(locs) > 1)


R = range(N)


def OPT(cri):
    if cri == 0:
        return [[sum([D[0][x] for x in C]), C]]
    else:
        for OPT_DATA in OPT(cri - 1):
            opt_max, optc = OPT_DATA
            c_2_v = [D[cri][pi] if pi not in [optc[0], optc[1]] else None for pi in R]
            case_2_max = max([a for a in c_2_v if a is not None])
            case_2_index = c_2_v.index(case_2_max)

            c_3_v = [D[cri][pi] if pi not in [optc[0], optc[2]] else None for pi in R]
            case_3_max = max([a for a in c_3_v if a is not None])
            case_3_index = c_3_v.index(case_3_max)

            c_4_v = [D[cri][pi] if pi not in [optc[1], optc[2]] else None for pi in R]
            case_4_max = max([a for a in c_4_v if a is not None])
            case_4_index = c_4_v.index(case_4_max)

            case_C = [
                [optc[0], optc[1], optc[2]],
                [optc[0], optc[1], case_2_index],
                [optc[0], case_3_index, optc[2]],
                [case_4_index, optc[1], optc[2]],
            ]

            cases = [
                opt_max + D[cri][optc[0]] + D[cri][optc[1]] + D[cri][optc[2]],
                opt_max + D[cri][optc[0]] + D[cri][optc[1]] + D[cri][case_2_index],
                opt_max + D[cri][optc[0]] + D[cri][case_3_index] + D[cri][optc[2]],
                opt_max + D[cri][case_4_index] + D[cri][optc[1]] + D[cri][optc[2]],
            ]

            new_total = max(cases)
            max_case_index = cases.index(new_total)
            le_case_en_question = case_C[max_case_index]
            counter_case_C = [le_case_en_question]

            so = list_duplicates(D[cri])
            # [(1, [1, 2]), (11, [3, 4])]
            # if new_total == 75:
            #     print(list(so))
            for s in so:
                ind = list(s)[1]
                for i in ind:
                    if i in le_case_en_question:
                        opt_to_replace = le_case_en_question.index(i)
                for i in ind:
                    # if new_total == 75:
                    #     print(i)
                    if (
                        i != le_case_en_question[opt_to_replace]
                        and i not in le_case_en_question
                    ):
                        counter_case_C.append(
                            [
                                i if x == le_case_en_question[opt_to_replace] else x
                                for x in le_case_en_question
                            ]
                        )
            return [[new_total, cas] for cas in counter_case_C]


# edge cases:
if M == 1:
    d = D[0]
    total = 0
    for _ in range(3):
        if d:
            c_max = max(d)
            total += c_max
            for i in range(len(d)):
                if d[i] == c_max:
                    del d[i]
                    break
    print(total)
elif N <= 3:
    print(sum([sum(dd) for dd in D]))

# General case
else:
    initial_C = list(set(itertools.combinations(range(N), 3)))
    solutions = []
    for initial_c in initial_C:
        C = list(initial_c)
        solution = OPT(M - 1)
        if solution[0][0] == 75:
            print(solution)
        solutions.append(solution[0][0])

    print(max(solutions))
