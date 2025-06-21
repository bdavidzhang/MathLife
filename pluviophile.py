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

# Create custom colormap (blue to purple to pink)
colors = [(0.2, 0.5, 1.0), (0.7, 0.2, 0.8), (1.0, 0.5, 0.8)]
cmap = LinearSegmentedColormap.from_list("custom", colors)

# Initialize particles
i = np.arange(0, 10001)  # 0 to 1e4
x = i % 200
y = i / 43
k = 5 * np.cos(x/14) * np.cos(y/30)
e = y/8 - 13
d = (k**2 + e**2)/59 + 4
a = np.arctan2(k, e)

# Create scatter plot with initial empty data
sc = ax.scatter([], [], s=1, alpha=0.4, edgecolors='none', marker='o')

t = 0
dt = np.pi / 20
total_frames = 120  # About 4 seconds at 30 FPS

def update(frame):
    global t
    t += dt
    
    q = 60 - 3 * np.sin(a * e) + k * (3 + 4/d * np.sin(d**2 - t * 2))
    c = d/2 + e/99 - t/18
    
    xdata = q * np.sin(c) + 200
    ydata = (q + d * 9) * np.cos(c) + 200
    
    # Position-based coloring
    norm_x = (xdata - 200) / 200  # Normalize to [-1, 1]
    norm_y = (ydata - 200) / 200
    distance = np.sqrt(norm_x**2 + norm_y**2)
    angle = (np.arctan2(norm_y, norm_x) + np.pi) / (2 * np.pi)  # [0, 1]
    
    # Dynamic color mapping with time-based variation
    color_values = (distance * 0.7 + angle * 0.3 + t/20) % 1.0
    
    # Update scatter plot
    sc.set_offsets(np.column_stack((xdata, ydata)))
    sc.set_array(color_values)
    sc.set_cmap(cmap)
    
    return [sc]

# Create animation
ani = FuncAnimation(fig, update, frames=total_frames, interval=33, blit=True)

# Save as GIF
save_gif = True
if save_gif:
    print("Rendering animation...")
    ani.save('pluviophile.gif', writer='pillow', fps=30, dpi=100,
             progress_callback=lambda i, n: print(f"Frame {i}/{n}") if i % 30 == 0 else None)
    print("Animation saved as 'pluviophile.gif'")

plt.show()