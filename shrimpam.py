import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.colors import LinearSegmentedColormap

# Set up figure with black background
fig = plt.figure(figsize=(9, 9), facecolor='black')
ax = fig.add_axes([0, 0, 1, 1], facecolor='black')  # Full figure coverage
ax.set_xlim(0, 400)
ax.set_ylim(0, 400)
ax.set_axis_off()  # Hide axes

# Create custom colormap (blue to magenta to yellow)
colors = [(0, 0.5, 1), (0.8, 0, 0.8), (1, 1, 0)]
cmap = LinearSegmentedColormap.from_list("custom", colors)

# Initialize particles
i = np.arange(0, 10001)  # 0 to 1e4
x = i
y = i / 235
e = y / 8 - 13

# Create scatter plot with initial empty data
sc = ax.scatter([], [], s=2, alpha=0.4, edgecolors='none', marker='o')

t = 0
dt = np.pi / 240
total_frames = 240  # About 8 seconds at 30 FPS

def update(frame):
    global t
    t += dt
    
    k = (4 + np.sin(y * 2 - t) * 3) * np.cos(x / 29)
    d = np.sqrt(k**2 + e**2)  # vecnorm equivalent
    
    with np.errstate(divide='ignore', invalid='ignore'):
        q = 3 * np.sin(k * 2) + 0.3/k + np.sin(y/25) * k * (9 + 4 * np.sin(e*9 - d*3 + t*2))
    
    xdata = q + 30 * np.cos(d - t) + 200
    ydata = 620 - q * np.sin(d - t) - d * 39
    
    # Position-based coloring
    norm_x = (xdata - 200) / 200  # Normalize to [-1, 1]
    norm_y = (ydata - 200) / 200
    distance = np.sqrt(norm_x**2 + norm_y**2)
    angle = (np.arctan2(norm_y, norm_x) + np.pi) / (2 * np.pi)  # [0, 1]
    color_values = (distance * 0.6 + angle * 0.4) % 1.0
    
    # Update scatter plot
    sc.set_offsets(np.column_stack((xdata, ydata)))
    sc.set_array(color_values)  # For colormap mapping
    sc.set_cmap(cmap)
    
    return [sc]

# Create animation
ani = FuncAnimation(fig, update, frames=total_frames, interval=33, blit=True)

# Save as GIF
save_gif = True
if save_gif:
    print("Rendering animation...")
    ani.save('shrimpam.gif', writer='pillow', fps=30, dpi=100,
             progress_callback=lambda i, n: print(f"Frame {i}/{n}") if i % 30 == 0 else None)
    print("Animation saved as 'shrimpam.gif'")

plt.show()