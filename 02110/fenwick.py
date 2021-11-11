def add(fenwick, i, v):
    while i < len(fenwick):
        fenwick[i] += v
        i += i & ~ i + 1

def sum(fenwick, i):
    s=0
    while i>0:
        s += fenwick[i]
        i -= i & ~ i + 1
    return s

n = int(input())
f = [0 for _ in range(10**6 + 1)]

for _ in range(n):
    i = int(input())