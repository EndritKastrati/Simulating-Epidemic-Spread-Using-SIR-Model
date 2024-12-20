import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib

matplotlib.use('TkAgg')
from sir_solver import solve_sir  # Import the solver function
import threading

# Create the main application window
root = tk.Tk()
root.title("Epidemic Simulation - SIR Model")
root.geometry("900x700")  # Set the window size

# ---- Left Panel for Inputs ----
input_frame = tk.Frame(root, width=200, padx=10, pady=10)
input_frame.pack(side=tk.LEFT, fill=tk.Y)

# Add input fields
tk.Label(input_frame, text="Population Size:").pack(anchor="w")
population_entry = tk.Entry(input_frame)
population_entry.pack(fill=tk.X, pady=5)

tk.Label(input_frame, text="Initially Infected:").pack(anchor="w")
infected_entry = tk.Entry(input_frame)
infected_entry.pack(fill=tk.X, pady=5)

tk.Label(input_frame, text="Transmission Rate (Beta):").pack(anchor="w")
beta_entry = tk.Entry(input_frame)
beta_entry.pack(fill=tk.X, pady=5)

tk.Label(input_frame, text="Recovery Rate (Gamma):").pack(anchor="w")
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

fig, ax = plt.subplots()
canvas = FigureCanvasTkAgg(fig, master=graph_frame)
canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
animation = None

# Variables for stopping the simulation
stop_event = threading.Event()


def validate_inputs():
    """Validates the user inputs and returns them as a dictionary."""
    try:
        population = int(population_entry.get())
        initial_infected = int(infected_entry.get())
        beta = float(beta_entry.get())
        gamma = float(gamma_entry.get())

        # Logical checks
        if population <= 0 or initial_infected < 0 or initial_infected > population:
            raise ValueError("Invalid population or infected values.")
        if beta <= 0 or gamma <= 0:
            raise ValueError("Beta and Gamma must be positive.")

        return {
            "population": population,
            "initial_infected": initial_infected,
            "beta": beta,
            "gamma": gamma,
        }
    except ValueError as e:
        messagebox.showerror("Input Error", str(e))
        return None


def start_simulation():
    """Starts the SIR simulation."""
    inputs = validate_inputs()
    if not inputs:
        return  # Invalid inputs; stop execution

    stop_event.clear()  # Reset stop event
    ax.clear()  # Clear the graph

    def run_simulation():
        try:
            population = inputs["population"]
            initial_infected = inputs["initial_infected"]
            beta = inputs["beta"]
            gamma = inputs["gamma"]

            # Prepare initial conditions
            S0 = population - initial_infected
            I0 = initial_infected
            R0 = 0
            t_max = 50  # Simulation runs for 50 time units
            tol = 1e-8  # Tolerance for solving equations

            # Solve the SIR model
            results = solve_sir(S0, I0, R0, beta, gamma, t_max, tol)
            if results.shape[0] == 0:
                raise ValueError("No results to plot.")

            # Unpack results
            t_values = results[:, 0]  # Time values
            s_values = results[:, 1]  # Proportion of susceptible
            i_values = results[:, 2]  # Proportion of infected
            r_values = results[:, 3]  # Proportion of recovered

            # Initialize previous values for stability check
            prev_s = s_values[0]
            prev_i = i_values[0]
            prev_r = r_values[0]
            epsilon = 1e-6  # Tolerance for stability check
            stabilization_time = None  # To store the time of stabilization

            # Update the graph dynamically
            def update(frame):
                nonlocal prev_s, prev_i, prev_r, stabilization_time

                # Check for stability (values stop changing significantly)
                if frame > 0:
                    delta_s = abs(s_values[frame] - prev_s)
                    delta_i = abs(i_values[frame] - prev_i)
                    delta_r = abs(r_values[frame] - prev_r)

                    if delta_s < epsilon and delta_i < epsilon and delta_r < epsilon:
                        stabilization_time = t_values[frame]  # Store stabilization time
                        animation.event_source.stop()  # Stop the animation
                        # Adjust the x-axis dynamically to end at the stabilization time
                        ax.set_xlim(0, stabilization_time)
                        canvas.draw()  # Redraw the canvas with updated limits
                        return

                    # Update previous values
                    prev_s = s_values[frame]
                    prev_i = i_values[frame]
                    prev_r = r_values[frame]

                # Plot the data
                ax.clear()
                ax.plot(
                    t_values[:frame],
                    s_values[:frame] * population,
                    label="Susceptible",
                    color='blue'
                )
                ax.plot(
                    t_values[:frame],
                    i_values[:frame] * population,
                    label="Infected",
                    color='red'
                )
                ax.plot(
                    t_values[:frame],
                    r_values[:frame] * population,
                    label="Recovered",
                    color='green'
                )
                ax.set_title("SIR Model Simulation")
                ax.set_xlabel("Time (days)")
                ax.set_ylabel("Population")
                ax.set_xlim(0, t_max)  # Ensure x-axis covers the full simulation period initially
                ax.set_ylim(0, population)  # Set y-axis to total population size
                ax.legend()

            # Run animation
            global animation
            animation = FuncAnimation(fig, update, frames=len(t_values), interval=50, repeat=False)
            canvas.draw()

        except Exception as e:
            messagebox.showerror("Simulation Error", f"An error occurred: {e}")

    # Run the simulation in a separate thread
    threading.Thread(target=run_simulation).start()


def stop_simulation():
    """Stops the simulation."""
    global animation
    if animation:
        animation.event_source.stop()
    stop_event.set()


# Link buttons to their respective functions
start_button.config(command=start_simulation)
stop_button.config(command=stop_simulation)

# Start the main loop
root.mainloop()
