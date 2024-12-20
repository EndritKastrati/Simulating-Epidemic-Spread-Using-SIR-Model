from adaptive_rk import backward_euler_sir  # Import Backward Euler
from sir_model import sir_derivatives

def solve_sir(S0, I0, R0, beta, gamma, t_max, step_size):
    """
    Solve the SIR model using the Backward Euler solver.

    Parameters:
        S0, I0, R0 (float): Initial values for Susceptible, Infected, and Recovered.
        beta (float): Infection rate.
        gamma (float): Recovery rate.
        t_max (float): Maximum simulation time.
        step_size (float): Fixed step size for integration.

    Returns:
        np.array: Array of results with time and state variables [t, S, I, R].
    """
    print(f"solve_sir called with S0={S0}, I0={I0}, R0={R0}, beta={beta}, gamma={gamma}, t_max={t_max}, step_size={step_size}")

    # Ensure the initial infected count is meaningful
    N = S0 + I0 + R0
    if I0 < 1:
        I0 = max(1, 0.001 * N)  # Set minimum infected to 0.1% of the population
        print(f"Adjusted initial infected count to {I0} for numerical stability.")

    # Call Backward Euler Solver
    try:
        results = backward_euler_sir(S0, I0, R0, beta, gamma, t_max, step_size)
        print(f"Solver completed successfully. First 5 results:\n{results[:5]}")
        return results
    except Exception as e:
        print(f"Error in Backward Euler SIR Solver: {e}")
        raise
