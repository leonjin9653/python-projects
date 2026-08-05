import math

def pi_mandelbrot(epsilon):
    c = complex(-0.75, epsilon)
    z = 0
    n = 0
    while abs(z) <= 2 and n < max_iter:
        z = z * z + c
        n += 1
    return epsilon * n

eps = 0.000001 #the smaller the epsilon, the more precise the computation, but it'll also take much much longer. 
max_iter = 100000000000000000
pi_approx = pi_mandelbrot(eps)
print(f"π ≈ {pi_approx}")
print(f"Actual π = {math.pi}")