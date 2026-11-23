def is_even(n: int) -> int:
    if n == 0:
        return 1
    else:
        return is_odd(n - 1)

def is_odd(n: int) -> int:
    if n == 0:
        return 0
    else:
        return is_even(n - 1)

print(is_even(10))
print(is_odd(10))
print(is_even(7))
