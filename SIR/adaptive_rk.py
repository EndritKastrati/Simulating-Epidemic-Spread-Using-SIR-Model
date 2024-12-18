import numpy as np


def adaptive_rk(f, y0, t_max, tol, params):
    """
    General solver using an adaptive Runge-Kutta method.

    Parameters:
        f (function): Function to compute derivatives. Must take (y, params) as arguments.
        y0 (list or np.array): Initial state values.
        t_max (float): Maximum simulation time.
        tol (float): Tolerance for error.
        params (dict): Additional parameters required by the derivative function.

    Returns:
        np.array: Array of results with time and state variables.
    """

    print(f"adaptive_rk called with y0={y0}, t_max={t_max}, tol={tol}, params={params}")

    t = 0
    h = 0.1  # Initial step size
    y = np.array(y0)
    results = [(t, *y)]

    while t < t_max:
        # Compute derivatives using the function f
        k1 = np.array(f(y, params))
        k2 = np.array(f(y + h * k1 / 2, params))

        # RK2 step (low-order)
        y_half = y + h * k1 / 2

        # RK4 step (high-order)
        y_next = y + h * k2

        # Estimate error
        error = np.max(np.abs(y_next - y_half))

        # Adjust step size
        if error > tol:
            h /= 2  # Reduce step size
        else:
            t += h
            y = y_next
            results.append((t, *y))
            if error < tol / 2:
                h *= 2  # Increase step size if error is small

    return np.array(results)