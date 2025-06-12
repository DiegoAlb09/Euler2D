"""
Configuración para el análisis topológico 2D
"""

# Configuración de imágenes
IMAGE_CONFIG = {
    'default_size': (256, 256),  # Tamaño por defecto para imágenes generadas
    'min_size': (64, 64),       # Tamaño mínimo permitido
    'max_size': (1024, 1024),   # Tamaño máximo permitido
    'binary_threshold': 0.5,    # Umbral para binarización
}

# Configuración de visualización
VISUALIZATION_CONFIG = {
    'dpi': 300,                 # DPI para guardar imágenes
    'vector_field_step': 10,    # Paso para submuestreo del campo vectorial
    'arrow_color': 'red',       # Color de las flechas del campo vectorial
    'arrow_scale': 30,          # Escala de las flechas
}

# Configuración de topología
TOPOLOGY_CONFIG = {
    'smoothing_sigma': 1.0,     # Sigma para suavizado gaussiano
    'min_blob_radius': 10,      # Radio mínimo para blobs
    'min_hole_radius': 5,       # Radio mínimo para agujeros
    'min_distance': 20,         # Distancia mínima entre características
    'noise_level': 0.05,        # Nivel de ruido por defecto
} 