import numpy as np

def backward_euler_sir(S0, I0, R0, beta, gamma, t_max, step_size, tol=1e-6, max_iter=20):
    """
    Solve the SIR model using the Backward Euler method with Newton-Raphson iteration.

    Parameters:
        S0, I0, R0 (float): Initial values for Susceptible, Infected, and Recovered.
        beta (float): Infection rate.
        gamma (float): Recovery rate.
        t_max (float): Maximum simulation time.
        step_size (float): Step size for time discretization.
        tol (float): Convergence tolerance for Newton-Raphson.
        max_iter (int): Maximum iterations for Newton-Raphson.

    Returns:
        np.array: Array of results [time, S, I, R].
    """
    t_values = [0]
    S, I, R = S0, I0, R0
    results = [[0, S, I, R]]

    t = 0
    while t < t_max:
        # Stop condition when infected population is effectively zero
        if I < 1e-6:
            print(f"Stopping simulation at t={t:.2f} as I < 1e-6")
            break

        # Initialize guesses for next step
        S_next, I_next, R_next = S, I, R

        # Newton-Raphson iteration
        for _ in range(max_iter):
            # Residuals
            f1 = S_next - S + step_size * beta * S_next * I_next / (S + I + R)
            f2 = I_next - I - step_size * (beta * S_next * I_next / (S + I + R) - gamma * I_next)
            f3 = R_next - R - step_size * gamma * I_next

            # Check for convergence
            if max(abs(f1), abs(f2), abs(f3)) < tol:
                break

            # Jacobian matrix components
            J11 = 1 + step_size * beta * I_next / (S + I + R)
            J12 = step_size * beta * S_next / (S + I + R)
            J21 = -step_size * beta * I_next / (S + I + R)
            J22 = 1 + step_size * (beta * S_next / (S + I + R) - gamma)

            # Newton step corrections
            delta_S = -f1 / J11
            delta_I = -f2 / J22
            delta_R = -f3

            # Update guesses
            S_next += delta_S
            I_next += delta_I
            R_next += delta_R

            # Ensure non-negativity
            S_next = max(S_next, 0)
            I_next = max(I_next, 0)
            R_next = max(R_next, 0)

        else:
            print(f"Warning: Newton-Raphson did not converge at time t={t:.2f}")
            break

        # Update state variables
        S, I, R = S_next, I_next, R_next
        t += step_size
        t_values.append(t)
        results.append([t, S, I, R])

    return np.array(results)
