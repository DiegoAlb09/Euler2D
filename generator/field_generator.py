import numpy as np
from scipy.ndimage import gaussian_filter

def generate_field_with_holes(size=(256, 256), num_holes=3, hole_radius=20):
    field = np.ones(size)

    # Centroides aleatorios para los agujeros
    centers = np.random.randint(hole_radius, size[0] - hole_radius, size=(num_holes, 2))

    for cx, cy in centers:
        y, x = np.ogrid[:size[0], :size[1]]
        mask = (x - cx)**2 + (y - cy)**2 <= hole_radius**2
        field[mask] = 0  # agujero (porosidad)

    return field

def generate_vector_field(field):
    # Campo vectorial artificial generado como gradiente del campo base
    grad_y, grad_x = np.gradient(field)
    norm = np.sqrt(grad_x**2 + grad_y**2) + 1e-5
    return grad_x / norm, grad_y / norm
