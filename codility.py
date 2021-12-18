import string

# idea: Keep track of the letters we see in two
# separates array, one for the Uppercase letter, another for the lowercase
# letters. At the end, take the biggest index that has letters in both arrays
# Time complexity: We traverse 2 times the array of size N: O(N)
# Space complexity: We user 2 arrays of size N: O(N)


def solution1(S):
    def get_index(letter):
        return string.ascii_letters.index(letter)

    max_index = ["NO", -1]
    U, L = ["NO"] * 26, ["NO"] * 26

    for s in S:
        if s.islower():
            L[get_index(s)] = s
        elif s.isupper():
            U[get_index(s) - 26] = s

    for i in range(26):
        if U[i] != "NO" and L[i] != "NO":
            if i > max_index[1]:
                max_index = [U[i], i]

    return max_index[0]


# print(solution1("aaBabcDaA"))
# print(solution1("Codility"))
# print(solution1("WeTestCodErs"))
# print(solution1("aaaabbbbbbB"))

import random


def solution2(N):
    i = 1
    ans = []
    s = 0
    while n > 1:
        ans.append(i)
        s += i
        i += 1
        n -= 1
    ans.append(-s)
    return ans


import math


def solution3(A, B, C):
    if divmod(A, 2)[0] - 1 + divmod(A, 2)[1] > B + C:
        return ""
    res = ""
    MAP = {"a": A, "b": B, "c": C}

    def is_valid(string, new_letter):
        if len(string) < 2:
            return True
        if string[-1] == new_letter and string[-2] == new_letter:
            return False
        return True

    while MAP["a"] or MAP["b"] or MAP["c"]:
        MAP = {k: v for k, v in sorted(MAP.items(), key=lambda item: -item[1])}
        order_to_test = list(MAP.keys())

        for k in order_to_test:
            if is_valid(res, k) and MAP[k]:
                res += k
                MAP[k] -= 1
                break
        else:   
            return res
    return res


print(solution3(9, 2, 1))
