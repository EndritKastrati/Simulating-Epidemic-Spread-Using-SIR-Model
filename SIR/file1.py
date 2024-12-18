import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import threading
import matplotlib
matplotlib.use('TkAgg')

from sir_solver import solve_sir  

# Krijimi i window/dritares kryesore
root = tk.Tk()
root.title("Epidemic Simulation - SIR Model")
root.geometry("900x700")  

# ---- Vendi i inputave ----
input_frame = tk.Frame(root, width=200, padx=10, pady=10)
input_frame.pack(side=tk.LEFT, fill=tk.Y)

# Inputat:
tk.Label(input_frame, text="Numri i Popullsise:").pack(anchor="w")
population_entry = tk.Entry(input_frame)
population_entry.pack(fill=tk.X, pady=5)

tk.Label(input_frame, text="Te Infektuar:").pack(anchor="w")
infected_entry = tk.Entry(input_frame)
infected_entry.pack(fill=tk.X, pady=5)

tk.Label(input_frame, text="Transmission Rate (Beta):").pack(anchor="w")
beta_entry = tk.Entry(input_frame)
beta_entry.pack(fill=tk.X, pady=5)

tk.Label(input_frame, text="Recovery Rate (Gamma):").pack(anchor="w")
gamma_entry = tk.Entry(input_frame)
gamma_entry.pack(fill=tk.X, pady=5)

# Butonat:
button_frame = tk.Frame(input_frame)
button_frame.pack(pady=20)

start_button = tk.Button(button_frame, text="Start", bg="blue", fg="white", width=10)
start_button.pack(side=tk.LEFT, padx=5)

stop_button = tk.Button(button_frame, text="Stop", bg="red", fg="white", width=10)
stop_button.pack(side=tk.LEFT, padx=5)

# ---- Paneli kryesor ku ka mu shfaq grafi dhe stimulimi ----
main_frame = tk.Frame(root, padx=10, pady=10)
main_frame.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH)

# Display i grafit:
graph_frame = tk.Frame(main_frame)
graph_frame.pack(fill=tk.BOTH, expand=True)

fig, ax = plt.subplots()
canvas = FigureCanvasTkAgg(fig, master=graph_frame)
canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
animation = None

stop_event = threading.Event()

def validate_inputs():
    """Validates the user inputs and returns them as a dictionary."""
      
    try:
        population = int(population_entry.get())
        initial_infected = int(infected_entry.get())
        beta = float(beta_entry.get())
        gamma = float(gamma_entry.get())
    
        # Logjika
        if population <= 0 or initial_infected < 0 or initial_infected > population:
            raise ValueError("Vlera jo-valide ne lidhje me numrin e popullsise ose te infektuarve.")
        if beta <= 0 or gamma <= 0:
            raise ValueError("Beta dhe Gamma duhet te jene pozitive.")


            return {
            "population": population,
            "initial_infected": initial_infected,
            "beta": beta,
            "gamma": gamma,
        }
    except ValueError as e:
        messagebox.showerror("Vlera Jo-Valide", str(e))
        return None
    

def start_simulation():

    """Starts the SIR simulation."""

    inputs = validate_inputs()
    if not inputs:
        return  
    

    stop_event.clear()  
    ax.clear()  

    def run_simulation():
        try:
            population = inputs["population"]
            initial_infected = inputs["initial_infected"]
            beta = inputs["beta"]
            gamma = inputs["gamma"]

            S0 = population - initial_infected
            I0 = initial_infected
            R0 = 0
            t_max = 10000
            tol = 1e-1

            results = solve_sir(S0, I0, R0, beta, gamma, t_max, tol)

            t_values = results[:, 0]  
            s_values = results[:, 1]  
            i_values = results[:, 2]  
            r_values = results[:, 3]  
        
            def update(frame):
                ax.clear()
                ax.plot(t_values[:frame], s_values[:frame], label="Susceptible", color='blue')
                ax.plot(t_values[:frame], i_values[:frame], label="Infektuar", color='red')
                ax.plot(t_values[:frame], r_values[:frame], label="Sheruar", color='green')
                ax.set_title("SIR Model")
                ax.set_xlabel("Koha")
                ax.set_ylabel("Popullsia")
                ax.legend()

            global animation
            animation = FuncAnimation(fig, update, frames=len(t_values), interval=50, repeat=False)
            canvas.draw()

        except Exception as e:
            messagebox.showerror("Error", f"U shfaq nje error: {e}")
    
    threading.Thread(target=run_simulation).start()



def stop_simulation():
    """Stops the simulation."""
    global animation
    if animation:
        animation.event_source.stop()
        stop_event.set()


# Lidhja e butonava me funksionet e tyre
start_button.config(command=start_simulation)
stop_button.config(command=stop_simulation)


root.mainloop()