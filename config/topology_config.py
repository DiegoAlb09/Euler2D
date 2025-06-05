# Configuración de parámetros para análisis topológico

# Configuración de imágenes
IMAGE_CONFIG = {
    'default_size': (256, 256),
    'output_format': 'png',
    'dpi': 150
}

# Configuración de visualización
VISUALIZATION_CONFIG = {
    'vector_field_step': 8,
    'arrow_scale': 15,
    'arrow_color': 'red',
    'background_cmap': 'gray',
    'figsize': (10, 8),
    'dpi': 150
}

# Configuración de topología
TOPOLOGY_CONFIG = {
    'blob_radius_range': (30, 50),
    'hole_radius_range': (15, 25),
    'min_distance_between_features': 40,
    'smoothing_sigma': 2.0
}

# Casos de prueba predefinidos
TOPOLOGY_CASES = {
    'single_blob': {
        'description': 'Un blob sin agujeros',
        'expected_beta0': 1,
        'expected_beta1': 0,
        'expected_euler': 1
    },
    'blob_with_hole': {
        'description': 'Un blob con un agujero',
        'expected_beta0': 1,
        'expected_beta1': 1,
        'expected_euler': 0
    },
    'blob_with_three_holes': {
        'description': 'Un blob con tres agujeros',
        'expected_beta0': 1,
        'expected_beta1': 3,
        'expected_euler': -2
    },
    'two_blobs': {
        'description': 'Dos blobs separados',
        'expected_beta0': 2,
        'expected_beta1': 0,
        'expected_euler': 2
    },
    'two_blobs_one_hole': {
        'description': 'Dos blobs, uno con agujero',
        'expected_beta0': 2,
        'expected_beta1': 1,
        'expected_euler': 1
    },
    'complex_topology': {
        'description': 'Topología compleja',
        'expected_beta0': 3,
        'expected_beta1': 2,
        'expected_euler': 1
    }
}