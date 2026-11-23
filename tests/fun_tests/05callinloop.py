from runtime import input_int

def double(x: int) -> int:
    return x + x

n = input_int()
acc = 0
while n > 0:
    acc = acc + double(n)
    n = n - 1
print(acc)
