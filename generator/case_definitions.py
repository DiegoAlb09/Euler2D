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

def create_blob(center, radius, size, smooth=False):
    """
    Crea un blob circular en la imagen - VERSIÓN CORREGIDA
    
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
    blob = np.zeros(size, dtype=float)
    blob[mask] = 1.0
    
    if smooth:
        blob = gaussian_filter(blob, sigma=TOPOLOGY_CONFIG['smoothing_sigma'])
        # Mantener binarización más estricta para topología clara
        blob = (blob > 0.3).astype(float)
    
    return blob

def create_hole(center, radius, size):
    """
    Crea un agujero circular - VERSIÓN CORREGIDA
    
    Args:
        center: Tupla (x, y) del centro
        radius: Radio del agujero
        size: Tamaño de la imagen
        
    Returns:
        Array 2D con el agujero (1=agujero, 0=material)
    """
    y, x = np.ogrid[:size[0], :size[1]]
    mask = (x - center[0])**2 + (y - center[1])**2 <= radius**2
    hole = np.zeros(size, dtype=float)
    hole[mask] = 1.0
    return hole

def get_safe_positions(size, num_positions, min_radius, min_distance):
    """
    Genera posiciones que no se superpongan - VERSIÓN MEJORADA
    
    Args:
        size: Tamaño de la imagen
        num_positions: Número de posiciones a generar
        min_radius: Radio mínimo de las características
        min_distance: Distancia mínima entre características
        
    Returns:
        Lista de posiciones (x, y)
    """
    positions = []
    max_attempts = 200  # Más intentos
    margin = min_radius + 10  # Margen desde el borde
    
    for i in range(num_positions):
        best_position = None
        best_min_distance = 0
        
        for attempt in range(max_attempts):
            x = np.random.randint(margin, size[1] - margin)
            y = np.random.randint(margin, size[0] - margin)
            
            # Calcular distancia mínima a posiciones existentes
            if positions:
                distances = [np.sqrt((x - px)**2 + (y - py)**2) for px, py in positions]
                current_min_distance = min(distances)
            else:
                current_min_distance = float('inf')
            
            # Si cumple la distancia mínima, usarla inmediatamente
            if current_min_distance >= min_distance:
                positions.append((x, y))
                break
            
            # Si no, guardar la mejor hasta ahora
            if current_min_distance > best_min_distance:
                best_min_distance = current_min_distance
                best_position = (x, y)
        
        # Si no se encontró una posición válida, usar la mejor
        if len(positions) <= i and best_position is not None:
            positions.append(best_position)
        elif len(positions) <= i:
            # Última opción: posición determinística
            if num_positions == 2:
                if i == 0:
                    positions.append((size[1]//3, size[0]//2))
                else:
                    positions.append((2*size[1]//3, size[0]//2))
            else:
                # Para otros números de posiciones, usar una cuadrícula
                grid_size = int(np.ceil(np.sqrt(num_positions)))
                x = margin + (i % grid_size) * ((size[1] - 2*margin) // (grid_size - 1))
                y = margin + (i // grid_size) * ((size[0] - 2*margin) // (grid_size - 1))
                positions.append((x, y))
    
    return positions

def get_safe_positions_old(size, num_positions, min_radius, min_distance):
    """
    Genera posiciones que no se superpongan - VERSIÓN ANTIGUA
    
    Args:
        size: Tamaño de la imagen
        num_positions: Número de posiciones a generar
        min_radius: Radio mínimo de las características
        min_distance: Distancia mínima entre características
        
    Returns:
        Lista de posiciones (x, y)
    """
    positions = []
    max_attempts = 200  # Más intentos
    margin = min_radius + 10  # Margen desde el borde
    
    for i in range(num_positions):
        best_position = None
        best_min_distance = 0
        
        for attempt in range(max_attempts):
            x = np.random.randint(margin, size[1] - margin)
            y = np.random.randint(margin, size[0] - margin)
            
            # Calcular distancia mínima a posiciones existentes
            if positions:
                distances = [np.sqrt((x - px)**2 + (y - py)**2) for px, py in positions]
                current_min_distance = min(distances)
            else:
                current_min_distance = float('inf')
            
            # Si cumple la distancia mínima, usarla inmediatamente
            if current_min_distance >= min_distance:
                positions.append((x, y))
                break
            
            # Si no, guardar la mejor hasta ahora
            if current_min_distance > best_min_distance:
                best_min_distance = current_min_distance
                best_position = (x, y)
        
        # Si no se encontró una posición válida, usar la mejor
        if len(positions) <= i and best_position is not None:
            positions.append(best_position)
        elif len(positions) <= i:
            # Última opción: posición determinística
            if num_positions == 2:
                if i == 0:
                    positions.append((size[1]//3, size[0]//2))
                else:
                    positions.append((2*size[1]//3, size[0]//2))
            else:
                # Para otros números de posiciones, usar una cuadrícula
                grid_size = int(np.ceil(np.sqrt(num_positions)))
                x = margin + (i % grid_size) * ((size[1] - 2*margin) // (grid_size - 1))
                y = margin + (i // grid_size) * ((size[0] - 2*margin) // (grid_size - 1))
                positions.append((x, y))
    
    return positions
    