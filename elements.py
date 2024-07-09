import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from constants import subshell_capacity, subshell_order, category_colors, subshell_colors

# Load atomic masses from CSV file
atomic_masses = pd.read_csv('atomic_masses.csv')

# region Atomic Structure

# Function to get the electron configuration
def get_electron_configuration(atomic_number):
    electrons = atomic_number
    configuration = []

    for n, subshell in subshell_order:
        capacity = subshell_capacity[subshell]
        if electrons >= capacity:
            configuration.append((n, subshell, capacity))
            electrons -= capacity
        else:
            configuration.append((n, subshell, electrons))
            break

    return configuration

# Function to show atom structure
def show_atom_structure(_element):
    symbol = _element["Symbol"]
    name = _element["Name"]
    atomic_number = _element["AtomicNumber"]

    # Retrieve the actual atomic mass
    atomic_mass = atomic_masses[atomic_masses["AtomicNumber"] == atomic_number]["AtomicMass"].values[0]

    # Calculate number of protons and neutrons
    protons = atomic_number
    neutrons = int(round(atomic_mass - protons))
    electrons = atomic_number

    # Get the electron configuration
    electron_config = get_electron_configuration(atomic_number)

    # Create a new window for the atom structure
    window = tk.Toplevel(root)
    window.title(f"Electron Configuration of {name} ({symbol})")

    # Create a figure for the atom structure
    _fig = plt.figure(figsize=(14, 8))
    _ax = _fig.add_axes((0.05, 0.1, 0.5, 0.8))  # Position the atom model on the left half
    ax_particle_table = _fig.add_axes((0.6, 0.6, 0.35, 0.3))  # Position the particle table on the right half
    ax_table = _fig.add_axes((0.6, 0.1, 0.35, 0.4))  # Position the electron configuration table below the particle table

    # Draw the nucleus
    _ax.plot(0, 0, 'o', markersize=20, color='orange')

    # Draw the electron shells and subshells
    shell_positions = {}
    for n, subshell, count in electron_config:
        if n not in shell_positions:
            shell_positions[n] = {}
        shell_positions[n][subshell] = count

    max_n = max(shell_positions.keys())
    for n in range(1, max_n + 1):
        if n in shell_positions:
            subshells = shell_positions[n]
            total_electrons = sum(subshells.values())
            radius = n
            if total_electrons == 0:
                angle_step = 0
            else:
                angle_step = 2 * np.pi / total_electrons
            current_angle = 0

            # Draw orbit lines
            circle = plt.Circle((0, 0), radius, color='gray', fill=False, linestyle='--')
            _ax.add_artist(circle)

            for subshell, count in subshells.items():
                _color = subshell_colors[subshell]  # Get the color for the current subshell
                for _ in range(count):
                    x = radius * np.cos(current_angle)
                    y = radius * np.sin(current_angle)
                    _ax.plot(x, y, 'o', markersize=5, color=_color, label=f'{n}{subshell}')
                    current_angle += angle_step

    # Set plot limits and title
    _ax.set_xlim(-max_n - 1, max_n + 1)
    _ax.set_ylim(-max_n - 1, max_n + 1)
    _ax.set_aspect('equal', 'box')
    _ax.axis('off')
    _ax.set_title(f'Electron configuration of {name} ({symbol})\nAtomic Number: {atomic_number}\nAtomic Mass: {atomic_mass}')

    # Create proton, neutron, electron table
    particle_data = [['Protons', protons], ['Neutrons', neutrons], ['Electrons', electrons]]
    ax_particle_table.axis('tight')
    ax_particle_table.axis('off')
    particle_table = ax_particle_table.table(cellText=particle_data, colLabels=["Particle", "Count"], cellLoc='center',
                                             loc='center')
    particle_table.auto_set_font_size(False)
    particle_table.set_fontsize(10)
    particle_table.scale(1.2, 1.2)

    # Create electron configuration table
    table_data = [(n, subshell, count) for n, subshell, count in electron_config]
    column_labels = ["Shell", "Subshell", "Electrons"]
    ax_table.axis('tight')
    ax_table.axis('off')
    table = ax_table.table(cellText=table_data, colLabels=column_labels, cellLoc='center', loc='center')
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1.2, 1.2)

    # Embed the plot in the tkinter window
    canvas = FigureCanvasTkAgg(_fig, master=window)
    canvas.draw()
    canvas.get_tk_widget().pack()

    # Close button
    close_button = tk.Button(window, text="Close", command=window.destroy)
    close_button.pack()

    # Make sure the window is updated
    window.update_idletasks()
    window.mainloop()

