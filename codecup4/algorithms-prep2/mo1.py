R = lambda : map(int, raw_input().split())
n, k = R()
s = sum(R())
print(n - (s/k + (s%k > 0)))