def divide(dividend, divisor):
    result = divisor
    c = 0
    while result > dividend:
        result -= dividend
        c += 1
    return c


def isPalindrome(s):
    s = "".join(e for e in s if e.isalnum()).lower()
    if not s:
        return True
    else:
        return recur(s)


def recur(s):
    if len(s) in (2, 3):
        return s[0] == s[-1]
    if s[0] == s[-1]:
        return recur(s[1:-1])
    else:
        return False


class ListNode(object):
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


def addTwoNumbers(l1, l2):
    result = ListNode(0)
    result_tail = result
    carry = 0

    while l1 or l2 or carry:
        val1 = l1.val if l1 else 0
        val2 = l2.val if l2 else 0
        carry, out = divmod(val1 + val2 + carry, 10)

        result_tail.next = ListNode(out)
        result_tail = result_tail.next

        l1 = l1.next if l1 else None
        l2 = l2.next if l2 else None

    return [
        result.val,
        result.next.val,
        result.next.next.val,
        result.next.next.next.val,
    ]


l1 = ListNode(2)
l1.next = ListNode(4)
l1.next.next = ListNode(3)

l2 = ListNode(5)
l2.next = ListNode(6)
l2.next.next = ListNode(4)

# print(addTwoNumbers(l1,l2))


def lengthOfLongestSubstring(s):
    s = s.strip()
    if not s:
        return 0
    M = {}
    maxx = []
    current_max = 0
    for i in range(len(s)):
        x = s[i]
        if x not in M:
            M[x] = i
            current_max += 1
        else:
            maxx.append(current_max)
            current_max = i - M[x]
            st = M[x]
            for k, v in M.items():
                if v <= st:
                    del M[k]
            M[x] = i
    maxx.append(current_max)
    return max(maxx)


def convert(s, numRows):
    if len(s) < numRows:
        return s
    if numRows == 1:
        return s
    M = {i: [] for i in range(numRows)}
    incr = True
    j = 0
    for i in range(len(s)):
        M[j].append(s[i])
        if j == numRows - 1:
            incr = False
        elif j == 0:
            incr = True
        if incr:
            j += 1
        else:
            j -= 1

    final = []
    for i in range(numRows):
        for k in M[i]:
            final.append(k)
    return "".join(final)


def isTrue(s):
    return s == "AB"


def isPalindrome(integer):
    if integer < 0:
        return False
    r_integer = 0
    while integer > r_integer:
        r_integer = r_integer * 10 + integer % 10
        integer /= 10

    return integer == r_integer


def twoSum(nums, target):
    M = {}
    for i in range(len(nums)):
        if target - nums[i] in M:
            return [i, M[target - nums[i]]]
        else:
            M[nums[i]] = i


def twoSumII(numbers, target):
    M = {}
    for i in range(len(numbers)):
        if target - numbers[i] in M:
            a = [i + 1, M[target - numbers[i]] + 1]
            a.sort()
            return a
        else:
            M[numbers[i]] = i


def threeSum(nums):
    i, j, k = None, None, None
    sol = []
    for l in range(len(nums)):
        nums_modified = []
        for o in range(len(nums)):
            if o != l:
                nums_modified.append(nums[o])
        two = twoSum(nums_modified, -nums[l])
        if two:
            s = [nums[l], nums_modified[two[0]], nums_modified[two[1]]]
            s.sort()
            if s not in sol:
                sol.append(s)
    return sol


def findMedianSortedArrays(nums1, nums2):
    l = len(nums1) + len(nums2)
    l2 = l // 2 + 1
    print(l2)
    arr = []
    i, j = 0, 0
    while len(arr) < l2:
        print(arr, nums1, nums2)
        if i == len(nums1):
            arr.append(nums2[0])
            del nums2[0]
        elif j == len(nums2):
            arr.append(nums1[0])
            del nums1[0]

        else:
            if nums1[i] < nums2[j]:
                arr.append(nums1[i])
                i += 1
            elif nums2[j] < nums2[i]:
                arr.append(nums2[j])
                j += 1

    if l % 2 == 0:
        return (arr[-2] + arr[-1]) / 2
    else:
        return arr[-1]


# print(findMedianSortedArrays([1, 2], [3, 4]))
# print(findMedianSortedArrays([1, 2], [2]))


class SolutionReverseLinkedList:
    def __init__(self, linked_list):
        self.result = ListNode(None)
        self.linked_list = linked_list
        self.to_do = []

    def reverseList(self, head):
        if head.next != None:
            self.to_do.append(head)
            self.reverseList(head.next)
        else:
            self.result.next = head
            for h in self.to_do:
                self.result.next = h

    def __repr__(self):
        node = self.result
        l = []
        while node != None:
            l.append(node.val)
            node = node.next
        return str(l)


# linked_list = ListNode(1, ListNode(2, ListNode(3, ListNode(4, ListNode(5, None)))))
# sol = SolutionReverseLinkedList(linked_list)
# sol.reverseList(linked_list)
# print(sol)


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
            print("Found pattern at index " + str(i - j))
            j = lps[j - 1]

        # mismatch after j matches
        elif i < N and pat[j] != txt[i]:
            # Do not match lps[0..lps[j-1]] characters,
            # they will match anyway
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1


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


