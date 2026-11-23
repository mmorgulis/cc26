def f(x: int) -> int:
    y = x + 1
    return y * 2

def g(x: int) -> int:
    y = x + 100
    return y * 3

x = 5
y = f(x) + g(x)
print(y)
print(f(1))
print(g(1))
