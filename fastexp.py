def fastexp(x, n):
    if n == 0:
        return 1
    elif n % 2 == 0:
        return fastexp(x*x, n/2)
    else:
        return x * fastexp(x, n-1)
