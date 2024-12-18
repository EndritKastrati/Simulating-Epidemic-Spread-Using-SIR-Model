from adaptive_rk_solver import adaptive_rk
from sir_model import sir_derivatives

def solve_sir(S0, I0, R0, beta, gamma, t_max, tol):
    """

    Solve the SIR model using the general adaptive RK solver.
    Parameters:
        S0, I0, R0 (float): Initial values for Susceptible, Infected, and Recovered.
        beta (float): Infection rate.
        gamma (float): Recovery rate.
        t_max (float): Maximum simulation time.
        tol (float): Error tolerance.
    Returns:
        np.array: Array of results with time and state variables [t, S, I, R].

    """


    y0 = [S0, I0, R0]
    params = {'beta': beta, 'gamma': gamma}
    
    return adaptive_rk(sir_derivatives, y0, t_max, tol, params)