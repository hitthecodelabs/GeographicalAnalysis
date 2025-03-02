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

def round_to_nearest_multiple(value, multiple=30):
    return multiple * round(value / multiple)

def calculate_scale(utm_x, utm_y, paper_size="A1", target_aspect_ratio=25/22):
    """
    Calculate the map scale dynamically for accurate printing.
    """
    x_range = max(utm_x) - min(utm_x)  # Width in meters
    y_range = max(utm_y) - min(utm_y)  # Height in meters

    if x_range == 0 or y_range == 0:
        return 1  # Prevent division by zero

    paper_width, paper_height = paper_sizes_meters.get(paper_size, paper_sizes_meters["A1"])
    paper_width_adjusted = paper_height * target_aspect_ratio
    
    scale_x = x_range / paper_width_adjusted
    scale_y = y_range / paper_height
    
    calculated_scale = max(scale_x, scale_y)
    
    possible_scales = [500, 750, 900, 1000, 1500, 2000, 2500]
    final_scale = min(possible_scales, key=lambda x: abs(x - calculated_scale))
    
    return final_scale

utm_coords = [
    (5.0, 94.0),
]

distances = []
for i in range(len(utm_coords) - 1):
    point1 = utm_coords[i]
    point2 = utm_coords[i+1]
    distance = math.sqrt((point2[0] - point1[0])**2 + (point2[1] - point1[1])**2)
    distances.append(distance)

utm_x, utm_y = zip(*utm_coords)

fig, ax = plt.subplots(figsize=(25, 22))
ax.plot(utm_x, utm_y, 'ko-', markersize=0, linewidth=1, label="Path (UTM)")

for i in range(len(utm_coords) - 1):
    point1 = utm_coords[i]
    point2 = utm_coords[i+1]
    mid_x = (point1[0] + point2[0]) / 2
    mid_y = (point1[1] + point2[1]) / 2
    dx = point2[0] - point1[0]
    dy = point2[1] - point1[1]
    rotation_degrees = np.degrees(np.arctan2(dy, dx))
    rotation_degrees += -7.5 if (0 <= rotation_degrees < 90) or (-180 <= rotation_degrees < -90) else 7.5
    offset_pixels = 10
    offset_x_pixels = offset_pixels * math.cos(math.radians(rotation_degrees + 90))
    offset_y_pixels = offset_pixels * math.sin(math.radians(rotation_degrees + 90))
    ax.annotate(f"{distances[i]:.2f} m", xy=(mid_x, mid_y), xytext=(offset_x_pixels, offset_y_pixels), textcoords='offset points', ha='center', va='center', rotation=rotation_degrees, fontsize=15, color='black')
    ax.text(point1[0], point1[1], f"P0{i+1}", horizontalalignment='center', verticalalignment='center', rotation_mode='anchor', fontsize=15, color='red')
    ax.plot(point1[0], point1[1], "o", color='red', markersize=3, linewidth=10)

margin_factor = 0.3  # Adjusted for better centering
x_min, x_max = min(utm_x), max(utm_x)
y_min, y_max = min(utm_y), max(utm_y)
x_range = x_max - x_min
y_range = y_max - y_min
x_centered_min = round_to_nearest_multiple(x_min - margin_factor*x_range)
x_centered_max = round_to_nearest_multiple(x_max + margin_factor*x_range)
y_centered_min = round_to_nearest_multiple(y_min - margin_factor*y_range)
y_centered_max = round_to_nearest_multiple(y_max + margin_factor*y_range)
ax.set_xlim(x_centered_min, x_centered_max)
ax.set_ylim(y_centered_min, y_centered_max)

num_grid_lines = 7  # Adjusted to maintain proper spacing
custom_xticks = np.arange(x_centered_min, x_centered_max + 1, 30)
custom_yticks = np.arange(y_centered_min, y_centered_max + 1, 30)
ax.set_xticks(custom_xticks)
ax.set_yticks(custom_yticks)
ax.set_xticklabels([f"{tick}" for tick in custom_xticks], fontsize=15)
ax.set_yticklabels([f"{tick}" for tick in custom_yticks], rotation=90, fontsize=15)

ax2, ax3 = ax.twiny(), ax.twinx()
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

dynamic_scale = calculate_scale(utm_x, utm_y)
# plt.figtext(0.8, 0.02, f"Escala 1:{dynamic_scale}", fontsize=15, color='black')
plt.show()
