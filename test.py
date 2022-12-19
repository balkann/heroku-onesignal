def fibonacci(n):
    return fibonacci_helper(n,1,0)

def fibonacci_helper(n, current, prev):
    if n ==1:
        print(2)
        return current
    elif n>1:
        print(1)
        return fibonacci_helper(n-1, prev + current, current)


x = fibonacci(5)
print(x)