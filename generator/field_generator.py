import numpy as np
from scipy.ndimage import gaussian_filter
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.topology_config import TOPOLOGY_CONFIG
from generator.case_definitions import create_blob, create_hole, get_safe_positions

def generate_topology_case(case_name, size=(256, 256), seed=None):
    """
    Genera un caso específico de topología
    
    Args:
        case_name: Nombre del caso a generar
        size: Tamaño de la imagen
        seed: Semilla para reproducibilidad
        
    Returns:
        Array 2D binario con la topología especificada
    """
    if seed is not None:
        np.random.seed(seed)
    
    if case_name == 'single_blob':
        return create_single_blob(size)
    elif case_name == 'blob_with_hole':
        return create_single_blob_with_holes(size, num_holes=1)
    elif case_name == 'blob_with_three_holes':
        return create_single_blob_with_holes(size, num_holes=3)
    elif case_name == 'two_blobs':
        return create_multiple_blobs(size, num_blobs=2)
    elif case_name == 'two_blobs_one_hole':
        return create_two_blobs_one_with_hole(size)
    elif case_name == 'complex_topology':
        return create_complex_topology(size)
    else:
        raise ValueError(f"Caso desconocido: {case_name}")

def create_single_blob(size):
    """Crea un blob único sin agujeros"""
    center_x = size[1] // 2
    center_y = size[0] // 2
    radius = min(size) // 4
    
    return create_blob((center_x, center_y), radius, size)

def create_single_blob_with_holes(size, num_holes=3):
    """
    Crea un blob con agujeros internos
    
    Args:
        size: Tamaño de la imagen
        num_holes: Número de agujeros a crear
        
    Returns:
        Array 2D con el blob y agujeros
    """
    # Crear blob principal
    center_x = size[1] // 2
    center_y = size[0] // 2
    blob_radius = min(size) // 3
    
    field = create_blob((center_x, center_y), blob_radius, size)
    
    # Crear agujeros dentro del blob
    hole_radius = blob_radius // 4
    min_distance = hole_radius * 2.5
    
    # Generar posiciones para agujeros dentro del blob
    hole_positions = []
    max_attempts = 50
    
    for _ in range(num_holes):
        for attempt in range(max_attempts):
            # Generar posición dentro del blob
            angle = np.random.uniform(0, 2 * np.pi)
            distance = np.random.uniform(0, blob_radius * 0.6)
            
            hole_x = center_x + distance * np.cos(angle)
            hole_y = center_y + distance * np.sin(angle)
            
            # Verificar que esté dentro de los límites
            if (hole_radius < hole_x < size[1] - hole_radius and 
                hole_radius < hole_y < size[0] - hole_radius):
                
                # Verificar distancia con otros agujeros
                valid = True
                for hx, hy in hole_positions:
                    if np.sqrt((hole_x - hx)**2 + (hole_y - hy)**2) < min_distance:
                        valid = False
                        break
                
                if valid:
                    hole_positions.append((hole_x, hole_y))
                    break
    
    # Crear agujeros
    for hole_x, hole_y in hole_positions:
        hole = create_hole((hole_x, hole_y), hole_radius, size)
        field = field * (1 - hole)  # Restar agujero del campo
    
    return field

def create_multiple_blobs(size, num_blobs=2):
    """
    Crea múltiples blobs separados
    
    Args:
        size: Tamaño de la imagen
        num_blobs: Número de blobs a crear
        
    Returns:
        Array 2D con múltiples blobs
    """
    blob_radius = min(size) // 6
    min_distance = blob_radius * 3
    
    positions = get_safe_positions(size, num_blobs, blob_radius, min_distance)
    
    field = np.zeros(size)
    for x, y in positions:
        blob = create_blob((x, y), blob_radius, size)
        field = np.maximum(field, blob)  # Unión de blobs
    
    return field

def create_two_blobs_one_with_hole(size):
    """Crea dos blobs, uno de ellos con un agujero"""
    blob_radius = min(size) // 5
    min_distance = blob_radius * 2.5
    
    # Posiciones para dos blobs
    positions = get_safe_positions(size, 2, blob_radius, min_distance)
    
    field = np.zeros(size)
    
    # Primer blob sin agujero
    blob1 = create_blob(positions[0], blob_radius, size)
    field = np.maximum(field, blob1)
    
    # Segundo blob con agujero
    blob2 = create_blob(positions[1], blob_radius, size)
    
    # Crear agujero en el segundo blob
    hole_radius = blob_radius // 3
    hole = create_hole(positions[1], hole_radius, size)
    blob2 = blob2 * (1 - hole)
    
    field = np.maximum(field, blob2)
    
    return field

def create_complex_topology(size):
    """
    Crea una topología compleja con múltiples características
    
    Returns:
        Array 2D con topología compleja
    """
    field = np.zeros(size)
    
    # Tres blobs principales
    blob_radius = min(size) // 6
    positions = get_safe_positions(size, 3, blob_radius, blob_radius * 2.2)
    
    for i, (x, y) in enumerate(positions):
        blob = create_blob((x, y), blob_radius, size)
        
        # Primer blob: sin agujero
        if i == 0:
            field = np.maximum(field, blob)
        # Segundo blob: con un agujero
        elif i == 1:
            hole_radius = blob_radius // 3
            hole = create_hole((x, y), hole_radius, size)
            blob = blob * (1 - hole)
            field = np.maximum(field, blob)
        # Tercer blob: con un agujero
        else:
            hole_radius = blob_radius // 4
            hole = create_hole((x, y), hole_radius, size)
            blob = blob * (1 - hole)
            field = np.maximum(field, blob)
    
    return field

def generate_vector_field(field):
    """
    Genera un campo vectorial basado en el gradiente del campo escalar
    
    Args:
        field: Campo escalar 2D
        
    Returns:
        Tupla (u, v) con componentes del campo vectorial
    """
    # Suavizar el campo para mejores gradientes
    smoothed_field = gaussian_filter(field.astype(float), sigma=2.0)
    
    # Calcular gradiente
    grad_y, grad_x = np.gradient(smoothed_field)
    
    # Normalizar y añadir componente rotacional para visualización
    norm = np.sqrt(grad_x**2 + grad_y**2) + 1e-8
    
    # Campo vectorial normalizado con componente tangencial
    u = grad_x / norm + 0.3 * (-grad_y / norm)
    v = grad_y / norm + 0.3 * (grad_x / norm)
    
    # Aplicar máscara del campo original
    mask = field > 0.1
    u = u * mask
    v = v * mask
    
    return u, v

def add_noise_to_field(field, noise_level=0.05):
    """
    Añade ruido controlado al campo para hacerlo más realista
    
    Args:
        field: Campo original
        noise_level: Nivel de ruido (0-1)
        
    Returns:
        Campo con ruido añadido
    """
    noise = np.random.normal(0, noise_level, field.shape)
    noisy_field = field + noise
    return np.clip(noisy_field, 0, 1)