# endregion

# region Table of Elements

# Create a DataFrame
df = pd.read_csv('elements.csv')

# Create the main Tkinter window
root = tk.Tk()
root.withdraw()  # Hide the root window

# Create a figure and axis for the periodic table
fig, ax = plt.subplots(figsize=(18, 10))
fig.canvas.manager.set_window_title('Periodic Table of Elements')

# Plot each element with the appropriate color
for _, element in df.iterrows():
    color = category_colors[element["Category"]]
    if element["Category"] in ["Lanthanide", "Actinide"]:
        y_pos = 9 if element["Category"] == "Lanthanide" else 10
        x_pos = element["AtomicNumber"] - (57 if element["Category"] == "Lanthanide" else 89) + 3
    else:
        y_pos = element["Period"]
        x_pos = element["Group"]

    # Draw the bounding box
    bbox = plt.Rectangle((x_pos - 0.5, y_pos - 0.5), 1, 1, color=color, ec='black', lw=1, picker=True, gid=element["AtomicNumber"])
    ax.add_patch(bbox)

    # Atomic number
    ax.text(x_pos, y_pos - 0.3, str(element['AtomicNumber']),
            ha='center', va='center', fontsize=10, fontweight='bold', color='black')

    # Symbol
    ax.text(x_pos, y_pos, element['Symbol'],
            ha='center', va='center', fontsize=14, fontweight='bold', color='black')

    # Name
    ax.text(x_pos, y_pos + 0.3, element['Name'],
            ha='center', va='center', fontsize=8, color='black')

# Add placeholders for lanthanides and actinides
ax.add_patch(plt.Rectangle((2.5, 5.5), 1, 1, color=category_colors["Lanthanide"], ec='black', lw=1))
ax.text(3, 6, "Lanthanides\n(57-71)", ha='center', va='center', fontsize=8, fontweight='normal', color='black')

ax.add_patch(plt.Rectangle((2.5, 6.5), 1, 1, color=category_colors["Actinide"], ec='black', lw=1))
ax.text(3, 7, "Actinides\n(89-103)", ha='center', va='center', fontsize=8, fontweight='normal', color='black')

# Set axis limits
ax.set_xlim(0.5, 18.5)
ax.set_ylim(10.5, 0.5)

# Set axis labels
ax.set_xticks(range(1, 19))
ax.set_yticks(range(1, 11))
ax.set_xticklabels(range(1, 19))
ax.set_yticklabels(list(range(1, 8)) + ["", "L", "A"])

# Set axis titles
ax.set_xlabel('Group')
ax.set_ylabel('Period')
ax.set_title('Periodic Table of Elements')

# Remove grid lines
ax.grid(False)

# Add legend
legend_elements = [plt.Line2D([0], [0], marker='s', color='w', markerfacecolor=color, markersize=15,
                              label=category) for category, color in category_colors.items()]
plt.legend(handles=legend_elements, loc='upper left', bbox_to_anchor=(1, 0.8), title="Categories")

# Event handling for clicks
def onpick(event):
    if isinstance(event.artist, plt.Rectangle):
        gid = event.artist.get_gid()
        if gid is not None:
            _element = df[df["AtomicNumber"] == gid].iloc[0]
            show_atom_structure(_element)

# Event to close the Tkinter application when the figure is closed
# noinspection PyUnusedLocal
def on_close(event):
    plt.close(fig)
    root.destroy()

fig.canvas.mpl_connect('pick_event', onpick)
fig.canvas.mpl_connect('close_event', on_close)

# Show the plot
plt.tight_layout(rect=(0, 0, 0.98, 1))  # Adjust the layout to make room for the legend
plt.show()

# endregion
