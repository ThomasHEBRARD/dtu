# S = [500, 150, 500, 300, 450, 200]
# B = [700, 300, 400, 300, 600, 300]
# #########################################
# S = "133 149 351 466 351 411 435 456 96 334".split()
# B = "119 342 76 446 116 329 376 96 67 37".split()
# #########################################
# S = [1000, 1000, 1000, 100]
# B = [1100, 900, 1201, 1300]
# #########################################
# S = [1000]
# B = [1]
# #########################################
# S = [1]
# B = [1000]
# #########################################
# S = [
#     8706,
#     3505,
#     4828,
#     492,
#     7072,
#     2070,
#     9969,
#     237,
#     4520,
#     2404,
#     1392,
#     4300,
#     7391,
#     7156,
#     2286,
#     4206,
#     5829,
# ]

# B = [
#     3835,
#     7976,
#     9007,
#     9243,
#     7039,
#     5968,
#     7043,
#     5141,
#     1923,
#     5669,
#     9744,
#     4308,
#     7347,
#     9081,
#     2210,
#     7216,
#     7265,
# ]
# N = len(S)

# N = int(input())
# S = input().split()
# B = input().split()

# S = S[: len(B)]
# profits = []


# def solution(i):
#     for j in range(i, N):
#         profit = int(B[j]) - int(S[i]) - 100 * (j - i)
#         if profit > 0:
#             profits.append(profit)
#         else:
#             profits.append(0)
#     if i == N:
#         print(max(profits))
#     else:
#         solution(i + 1)

# solution(0)
def subsetsum(array, num):

    if num == 0 or num < 1:
        return None
    elif len(array) == 0:
        return None
    else:
        if array[0] == num:
            return [array[0]]
        else:
            with_v = subsetsum(array[1:], (num - array[0]))
            if with_v:
                return [array[0]] + with_v
            else:
                return subsetsum(array[1:], num)


print(subsetsum([2, 5, 8, 9, 12, 18], 25))
