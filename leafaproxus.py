import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.colors import LinearSegmentedColormap

# Create radial color gradient: blue at center, red at edges
colors = [(0.2, 0.6, 1.0), (0.9, 0.1, 0.2)]  # Blue to Red
cmap = LinearSegmentedColormap.from_list("radial_gradient", colors)

# Set up figure
fig = plt.figure(figsize=(9, 9), facecolor='k')
ax = fig.add_axes([0, 0, 1, 1], facecolor='k')
ax.set_xlim(0, 400)
ax.set_ylim(0, 400)
ax.set_axis_off()

# Precompute static arrays
i = np.arange(0, 20001)
x = i % 100
y = i // 100
k = x/4 - 12.5
e = y/9 + 5
o = np.sqrt(k**2 + e**2) / 9

# Initialize scatter plot (start with empty positions)
sc = ax.scatter([], [], s=2, alpha=0.4, edgecolors='none', marker='o')

t = 0
dt = np.pi / 90
total_frames = 180  # 6 seconds at 30 FPS

def update(frame):
    global t
    t += dt
    
    with np.errstate(divide='ignore', invalid='ignore'):
        q = x + 99 + np.tan(1/k) + o * k * (np.cos(e*9)/4 + np.cos(y/2)) * np.sin(o*4 - t)
    
    c = o * e / 30 - t/8
    xdata = (q * 0.7 * np.sin(c)) + 9 * np.cos(y/19 + t) + 200
    ydata = 200 + (q/2 * np.cos(c))
    
    # Calculate distances from center for color mapping
    dist_x = (xdata - 200) / 200  # Normalized [-1, 1]
    dist_y = (ydata - 200) / 200
    distance = np.sqrt(dist_x**2 + dist_y**2)  # Radial distance
    
    # Calculate angle for secondary color effect
    angle = (np.arctan2(dist_y, dist_x) + np.pi) / (2 * np.pi)  # [0, 1]
    
    # Combine distance and angle for more interesting color patterns
    color_value = (distance * 0.7 + angle * 0.3) % 1.0
    
    # Get colors from colormap
    point_colors = cmap(color_value)
    point_colors[:, 3] = 0.4  # Set alpha to 40%
    
    # Update scatter plot
    sc.set_offsets(np.column_stack((xdata, ydata)))
    sc.set_facecolors(point_colors)
    
    return [sc]

ani = FuncAnimation(fig, update, frames=total_frames, interval=20, blit=True)

# Save as GIF
save_gif = True
if save_gif:
    print("Rendering position-colored animation...")
    ani.save('position_colored_swarm.gif', writer='pillow', fps=30, dpi=100,
             progress_callback=lambda i, n: print(f"Frame {i}/{n}") if i % 20 == 0 else None)
    print("Saved as 'position_colored_swarm.gif'")

plt.show()