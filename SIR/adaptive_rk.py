import numpy as np

def backward_euler_sir_full(S0, I0, R0, beta, gamma, t_max, step_size, tol=1e-8, max_iter=20):
    """
    Solve the SIR model using the Backward Euler method with full Jacobian and Newton-Raphson iteration.

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
            J13 = 0

            J21 = -step_size * beta * I_next / (S + I + R)
            J22 = 1 + step_size * (beta * S_next / (S + I + R) - gamma)
            J23 = 0

            J31 = 0
            J32 = -step_size * gamma
            J33 = 1

            # Construct the Jacobian matrix and residual vector
            J = np.array([
                [J11, J12, J13],
                [J21, J22, J23],
                [J31, J32, J33]
            ])

            F = np.array([-f1, -f2, -f3])

            # Solve the linear system J * [dS, dI, dR] = -[f1, f2, f3] using Gaussian elimination
            dS, dI, dR = gaussian_elimination(J, F)

            # Update guesses
            S_next += dS
            I_next += dI
            R_next += dR

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

def gaussian_elimination(A, b):
    """
    Solve the linear system Ax = b using Gaussian elimination.

    Parameters:
        A (np.array): Coefficient matrix (Jacobian).
        b (np.array): Right-hand side vector (negative residuals).

    Returns:
        np.array: Solution vector x.
    """
    n = len(b)

    # Forward elimination
    for i in range(n):
        # Make the diagonal element 1 by dividing the row
        factor = A[i, i]
        A[i, :] /= factor
        b[i] /= factor

        # Eliminate the current column in subsequent rows
        for j in range(i + 1, n):
            factor = A[j, i]
            A[j, :] -= factor * A[i, :]
            b[j] -= factor * b[i]

    # Back substitution
    x = np.zeros_like(b)
    for i in range(n - 1, -1, -1):
        x[i] = b[i] - np.dot(A[i, i + 1:], x[i + 1:])

    return x

# Example Usage
# S0, I0, R0 = initial values; beta, gamma = infection and recovery rates; t_max = total time; step_size = time step
results = backward_euler_sir_full(S0=990, I0=10, R0=0, beta=0.3, gamma=0.1, t_max=100, step_size=0.1)
print(results)