# txt = "ABABDABACDABABCABAB"
# pat = "ABABCABAB"

# txt = [1, 2, 3, 4, 5, -6, 7, 8, 9, 3, 4, 5, -6]
# pat = [3, 4, 5, -6]
# KMPSearch(pat, txt)


class Solution:
    def numIslands(self, grid):
        if not grid:
            return 0
        n, m = len(grid), len(grid[0])
        nbr_islands = 0

        marked = {}

        def vert_hor(i, j):
            return [[i - 1, j], [i, j - 1], [i + 1, j], [i, j + 1]]

        def get_children(i, j):
            children = []
            for k, l in vert_hor(i, j):
                if (
                    k in range(n)
                    and l in range(m)
                    and grid[k][l] == "1"
                    and str(k) + str(l) not in marked
                ):
                    children.append([k, l])
            return children

        def BFS(i, j):
            if str(i) + str(j) in marked:
                return
            marked[str(i) + str(j)] = True
            children = get_children(i, j)
            if not children:
                return
            for child in children:
                BFS(child[0], child[1])

        for i in range(n):
            for j in range(m):
                if grid[i][j] == "1" and str(i) + str(j) not in marked:
                    BFS(i, j)
                    nbr_islands += 1
        return nbr_islands


# sol = Solution()
# print(sol.numIslands([["1", "1", "1"], ["0", "1", "0"], ["0", "1", "0"]]))


def longestPrefix(s):
    m = ""
    for i in range(len(s)-1):
        if s[:i+1] == s[-(i+1):]:
            m = s[:i+1]
    return m


print(longestPrefix("ababab"))
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
# N, G = 3, 2
# TRACK = [0, 1, 2]
# ground_phases = [[0], [1]]
# air_phases = [[1, 3]]
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
# N, G = 32, 4
# TRACK = [
#     0,
#     0,
#     0,
#     0,
#     0,
#     0,
#     0,
#     0,
#     0,
#     0,
#     0,
#     0,
#     0,
#     0,
#     0,
#     0,
#     0,
#     0,
#     0,
#     0,
#     0,
#     0,
#     0,
#     0,
#     0,
#     0,
#     0,
#     0,
#     0,
#     0,
#     0,
#     0,
# ]
# ground_phases = [[0, 0, 0, 0, 0], [0], [0, 0, 0, 0, 0, 0], [0, 0, 0]]
# air_phases = [[1, 32], [1, 32], [1, 32]]

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

N, G = map(int, input().split())
TRACK = list(map(int, input().split()))
nbr_lines = 1 + 2 * G
air_phases = []
ground_phases = []

for i in range(3, nbr_lines + 1):
    if i % 2 == 0:
        air_phases.append(list(map(int, input().split())))
    else:
        ground_phases.append(list(map(int, input().split())))

# with open("Samples07.in") as f:
#     N, G = map(int, f.readline().split())
#     TRACK = list(map(int, f.readline().split()))
#     nbr_lines = 1 + 2 * G
#     air_phases = []
#     ground_phases = []

#     for i in range(3, nbr_lines + 1):
#         if i % 2 == 0:
#             air_phases.append(list(map(int, f.readline().split())))
#         else:
#             ground_phases.append(list(map(int, f.readline().split())))


def PIArray(pat, M, array):
    idx = 0

    array[0]
    i = 1

    while i < M:
        if pat[i] == pat[idx]:
            idx += 1
            array[i] = idx
            i += 1
        else:
            if idx != 0:
                idx = array[idx - 1]
            else:
                array[i] = 0
                i += 1


def KMPSearch(pattern, text, NN, need_first=True):
    M = len(pattern)
    N = len(text)
    result = []
    array = [0] * M
    j = 0

    if not need_first:
        pattern = pattern[::-1]
        text = text[::-1][:-1]
        N -= 1

    PIArray(pattern, M, array)

    i = 0
    while i < N:

        if pattern[j] == text[i]:
            i += 1
            j += 1

        if j == M:
            r = len(text) - (i - j) - len(pattern) + 1
            if not need_first and 1 <= r <= NN:
                return [r]
            return [i - j]
            j = array[j - 1]

        elif i < N and pattern[j] != text[i]:
            if j != 0:
                j = array[j - 1]
            else:
                i += 1
    return result


class Solution:
    def __init__(self, N):
        self.N = N
        self.result = [0, 0]
        self.first = -1

    def dfs(self, track, air, ground, count):
        if not ground:
            if count > self.result[1] or (
                count == self.result and self.first + 1 < self.result[0]
            ):
                self.result = [self.first + 1, count]
            return

        position = KMPSearch(ground[0], track, self.N, len(ground) != 1)

        if position:
            position = position[0]
        else:
            return

        self.dfs(
            track[position + len(ground[0]) :],
            air[1:],
            ground[1:],
            count + position + len(ground[0]),
        )

    def sol(self, track, air, ground, count):
        self.first = KMPSearch(ground[0], track, self.N)[0]
        count = len(ground[0])
        self.dfs(track[self.first + count :], air, ground[1:], count)

        if self.result != [0, 0]:
            return str(self.result[0]) + " " + str(self.result[1])
        else:
            return "Impossible"


sol = Solution(N)
print(sol.sol(TRACK, air_phases, ground_phases, 0))
