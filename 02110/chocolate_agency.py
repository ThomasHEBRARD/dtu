S = [500, 150, 500, 300, 450, 200]
B = [700, 300, 400, 300, 600, 300]

def profit(i, j):
    return B[j] - S[i] - 100 * (j - i)

# Q1 ------
# m = B[0] - S[0]
# for i in range(len(S)):
#     for j in range(i, len(B)):
#         if profit(i, j) >= m:
#             m = profit(i, j)
#             print(m, i, j)
# Q2 -----


S = [500, 150, 500, 300, 450, 200]
B = [700, 300, 400, 300, 600, 300]

S = '133 149 351 466 351 411 435 456 96 334'.split()
B = '119 342 76 446 116 329 376 96 67 37'.split()

# S = [1000]
# B = [1]

# N = input()
# S = input().split()
# B = input().split()

n = len(S)
x0 = n - 2

def profit(i, j):
    return int(B[j]) - int(S[i]) - 100 * (j - i)

def sol(s, b, x):
    if x == 0:
        return max(profit(0, 1), profit(s, b))
    else:
        current_max = profit(s, b)
        b_index = x + 1
        for s_index in range(x + 1):
            if profit(s_index, b_index) > current_max:
                s, b = s_index, b_index
        return sol(s, b, x - 1)
        
if n > 1:
    print(sol(n-2, n-1, x0))
else:
    print(0)
