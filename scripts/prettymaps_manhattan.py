import prettymaps
import matplotlib.pyplot as plt
from matplotlib.transforms import Affine2D

# Crear el mapa
fig, ax = plt.subplots(figsize=(12, 12))

# Generar el mapa sin rotación inicial
prettymaps.plot(
    'Manhattan, New York, NY, USA',
    ax=ax,
    layers={
        "building": {"tags": {"building": True}},
        "water": {"tags": {"natural": "water"}},
        "green": {"tags": {"landuse": ["grass", "forest"], "natural": "wood"}},
        "streets": {"tags": {"highway": ["primary", "secondary", "tertiary"]}}
    },
    style={
        "building": {"palette": ["#D4A5A5", "#F1C5C5"], "edgecolor": "#E8C8C8"},
        "water": {"palette": ["#A1D6E2"]},
        "green": {"palette": ["#B5EAD7", "#CFF2D9"]},
        "streets": {"palette": ["#999999"], "linewidth": 0.5}
    },
    circle=False,
    radius=5000
)

# Aplicar rotación al eje (en este caso 45 grados)
rotation_degrees = 45  # Cambia el ángulo según desees
transform = Affine2D().rotate_deg(rotation_degrees) + ax.transData
ax.set_transform(transform)

# Ajustar límites y mostrar el mapa
ax.set_xlim(ax.get_xlim())  # Ajusta límites para incluir todos los datos tras la rotación
ax.set_ylim(ax.get_ylim())
plt.savefig("manhattan_map.png")
plt.show()
