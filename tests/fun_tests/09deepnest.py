def clamp(x: int, lo: int, hi: int) -> int:
    if x < lo:
        return lo
    else:
        if x > hi:
            return hi
        else:
            return x

def total(n: int) -> int:
    acc = 0
    i = 0
    while i < n:
        acc = acc + clamp(i, 2, 7)
        i = i + 1
    return acc

print(total(12))
print(clamp(-5, 0, 10))
print(clamp(50, 0, 10))
