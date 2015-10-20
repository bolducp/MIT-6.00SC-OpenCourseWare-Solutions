from solutions.ps2_newton_sol1 import evaluate_poly, compute_deriv


def compute_root(poly, x_0, epsilon):

    guess = x_0
    counter = 1
    while abs(evaluate_poly(poly, guess)) >= epsilon:
        guess = guess - evaluate_poly(poly, guess) / evaluate_poly(compute_deriv(poly), guess)
        counter += 1

    return (guess, counter)

