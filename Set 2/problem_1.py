#Problem Set 2, Problem 1

def evaluate_poly(poly, x):
    total = 0
    for num in poly:
        exponent = poly.index(num)
        if exponent == 0:
            total += num
        else:
            total += num * x**exponent
    return total

