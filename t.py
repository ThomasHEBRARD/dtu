def divide(dividend, divisor):
    result = divisor
    c = 0
    while result > dividend:
        result -= dividend
        c += 1
    return c


print(divide(3, 10))
