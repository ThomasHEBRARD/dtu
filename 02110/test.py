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
    def __init__(self, x):
        self.val = x
        self.next = None


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
print(findMedianSortedArrays([1, 2], [2]))
