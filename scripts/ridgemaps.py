import numpy as np
import matplotlib.pyplot as plt

from ridge_map import RidgeMap

# Plot with enhancements
fig, ax = plt.subplots(figsize=(14, 8))

rm_ch.plot_map(
    values=values_ch,
    label='Chimborazo Elevation',
    label_y=0.15,
    label_x=0.6,
    label_size=25,
    linewidth=1.5,
    line_color=plt.get_cmap('terrain'),
    kind='elevation',
    ax=ax  # Pass an explicit Axes to allow further customization
)

# Add title and annotations
ax.set_title('\nChimborazo Elevation Map', fontsize=20, fontweight='bold', pad=20)
# ax.text(0.5, 0.05, 'Elevation Lines at 150 Intervals', transform=ax.transAxes, 
#         fontsize=12, ha='center', va='center', style='italic')

# Flatten the array to calculate global min and max
elevation_min = np.min(values_ch)
elevation_max = np.max(values_ch)

# Create ScalarMappable for the colorbar
sm = plt.cm.ScalarMappable(cmap='terrain', norm=plt.Normalize(vmin=elevation_min, vmax=elevation_max))

# cbar = plt.colorbar(sm, ax=ax, orientation='horizontal', pad=0.05, aspect=50)
# cbar.set_label('Elevation (meters)', fontsize=12)

# Add a marker for Chimborazo's peak
# ax.plot(0.6, 0.15, 'ro', transform=ax.transAxes)  # Example peak position
# ax.text(0.61, 0.16, 'Chimborazo Peak (6,263m)', transform=ax.transAxes, fontsize=10, color='red')

# Hide axes for a clean map
ax.axis('off')

plt.tight_layout()
plt.savefig('chimborazo_elevation_map.png', dpi=300, bbox_inches='tight')
plt.show()
