import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import griddata

# File path
file_path = ''

# Parse the text file
data = []
with open(file_path, 'r') as file:
    for line in file:
        if "Force" in line:
            parts = line.strip().split(",")
            force = float(parts[0].split(":")[1].strip())
            turns = int(parts[1].split(":")[1].strip())
            length = float(parts[2].split(":")[1].strip())
            amps = float(parts[3].split(":")[1].strip())
            data.append({"Force": force, "Turns": turns, "Length": length, "Amps": amps})

# Convert data to numpy arrays
length = np.array([row["Length"] for row in data])
turns = np.array([row["Turns"] for row in data])
amps = np.array([row["Amps"] for row in data])

# Create a grid
grid_turns, grid_length = np.meshgrid(
    np.linspace(min(turns), max(turns), 100),
    np.linspace(min(length), max(length), 100)
)

# Interpolate the data to create a smooth surface
grid_amps = griddata(
    (turns, length),
    amps,
    (grid_turns, grid_length),
    method='cubic'  # Use 'linear' or 'cubic' for smooth interpolation
)

# Plot the surface
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Plot surface
surf = ax.plot_surface(grid_turns, grid_length, grid_amps, cmap='viridis', edgecolor='none')

# Add color bar
fig.colorbar(surf, ax=ax, shrink=0.5, aspect=10)

# Label axes
ax.set_xlabel('Turns')
ax.set_ylabel('Length (cm)')
ax.set_zlabel('Amps (A)')

# Title
plt.title('Smooth Blanket Structure of Amps vs Turns and Length')

# Show plot
plt.show()
