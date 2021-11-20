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
N, G = 30, 3
TRACK = [
    0,
    0,
    1,
    0,
    0,
    1,
    1,
    0,
    1,
    0,
    0,
    1,
    0,
    0,
    0,
    1,
    0,
    1,
    1,
    0,
    0,
    0,
    1,
    1,
    1,
    0,
    1,
    0,
    1,
    1,
]
ground_phases = [[0], [1], [1, 0, 1, 1]]
air_phases = [[1, 30], [1, 30]]
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
1 31
"""

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


def computeLPSArray(pat, M, lps):
    len = 0  # length of the previous longest prefix suffix

    lps[0]  # lps[0] is always 0
    i = 1

    # the loop calculates lps[i] for i = 1 to M-1
    while i < M:
        if pat[i] == pat[len]:
            len += 1
            lps[i] = len
            i += 1
        else:
            # This is tricky. Consider the example.
            # AAACAAAA and i = 7. The idea is similar
            # to search step.
            if len != 0:
                len = lps[len - 1]

                # Also, note that we do not increment i here
            else:
                lps[i] = 0
                i += 1


def KMPSearch(pat, txt):
    M = len(pat)
    N = len(txt)

    # create lps[] that will hold the longest prefix suffix
    # values for pattern
    lps = [0] * M
    j = 0  # index for pat[]

    # Preprocess the pattern (calculate lps[] array)
    computeLPSArray(pat, M, lps)

    i = 0  # index for txt[]
    while i < N:
        if pat[j] == txt[i]:
            i += 1
            j += 1

        if j == M:
            return i - j
            j = lps[j - 1]

        # mismatch after j matches
        elif i < N and pat[j] != txt[i]:
            # Do not match lps[0..lps[j-1]] characters,
            # they will match anyway
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1


class Solution:
    def __init__(self, N, G, TRACK, air_phases, ground_phases):
        self.N = N
        self.G = G
        self.track = TRACK
        self.air = air_phases
        self.ground = ground_phases
        self.current_ground_phase = 0
        self.current_pos = 0
        self.current_air_phase = 0
        self.first_pos = 0
        self.final_pos = 0
        self.sum_ground_phases = sum([len(g) for g in ground_phases])
        self.result = []

    def match(self, pos, m):
        to_match_with = self.track[pos : len(m) + 1]
        if m == to_match_with:
            return True
        return False

    def sol(self):
        if len(self.track[self.current_pos :]) < sum(
            [len(g) for g in self.ground[self.current_ground_phase :]]
        ):
            return "Impossible"
        if self.current_ground_phase >= len(
            self.ground
        ) and self.current_air_phase >= len(self.air):
            self.final_pos = self.current_pos
            # return self.first_pos, self.final_pos - self.first_pos
            self.result.append((self.first_pos, self.final_pos - self.first_pos))
            self.current_pos = i

            return

        for i in range(len(self.track[self.current_pos :])):
            index_found_for_next_ground_phase = KMPSearch(
                self.ground[self.current_ground_phase],
                self.track[self.current_pos :],
            )
            if len(self.track[self.current_pos :]) == N:
                self.first_pos = index_found_for_next_ground_phase

            self.current_pos += index_found_for_next_ground_phase + len(
                self.ground[self.current_ground_phase]
            )
            self.current_ground_phase += 1
            self.current_air_phase += 1

            return self.sol()


sol = Solution(N, G, TRACK, air_phases, ground_phases)
print("SOLUTION", sol.sol())
