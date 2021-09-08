S = [500, 150, 500, 300, 450, 200]
B = [700, 300, 400, 300, 600, 300]
m = B[0] - S[0]


def profit(i, j):
    return B[j] - S[i] - 100 * (j - i)


# Q1 ------
# for i in range(len(S)):
#     for j in range(i, len(B)):
#         if profit(i, j) >= m:
#             m = profit(i, j)
#             print(m, i, j)

# Q2 -----

# Given a day x, i <= x, j > x
# N = input()
# S = input().split()
# B = input().split()


def profit(i, j):
    return int(B[j]) - int(S[i]) - 100 * (j - i)

Smax, Bmax = 6, 6

def sol(s, b, x):
    if x > 0:
        if x == len(S):
            s, b = len(S) - 1, len(B) - 1
            return sol(s, b, x - 1)
        for k in range(x):
            if profit(k, x) > profit(s, b):
                s, b = k, x
        return sol(s, b, x - 1)
    elif x == 0:

        return s, b


def solution(S, B):
    return sol(len(S), len(B), len(S))


Smax, Bmax = solution(S, B)

print(profit(Smax, Bmax))
