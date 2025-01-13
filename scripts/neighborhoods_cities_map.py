# Create the color bar based on the bins
fig, ax = plt.subplots(1, 1, figsize=(15, 9), facecolor='black')
plot = gdf.plot(
    column='area_bins',
    cmap=cmap,
    linewidth=2,
    edgecolor='k',
    ax=ax,
    legend=True,
    missing_kwds={"color": "white", "label": "Sin datos"}
)

# Customize the legend
leg = ax.get_legend()
leg.set_bbox_to_anchor((0.15, 0.2))  # Use xy coordinates for precise positioning
leg.set_title("Tamaño de los Barrios (km²)", prop={'size': 12})
leg.get_title().set_color("white")  # Set title color to white

# Retrieve the legend handles and labels
handles, labels = leg.legend_handles, [text.get_text() for text in leg.get_texts()]

# Remove the unwanted label and its handle
new_handles = []
new_labels = []
for handle, label in zip(handles, labels):
    if label != ">100 km²":  # Keep only labels other than ">100 km²"
        new_handles.append(handle)
        new_labels.append(label)

# Update the legend with the filtered handles and labels
leg = ax.legend(new_handles, new_labels, loc='lower left', 
                bbox_to_anchor=(0.0, 0.2),
                title="Tamaño de los Barrios (km²)", 
                fontsize=10)

leg.get_title().set_color("white")  # Set title color to white
for text in leg.get_texts():
    text.set_color("white")  # Ensure text color is white

# Set the background color of the legend box
frame = leg.get_frame()
frame.set_facecolor("black")  # Set the background to black
frame.set_edgecolor("white")  # Set the edge color to white for contrast

# Add the title and background
ax.set_title(
    "\nMapa Coroplético de las Áreas de los Barrios en Barcelona", 
    color='white', 
    x=0.485,
    fontsize=14  # Increase the font size
)
ax.set_facecolor('k')  # Set axis background to black

# Add source attribution
ax.text(
    1.1, -0.05,  # Adjust position as needed
    "Data source: OpenStreetMap contributors. Processed using OSMnx.",
    fontsize=8, color='white', ha='right', transform=ax.transAxes
)

# Save the figure
plt.savefig('DAY16_adjusted_legend_xy_coords.png', dpi=150, bbox_inches='tight', facecolor='k')
