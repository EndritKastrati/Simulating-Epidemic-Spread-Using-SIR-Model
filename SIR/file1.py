import tkinter as tk
from tkinter import ttk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Create the main application window
root = tk.Tk()
root.title("Epidemic Simulation - SIR Model")
root.geometry("900x700")  # Set the window size

# ---- Left Panel for Inputs ----
input_frame = tk.Frame(root, width=200, padx=10, pady=10)
input_frame.pack(side=tk.LEFT, fill=tk.Y)

# Add input fields
tk.Label(input_frame, text="Numri i Popullsise:").pack(anchor="w")
population_entry = tk.Entry(input_frame)
population_entry.pack(fill=tk.X, pady=5)

tk.Label(input_frame, text="Sa Jane te Infektuar:").pack(anchor="w")
infected_entry = tk.Entry(input_frame)
infected_entry.pack(fill=tk.X, pady=5)

tk.Label(input_frame, text="Shperndarja (Beta):").pack(anchor="w")
beta_entry = tk.Entry(input_frame)
beta_entry.pack(fill=tk.X, pady=5)

tk.Label(input_frame, text="Sherimi (Gamma):").pack(anchor="w")
gamma_entry = tk.Entry(input_frame)
gamma_entry.pack(fill=tk.X, pady=5)

# Add buttons
button_frame = tk.Frame(input_frame)
button_frame.pack(pady=20)

start_button = tk.Button(button_frame, text="Start", bg="blue", fg="white", width=10)
start_button.pack(side=tk.LEFT, padx=5)

stop_button = tk.Button(button_frame, text="Stop", bg="red", fg="white", width=10)
stop_button.pack(side=tk.LEFT, padx=5)

# ---- Main Panel for Simulation and Graphs ----
main_frame = tk.Frame(root, padx=10, pady=10)
main_frame.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH)

# Graph display
graph_frame = tk.Frame(main_frame)
graph_frame.pack(fill=tk.BOTH, expand=True)

canvas = None
animation = None  # Variable to store the animation instance


# ---- Functionality for SIR Model ----
def sir_model(population, initial_infected, beta, gamma, max_steps=1000):
    """
    Generator function for simulating the SIR model dynamics in real-time.

        Args:
            population: Total population size.
            initial_infected: Initial number of infected individuals.
            beta: Transmission rate.
            gamma: Recovery rate.
            max_steps: Maximum number of simulation steps.

        Yields:
            step: Current time step.
            S, I, R: Current values of susceptible, infected, and recovered.
    """
    S = population - initial_infected
    I = initial_infected
    R = 0

    for step in range(max_steps):
        dS = -beta * S * I / population
        dI = beta * S * I / population - gamma * I
        dR = gamma * I

        S = max(S + dS, 0)
        I = max(I + dI, 0)
        R = max(R + dR, 0)

        yield step, S, I, R

        if I <= 0:  # Stop when no more infected individuals
            break

def start_simulation():
    """Starts the SIR simulation and updates the graph dynamically."""
    # Get user inputs
    try:
        population = int(population_entry.get())
        initial_infected = int(infected_entry.get())
        beta = float(beta_entry.get())
        gamma = float(gamma_entry.get())
    except ValueError:
        print("Error: Invalid input values!")
        return

    # Clear previous canvas
    global canvas, animation
    if canvas:
        canvas.get_tk_widget().destroy()
    if animation:
        animation.event_source.stop()

    # Create the figure
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.set_xlim(0, 100)  # Start with 100 steps and dynamically adjust later
    ax.set_ylim(0, population)
    ax.set_title("SIR Model Dynamics")
    ax.set_xlabel("Time")
    ax.set_ylabel("Population")
    ax.grid()

    line_S, = ax.plot([], [], label="Susceptible", color="blue")
    line_I, = ax.plot([], [], label="Infected", color="red")
    line_R, = ax.plot([], [], label="Recovered", color="green")
    ax.legend()

    time_data = []
    S_data = []
    I_data = []
    R_data = []

    # Generator for real-time SIR model updates
    sir_gen = sir_model(population, initial_infected, beta, gamma)

    # Animation update function
    def update(frame):
        step, S, I, R = next(sir_gen)

        # Append data
        time_data.append(step)
        S_data.append(S)
        I_data.append(I)
        R_data.append(R)

        # Update data
        line_S.set_data(time_data, S_data)
        line_I.set_data(time_data, I_data)
        line_R.set_data(time_data, R_data)

        # Dynamically adjust the x-axis if the time exceeds the current limit
        if step >= ax.get_xlim()[1]:
            ax.set_xlim(0, step + 50)

        return line_S, line_I, line_R

    # Create animation
    animation = FuncAnimation(fig, update, interval=100, blit=True, save_count=1000)

    # Embed the animated plot in Tkinter
    canvas = FigureCanvasTkAgg(fig, master=graph_frame)
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    canvas.draw()


def stop_simulation():
    """Stops the animation."""
    global animation
    if animation:
        animation.event_source.stop()


# Link buttons to their respective functions
start_button.config(command=start_simulation)
stop_button.config(command=stop_simulation)

# Start the main loop
root.mainloop()