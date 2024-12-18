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


def sir_derivative_i(S, I, gamma, beta):
    """
    Calculate dI/dt for the SIR model.
    Parameters:
        S (float): Susceptible population fraction.
        I (float): Infected population fraction.
        gamma (float): Recovery rate.
        beta (float): Infection rate.
    Returns:
        float: dI/dt.
    """
    return beta * S * I - gamma * I


def sir_derivative_r(I, gamma):
    """
    Calculate dR/dt for the SIR model.
    Parameters:
        I (float): Infected population fraction.
        gamma (float): Recovery rate.
    Returns:
        float: dR/dt.
    """
    return gamma * I


def sir_derivatives(y, params):
    """
    Derivative function for the SIR model.
    Parameters:
        y (list or np.array): Current values of [S, I, R].
        params (dict): Dictionary containing model parameters (beta, gamma).
    Returns:
        list: Derivatives [dS/dt, dI/dt, dR/dt].
    """
    S, I, R = y
    beta = params['beta']
    gamma = params['gamma']
    dS = sir_derivative_s(S, I, beta)
    dI = sir_derivative_i(S, I, gamma, beta)
    dR = sir_derivative_r(I, gamma)
    return [dS, dI, dR]