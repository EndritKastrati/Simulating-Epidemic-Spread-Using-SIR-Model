def sir_derivative_s(S, I, beta):
    """
    Calculate dS/dt for the SIR model.
    Parameters:
        S (float): Susceptible population fraction.
        I (float): Infected population fraction.
        beta (float): Infection rate.
    Returns:
        float: dS/dt.
    """
    return -beta * S * I