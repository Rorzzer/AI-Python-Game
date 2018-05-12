from timeit import timeit

num = 100000
x = 7


def between(value, low, high):
    return value >= low and value < high


print(timeit('x in range(0,8)', 'x=5', number=num) * num)
print(timeit('between(x,0,8)', """
x=5

def between(value, low, high):
    return value >= low and value < high

""", number=num) * num)

print(timeit('0<=x<8', 'x=5', number=num) * num)

# findings = between is much faster than in range