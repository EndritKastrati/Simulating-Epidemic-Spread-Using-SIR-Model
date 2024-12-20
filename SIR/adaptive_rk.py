import numpy as np

def rkf45(f, y0, t_max, tol, params, h_max=1.0, h_min=1e-6):

    """
    Implementation of the Runge-Kutta-Fehlberg (RKF45) method for ODE solving.

    Parameters:
        f (function): Function to compute derivatives.
        y0 (list or np.array): Initial state values.
        t_max (float): Maximum simulation time.
        tol (float): Error tolerance.
        params (dict): Additional parameters for the derivative function.
        h_max (float): Maximum step size.
        h_min (float): Minimum step size.

    Returns:
        np.array: Array of results [time, state variables].
    """
    a = [0, 1/4, 3/8, 12/13, 1, 1/2]
    b = [
        [],
        [1/4],
        [3/32, 9/32],
        [1932/2197, -7200/2197, 7296/2197],
        [439/216, -8, 3680/513, -845/4104],
        [-8/27, 2, -3544/2565, 1859/4104, -11/40]
    ]
    c = [16/135, 0, 6656/12825, 28561/56430, -9/50, 2/55]
    dc = [1/360, 0, -128/4275, -2197/75240, 1/50, 2/55]

    t = 0
    h = 0.1  # Initial step size
    y = np.array(y0)
    results = [(t, *y)]

    epsilon = 1e-10  # Small number to prevent division by zero

    while t < t_max:
        if h < h_min:
            raise ValueError("Step size too small. Integration failed.")
        if t + h > t_max:
            h = t_max - t  # Adjust final step size

        k = []
        for i in range(6):
            y_temp = y + h * sum(b[i][j] * k[j] for j in range(i)) if i > 0 else y
            k.append(np.array(f(y_temp, params)))

        # Calculate the 5th-order (high-order) and 4th-order (low-order) estimates
        y5 = y + h * sum(c[j] * k[j] for j in range(6))
        y4 = y + h * sum((c[j] + dc[j]) * k[j] for j in range(6))

        # Estimate the error
        error = np.max(np.abs(y5 - y4))

        # Adjust step size
        if error > tol:
            h *= max(0.1, 0.84 * (tol / error) ** 0.25)  # Reduce step size
        else:
            t += h
            y = y5
            results.append((t, *y))
            if error < epsilon or error < tol / 10:
                h = min(h * 2, h_max)  # Increase step size conservatively


    return np.array(results)