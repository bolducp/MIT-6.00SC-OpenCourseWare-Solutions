#Problem Set 2, Problem 2

def compute_deriv(poly):
    deriv = []
    for num in poly:
        exponent = poly.index(num)
        if exponent <= 0:
            continue
        elif exponent == 1:
            deriv.append(0.0)
        else:
            deriv.append(exponent * num)
    return tuple(deriv)


