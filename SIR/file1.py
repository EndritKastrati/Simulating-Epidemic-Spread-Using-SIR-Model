import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
import numpy as np
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
    global day_label_obj  # Ensure day_label_obj is reset
    day_label_obj = None

    inputs = validate_inputs()
    if not inputs:
        return  # Invalid inputs; stop execution

    stop_event.clear()  # Reset stop event
    ax.clear()  # Clear the graph


    def run_simulation():
        try:
            population = inputs["population"]
            initial_infected = max(inputs["initial_infected"], 1)
            beta = inputs["beta"]
            gamma = inputs["gamma"]

            # Use raw initial conditions
            S0 = population - initial_infected
            I0 = initial_infected
            R0 = 0

            # Adjust step size and t_max for more detailed results
            results = solve_sir(S0, I0, R0, beta, gamma, t_max=10000, step_size=0.1)

            # Extract results
            t_values = results[:, 0]
            s_values = results[:, 1]
            i_values = results[:, 2]
            r_values = results[:, 3]

            # Persistent label for the current day
            day_label_obj = fig.text(0.8, 0.95, "", fontsize=10, verticalalignment='top',
                                     bbox=dict(boxstyle="round", facecolor='white', edgecolor='0.8'))

            def update(frame):
                global day_label_obj # Access the global label object

                # Compute the actual frame index based on the skipping factor
                actual_frame = frame * frame_skip
                if actual_frame >= len(t_values):  # Ensure we don't exceed the data length
                    actual_frame = len(t_values) - 1

                # Stop the simulation when the infected population is near zero
                if i_values[actual_frame] <= 0.9 or actual_frame == len(t_values) - 1:
                    animation.event_source.stop()
                    print(
                        f"Simulation stopped: Infected population reached near zero at day {t_values[actual_frame]:.2f}.")
                    ax.set_xlim(0, t_values[actual_frame])  # Set the final x-axis range
                    canvas.draw()
                    return

                # Clear the plot and update with current frame data
                ax.clear()
                ax.plot(t_values[:actual_frame + 1], s_values[:actual_frame + 1], label="Susceptible", color='blue')
                ax.plot(t_values[:actual_frame + 1], i_values[:actual_frame + 1], label="Infected", color='red')
                ax.plot(t_values[:actual_frame + 1], r_values[:actual_frame + 1], label="Recovered", color='green')

                # Update the day label dynamically
                if day_label_obj is not None:
                    day_label_obj.set_text(f"Day: {t_values[actual_frame]:.0f}")  # Update existing label
                else:
                    # Create a new label if it doesn't exist
                    day_label_obj = fig.text(0.8, 0.95, f"Day: {t_values[actual_frame]:.0f}", fontsize=10,
                                             verticalalignment='top',
                                             bbox=dict(boxstyle="round", facecolor='white', edgecolor='0.8'))

                # Dynamically set the x-axis limits
                safe_xlim = max(np.max(t_values[:actual_frame + 1]), 1)  # Ensure a valid range
                ax.set_xlim(0, safe_xlim)

                # Set y-axis and graph labels
                ax.set_ylim(0, population)
                ax.set_title("SIR Model Simulation")
                ax.set_xlabel("Time (days)")
                ax.set_ylabel("Population")
                ax.legend()
                canvas.draw()

            # Define the frame skipping factor
            frame_skip = 4  # Skip every 4th frame

            # Initialize the animation with frame skipping
            global animation
            frames = range(0, (len(t_values) + frame_skip - 1) // frame_skip)
            animation = FuncAnimation(fig, update, frames=frames, interval=10, repeat=False)
            canvas.draw()

        except Exception as e:
            messagebox.showerror("Simulation Error", f"An error occurred: {e}")

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
