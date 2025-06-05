import numpy as np
from scipy.ndimage import gaussian_filter
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.topology_config import TOPOLOGY_CASES, TOPOLOGY_CONFIG

def get_topology_cases():
    """Devuelve los casos de topología definidos"""
    return TOPOLOGY_CASES

def validate_case_topology(case_name, calculated_metrics):
    """
    Valida si las métricas calculadas coinciden con las esperadas
    
    Args:
        case_name: Nombre del caso
        calculated_metrics: Dict con métricas calculadas
        
    Returns:
        bool: True si coinciden, False en caso contrario
    """
    if case_name not in TOPOLOGY_CASES:
        return False
    
    expected = TOPOLOGY_CASES[case_name]
    
    return (
        calculated_metrics['beta0'] == expected['expected_beta0'] and
        calculated_metrics['beta1'] == expected['expected_beta1'] and
        calculated_metrics['euler_poincare'] == expected['expected_euler']
    )

def create_blob(center, radius, size, smooth=True):
    """
    Crea un blob circular en la imagen
    
    Args:
        center: Tupla (x, y) del centro
        radius: Radio del blob
        size: Tamaño de la imagen (height, width)
        smooth: Si aplicar suavizado gaussiano
        
    Returns:
        Array 2D con el blob
    """
    y, x = np.ogrid[:size[0], :size[1]]
    mask = (x - center[0])**2 + (y - center[1])**2 <= radius**2
    blob = np.zeros(size)
    blob[mask] = 1.0
    
    if smooth:
        blob = gaussian_filter(blob, sigma=TOPOLOGY_CONFIG['smoothing_sigma'])
        blob = (blob > 0.5).astype(float)
    
    return blob

def create_hole(center, radius, size):
    """
    Crea un agujero circular
    
    Args:
        center: Tupla (x, y) del centro
        radius: Radio del agujero
        size: Tamaño de la imagen
        
    Returns:
        Array 2D con el agujero (1=agujero, 0=material)
    """
    y, x = np.ogrid[:size[0], :size[1]]
    mask = (x - center[0])**2 + (y - center[1])**2 <= radius**2
    hole = np.zeros(size)
    hole[mask] = 1.0
    return hole

def get_safe_positions(size, num_positions, min_radius, min_distance):
    """
    Genera posiciones que no se superpongan
    
    Args:
        size: Tamaño de la imagen
        num_positions: Número de posiciones a generar
        min_radius: Radio mínimo de las características
        min_distance: Distancia mínima entre características
        
    Returns:
        Lista de posiciones (x, y)
    """
    positions = []
    max_attempts = 100
    
    for _ in range(num_positions):
        for attempt in range(max_attempts):
            x = np.random.randint(min_radius + 10, size[1] - min_radius - 10)
            y = np.random.randint(min_radius + 10, size[0] - min_radius - 10)
            
            # Verificar distancia mínima con posiciones existentes
            valid = True
            for px, py in positions:
                if np.sqrt((x - px)**2 + (y - py)**2) < min_distance:
                    valid = False
                    break
            
            if valid:
                positions.append((x, y))
                break
        else:
            # Si no se puede encontrar una posición válida, usar una aleatoria
            x = np.random.randint(min_radius + 10, size[1] - min_radius - 10)
            y = np.random.randint(min_radius + 10, size[0] - min_radius - 10)
            positions.append((x, y))
    
    return positions