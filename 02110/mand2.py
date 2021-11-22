"""
12 3
-3 -1 2 -5 3 0 2 -3 2 3 -2 -3
-1 2 -5
1 12
2
1 12
-2 -3

Expected Output
2 11
"""
N, G = 12, 3
TRACK = [-3, -1, 2, -5, 3, 0, 2, -3, 2, 3, -2, -3]
ground_phases = [[-1, 2, -5], [2], [-2, -3]]
air_phases = [[1, 12], [1, 12]]

"""
3 2
0 1 2
0
1 3
1

Expected Output:
"Impossible"
"""
N, G = 3, 2
TRACK = [0, 1, 2]
ground_phases = [[0], [1]]
air_phases = [[1, 3]]
"""
30 3
0 0 1 0 0 1 1 0 1 0 0 1 0 0 0 1 0 1 1 0 0 0 1 1 1 0 1 0 1 1
0
1 30
1
1 30
1 0 1 1

Expected Output:
1 30
"""
# N, G = 30, 3
# TRACK = [
#     0,
#     0,
#     1,
#     0,
#     0,
#     1,
#     1,
#     0,
#     1,
#     0,
#     0,
#     1,
#     0,
#     0,
#     0,
#     1,
#     0,
#     1,
#     1,
#     0,
#     0,
#     0,
#     1,
#     1,
#     1,
#     0,
#     1,
#     0,
#     1,
#     1,
# ]
# ground_phases = [[0], [1], [1, 0, 1, 1]]
# air_phases = [[1, 30], [1, 30]]
"""
32 4
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0
1 32
0
1 32
0 0 0 0 0 0
1 32
0 0 0

Expected Output:
1 32
"""
N, G = 32, 4
TRACK = [
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
]
ground_phases = [[0, 0, 0, 0, 0], [0], [0, 0, 0, 0, 0, 0], [0, 0, 0]]
air_phases = [[1, 32], [1, 32], [1, 32]]

"""
252 3
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 12 -45 -12 -35 -6 30 4 -9 -20 41 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 -48 39 46 -16 22 -33 -39 -4 -16 28 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 -28 10 2 49 27 18 22 -21 6 49 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 12 -45 -12 -35 -6 30 4 -9 -20 41 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
1 252
0 0 0 0 0 0 0 0 0 0 0 0 0 0 -48 39 46 -16 22 -33 -39 -4 -16 28 0 0 0 0 0 0 0 0 0 0 0 0 0 0
1 252
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 -28 10 2 49 27 18 22 -21 6 49 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0

Expected Output:
21 211
"""
# N, G = 252, 3
# TRACK = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 12, -45, -12, -35, -6, 30, 4, -9, -20, 41, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -48, 39, 46, -16, 22, -33, -39, -4, -16, 28, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -28, 10, 2, 49, 27, 18, 22, -21, 6, 49, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
# ground_phases = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 12, -45, -12, -35, -6, 30, 4, -9, -20, 41, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -48, 39, 46, -16, 22, -33, -39, -4, -16, 28, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -28, 10, 2, 49, 27, 18, 22, -21, 6, 49, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
# air_phases = [[1, 252], [1, 252]]

# N, G = map(int, input().split())
# TRACK = list(map(int, input().split()))
# nbr_lines = 1 + 2 * G
# air_phases = []
# ground_phases = []

# for i in range(3, nbr_lines + 1):
#     if i % 2 == 0:
#         air_phases.append(list(map(int, input().split())))
#     else:
#         ground_phases.append(list(map(int, input().split())))

with open("Samples07.in") as f:
    N, G = map(int, f.readline().split())
    TRACK = list(map(int, f.readline().split()))
    nbr_lines = 1 + 2 * G
    air_phases = []
    ground_phases = []

    for i in range(3, nbr_lines + 1):
        if i % 2 == 0:
            air_phases.append(list(map(int, f.readline().split())))
        else:
            ground_phases.append(list(map(int, f.readline().split())))


def computeLPSArray(pat, M, lps):
    len = 0

    lps[0]
    i = 1

    while i < M:
        if pat[i] == pat[len]:
            len += 1
            lps[i] = len
            i += 1
        else:
            if len != 0:
                len = lps[len - 1]
            else:
                lps[i] = 0
                i += 1


def KMPSearch(pat, txt, NN, need_first=False):
    M = len(pat)
    N = len(txt)
    result = []
    lps = [0] * M
    j = 0

    computeLPSArray(pat, M, lps)

    i = 0
    while i < N:

        if pat[j] == txt[i]:
            i += 1
            j += 1

        if j == M:
            if need_first and i - j >= 0:
                return [i - j]
            elif 1 <= i - j <= NN:
                result.append(i - j)
            j = lps[j - 1]

        elif i < N and pat[j] != txt[i]:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1
    return result


class Solution:
    def __init__(self, N):
        self.N = N
        self.result = [0, 0]
        self.first = -1

    def dfs(self, track, air, ground, count):
        if not ground and not air:
            if count > self.result[1] or (
                count == self.result and self.first + 1 < self.result[0]
            ):
                self.result = [self.first + 1, count]
            return

        all_positions = []

        if len(ground) == 1:
            all_positions = KMPSearch(ground[0], track, self.N, False)
            all_positions = all_positions[-1:]
        else:
            all_positions = KMPSearch(ground[0], track, self.N, len(ground) != 1)

        for position in all_positions:
            self.dfs(
                track[position + len(ground[0]) :],
                air[1:],
                ground[1:],
                count + position + len(ground[0]),
            )

    def sol(self, track, air, ground, count):
        all_positions = KMPSearch(ground[0], track, self.N, True)
        self.first = all_positions[0]
        count = len(ground[0])
        self.dfs(track[self.first + count :], air, ground[1:], count)

        if self.result != [0, 0]:
            return str(self.result[0]) + " " + str(self.result[1])
        else:
            return "Impossible"


sol = Solution(N)
print(sol.sol(TRACK, air_phases, ground_phases, 0))
