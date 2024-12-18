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



def start_simulation():
    

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