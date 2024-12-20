from SIR.sir_solver import solve_sir


def calculate_epidemic_duration(S0, I0, R0, beta, gamma, step_size=1.0, tol=1e-6):
    """
    Calculate the duration of the epidemic based on SIR parameters.

    Parameters:
        S0, I0, R0 (float): Initial values for Susceptible, Infected, and Recovered.
        beta (float): Transmission rate.
        gamma (float): Recovery rate.
        step_size (float): Step size for numerical solver.
        tol (float): Threshold below which the epidemic is considered over.

    Returns:
        float: Duration of the epidemic in days.
    """
    # Solve the SIR model using the existing solver
    results = solve_sir(S0, I0, R0, beta, gamma, t_max=5000, step_size=step_size)
    t_values = results[:, 0]  # Time points
    i_values = results[:, 2]  # Infected population

    # Find the time when infected population approaches zero
    for t, I in zip(t_values, i_values):
        if I <= tol:  # Check if infected population falls below threshold
            return t  # Return the time (duration)

    # If the epidemic never fully resolves within t_max
    return t_values[-1]