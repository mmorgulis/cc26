def fib(n: int) -> int:
    if n < 2:
        return n
    else:
        x = fib(n - 1)
        y = fib(n - 2)
        z = y + x
        return z

print(fib(20))
