import numpy as np
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.topology_config import TOPOLOGY_CASES, TOPOLOGY_CONFIG
from generator.field_generator import (
    create_horizontal_dominant, create_vertical_dominant,
    create_asymmetric_mesh, create_asymmetric_spiral, create_asymmetric_branches,
    create_single_blob, create_single_blob_with_holes, create_multiple_blobs,
    create_two_blobs_one_with_hole, create_complex_topology, create_irregular_star,
    create_irregular_chain, create_irregular_mesh, create_irregular_clusters,
    create_spiral_holes
)

def get_topology_cases():
    """Devuelve los casos de topología definidos"""
    cases = TOPOLOGY_CASES.copy()
    
    
    # Map cases to their generation functions
    case_functions = {
        'single_blob': create_single_blob,
        'blob_with_hole': lambda size: create_single_blob_with_holes(size, num_holes=1),
        'blob_with_three_holes': lambda size: create_single_blob_with_holes(size, num_holes=3),
        'two_blobs': lambda size: create_multiple_blobs(size, num_blobs=2),
        'two_blobs_one_hole': create_two_blobs_one_with_hole,
        'complex_topology': create_complex_topology,
        'irregular_star': create_irregular_star,
        'irregular_chain': create_irregular_chain,
        'irregular_mesh': create_irregular_mesh,
        'irregular_clusters': create_irregular_clusters,
        'spiral_holes': create_spiral_holes
    }

    # Update existing cases with their generate functions
    for case_name, generate_func in case_functions.items():
        if case_name in cases:
            cases[case_name] = {**cases[case_name], 'generate': generate_func}
    
    # Añadir nuevos casos asimétricos
    cases.update({
        'horizontal_dominant': {
            'description': 'Estructura con dominancia horizontal',
            'expected_beta0': 1,
            'expected_beta1': 0,
            'expected_euler': 1,
            'generate': create_horizontal_dominant
        },
        'vertical_dominant': {
            'description': 'Estructura con dominancia vertical',
            'expected_beta0': 1,
            'expected_beta1': 0,
            'expected_euler': 1,
            'generate': create_vertical_dominant
        },
        'asymmetric_mesh': {
            'description': 'Malla asimétrica con más segmentos horizontales',
            'expected_beta0': 1,
            'expected_beta1': 4,
            'expected_euler': -3,
            'generate': create_asymmetric_mesh
        },
        'asymmetric_spiral': {
            'description': 'Espiral asimétrica con segmentos variables',
            'expected_beta0': 1,
            'expected_beta1': 0,
            'expected_euler': 1,
            'generate': create_asymmetric_spiral
        },
        'asymmetric_branches': {
            'description': 'Estructura ramificada asimétrica',
            'expected_beta0': 1,
            'expected_beta1': 0,
            'expected_euler': 1,
            'generate': create_asymmetric_branches
        }
    })
    
    return cases

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

# Pattern generation functions have been moved to field_generator.py to avoid circular imports
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
    
