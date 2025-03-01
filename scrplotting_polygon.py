import matplotlib.pyplot as plt
import numpy as np
import math

utm_coords = [
    (0.0, 0.0),
    ...
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

    # Correct adjustment based on the quadrant, considering negative angles
    print(f"Before Adjustment: {rotation_degrees:.2f} degrees")

    if (0 <= rotation_degrees < 90) or (-180 <= rotation_degrees < -90):  # First & Third Quadrants
        rotation_degrees -= 7.5
    else:  # Second & Fourth Quadrants (90 to 180, -90 to 0)
        rotation_degrees += 7.5

    print(f"After Adjustment: {rotation_degrees:.2f} degrees")

    offset_pixels = 10
    offset_x_pixels = offset_pixels * math.cos(math.radians(rotation_degrees + 90))
    offset_y_pixels = offset_pixels * math.sin(math.radians(rotation_degrees + 90))

    print(f"{distances[i]:.2f} m")
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
    print()

# Zoom out by adding margins
margin_factor = 0.25
x_min, x_max = min(utm_x), max(utm_x)
y_min, y_max = min(utm_y), max(utm_y)
x_range = x_max - x_min
y_range = y_max - y_min

ax.set_xlim(x_min - margin_factor*x_range, x_max + margin_factor*x_range)
ax.set_ylim(y_min - margin_factor*y_range, y_max + margin_factor*y_range)

ax.minorticks_on()

x_lim = ax.get_xlim()
y_lim = ax.get_ylim()
custom_xticks = np.linspace(x_lim[0], x_lim[1], 4)
custom_yticks = np.linspace(y_lim[0], y_lim[1], 4)
ax.set_xticks(custom_xticks)
ax.set_xticklabels([f"{tick:.4f}" for tick in custom_xticks])

ax2 = ax.twiny()
ax2.minorticks_on()
ax2.set_xlim(ax.get_xlim())
ax2.set_xticks(custom_xticks)
ax2.set_xticklabels([f"{tick:.4f}" for tick in custom_xticks])

ax3 = ax.twinx()
ax3.minorticks_on()
ax3.set_ylim(ax.get_ylim())
ax3.set_yticks(custom_yticks)
ax3.set_yticklabels([f"{tick:.4f}" for tick in custom_yticks])

ax.set_yticks(custom_yticks)
ax.set_yticklabels([f"{tick:.4f}" for tick in custom_yticks])

for label in ax.get_yticklabels():
    label.set_rotation(90)
    label.set_ha('right')

for label in ax3.get_yticklabels():
    label.set_rotation(90)
    label.set_ha('left')

plt.grid()
plt.show()
