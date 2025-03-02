import matplotlib.pyplot as plt
import numpy as np
import math


# Define common paper sizes in meters
paper_sizes_meters = {
    "A0": (0.841, 1.189),
    "A1": (0.594, 0.841),
    "A2": (0.420, 0.594),
    "A3": (0.297, 0.420),
    "A4": (0.210, 0.297),
}

def calculate_scale(utm_x, utm_y, paper_size="A1", target_aspect_ratio=25/22):
    """
    Calculate the map scale dynamically for accurate printing.

    Parameters:
    - utm_x, utm_y: Lists of UTM coordinates
    - paper_size: Selected paper format (default is A1)
    - target_aspect_ratio: The aspect ratio of the plotted figure

    Returns:
    - An integer representing the cartographic scale (e.g., 1:900)
    """
    return 900 # Fixed scale to 1:900

    x_range = max(utm_x) - min(utm_x)  # Width in meters
    y_range = max(utm_y) - min(utm_y)  # Height in meters

    if x_range == 0 or y_range == 0:
        return 1  # Prevent division by zero

    # Get the paper size in meters
    paper_width, paper_height = paper_sizes_meters.get(paper_size, paper_sizes_meters["A1"])

    # Adjust width to match the figure aspect ratio
    paper_width_adjusted = paper_height * target_aspect_ratio

    # Calculate scale based on both width and height constraints
    scale_x = x_range / paper_width_adjusted
    scale_y = y_range / paper_height

    # Choose the larger scale to fit within the paper
    calculated_scale = max(scale_x, scale_y)

    # Round to the nearest standard cartographic scale
    possible_scales = [500, 750, 900, 1000, 1500, 2000, 2500]
    final_scale = min(possible_scales, key=lambda x: abs(x - calculated_scale))

    return final_scale

utm_coords = [
    (5.0, 98.0)
]

distances = []

for i in range(len(utm_coords) - 1):
    point1 = utm_coords[i]
    point2 = utm_coords[i+1]

    x1, y1 = point1
    x2, y2 = point2

    distance = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    distances.append(distance)

# Extract UTM Easting (x) and Northing (y)
utm_x, utm_y = zip(*utm_coords)

fig, ax = plt.subplots(figsize=(25, 22))

ax.plot(
    utm_x, utm_y,
    'ko-',
    markersize=0,
    linewidth=1,
    label="Path (UTM)"
)

for i in range(len(utm_coords) - 1):
    point1 = utm_coords[i]
    point2 = utm_coords[i+1]

    mid_x = (point1[0] + point2[0]) / 2
    mid_y = (point1[1] + point2[1]) / 2

    dx = point2[0] - point1[0]
    dy = point2[1] - point1[1]
    rotation_degrees = np.degrees(np.arctan2(dy, dx))

    if (0 <= rotation_degrees < 90) or (-180 <= rotation_degrees < -90):  # First & Third Quadrants
        rotation_degrees -= 7.5
    else:  # Second & Fourth Quadrants (90 to 180, -90 to 0)
        rotation_degrees += 7.5

    offset_pixels = 10
    offset_x_pixels = offset_pixels * math.cos(math.radians(rotation_degrees + 90))
    offset_y_pixels = offset_pixels * math.sin(math.radians(rotation_degrees + 90))

    ax.annotate(
        f"{distances[i]:.2f} m",
        xy=(mid_x, mid_y),
        xytext=(offset_x_pixels, offset_y_pixels),
        textcoords='offset points',
        ha='center',
        va='center',
        rotation=rotation_degrees,
        fontsize=15,
        color='black'
    )

    ax.text(point1[0], point1[1], f"P0{i+1}",
            horizontalalignment='center',
            verticalalignment='center',
            rotation_mode='anchor',
            fontsize=15,
            color='red')
    ax.plot(point1[0], point1[1], "o", color='red', markersize=3, linewidth=10)

# Zoom out by adding margins
margin_factor = 0.25
x_min, x_max = min(utm_x), max(utm_x)
y_min, y_max = min(utm_y), max(utm_y)
x_range = x_max - x_min
y_range = y_max - y_min

ax.set_xlim(x_min - margin_factor*x_range, x_max + margin_factor*x_range)
ax.set_ylim(y_min - margin_factor*y_range, y_max + margin_factor*y_range)

# Define the number of grid lines
num_grid_lines = 6  # Adjust this based on the printed version

# Generate custom tick positions
x_lim = ax.get_xlim()
y_lim = ax.get_ylim()
custom_xticks = np.linspace(x_lim[0], x_lim[1], num_grid_lines, dtype=int)
custom_yticks = np.linspace(y_lim[0], y_lim[1], num_grid_lines, dtype=int)

custom_xticks = [tick for tick in custom_xticks if x_min <= tick <= x_max]
custom_yticks = [tick for tick in custom_yticks if y_min <= tick <= y_max]

ax.set_xticks(custom_xticks)
ax.set_yticks(custom_yticks)
ax.set_xticklabels([f"{tick}" for tick in custom_xticks], fontsize=15)
ax.set_yticklabels([f"{tick}" for tick in custom_yticks], rotation=90, fontsize=15)

ax2 = ax.twiny()
ax3 = ax.twinx()

ax2.set_xlim(ax.get_xlim())
ax3.set_ylim(ax.get_ylim())
ax2.set_xticks(custom_xticks)
ax3.set_yticks(custom_yticks)
ax2.set_xticklabels([f"{tick}" for tick in custom_xticks], fontsize=15)
ax3.set_yticklabels([f"{tick}" for tick in custom_yticks], rotation=270, fontsize=15)

ax.grid(True, which='major', linestyle='--', linewidth=0.5)
ax2.grid(True, which='major', linestyle='--', linewidth=0.5)
ax3.grid(True, which='major', linestyle='--', linewidth=0.5)

for tick in custom_xticks:
    ax.axvline(x=tick, color='gray', linestyle='--', linewidth=0.5)
for tick in custom_yticks:
    ax.axhline(y=tick, color='gray', linestyle='--', linewidth=0.5)

# Calculate and display the correct scale
dynamic_scale = calculate_scale(utm_x, utm_y)
plt.figtext(0.8, 0.02, f"Escala 1:{dynamic_scale}", fontsize=15, color='black')

plt.show()

print("11111")
