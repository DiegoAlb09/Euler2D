import numpy as np
from scipy.ndimage import label, binary_erosion, binary_dilation
from skimage.morphology import skeletonize
from skimage.measure import regionprops
from .topology_base import compute_betti_numbers_2d
from .topology_codes import compute_vcc, compute_3ot
from .topology_codes_extended import get_f8_code, f8_to_f4

def count_vertices_edges_faces_corrected(binary_image):
    """
    Cuenta vértices, aristas y caras usando el método de complejos celulares 2D
    
    Args:
        binary_image: Imagen binaria
        
    Returns:
        tuple: (V, E, F) vértices, aristas, caras
    """
    # Convertir a binario
    binary_img = (binary_image > 0.5).astype(bool)
    h, w = binary_img.shape
    
    # Contar caras (píxeles activos) - F
    F = np.sum(binary_img)
    
    # Contar aristas - método corregido
    # Aristas internas: conexiones entre píxeles adyacentes activos
    E_internal = 0
    
    # Aristas horizontales internas
    for i in range(h):
        for j in range(w - 1):
            if binary_img[i, j] and binary_img[i, j + 1]:
                E_internal += 1
    
    # Aristas verticales internas
    for i in range(h - 1):
        for j in range(w):
            if binary_img[i, j] and binary_img[i + 1, j]:
                E_internal += 1
    
    # Aristas de borde: cada píxel activo contribuye con aristas al borde
    E_boundary = 0
    for i in range(h):
        for j in range(w):
            if binary_img[i, j]:
                # Contar vecinos inactivos (contribuyen aristas de borde)
                neighbors = []
                if i > 0: neighbors.append(binary_img[i-1, j])
                else: neighbors.append(False)  # borde superior
                
                if i < h-1: neighbors.append(binary_img[i+1, j])
                else: neighbors.append(False)  # borde inferior
                
                if j > 0: neighbors.append(binary_img[i, j-1])
                else: neighbors.append(False)  # borde izquierdo
                
                if j < w-1: neighbors.append(binary_img[i, j+1])
                else: neighbors.append(False)  # borde derecho
                
                E_boundary += sum(1 for n in neighbors if not n)
    
    E = E_internal + E_boundary
    
    # Contar vértices - método corregido usando intersecciones de aristas
    V = 0
    
    # Vértices internos: intersecciones entre píxeles activos
    for i in range(h + 1):
        for j in range(w + 1):
            # Verificar los 4 píxeles alrededor de este vértice potencial
            pixels = []
            
            # Píxel superior-izquierdo
            if i > 0 and j > 0:
                pixels.append(binary_img[i-1, j-1])
            else:
                pixels.append(False)
            
            # Píxel superior-derecho
            if i > 0 and j < w:
                pixels.append(binary_img[i-1, j])
            else:
                pixels.append(False)
            
            # Píxel inferior-izquierdo
            if i < h and j > 0:
                pixels.append(binary_img[i, j-1])
            else:
                pixels.append(False)
            
            # Píxel inferior-derecho
            if i < h and j < w:
                pixels.append(binary_img[i, j])
            else:
                pixels.append(False)
            
            # Contar píxeles activos
            active_count = sum(pixels)
            
            # Un vértice existe si hay al menos un píxel activo
            if active_count > 0:
                V += 1
    
    return V, E, F

def euler_characteristic_2d(binary_image):
    """
    Calcula la característica de Euler usando χ = V - E + F (Método 1)
    
    Args:
        binary_image: Imagen binaria
        
    Returns:
        int: Característica de Euler
    """
    V, E, F = count_vertices_edges_faces_corrected(binary_image)
    return V - E + F

def euler_poincare_2d(binary_image):
    """
    Calcula la característica de Euler usando χ = β₀ - β₁ (Método 2 - Euler-Poincaré)
    
    Args:
        binary_image: Imagen binaria
        
    Returns:
        int: Característica de Euler
    """
    beta0, beta1 = compute_betti_numbers_2d(binary_image)
    return beta0 - beta1

def validate_euler_formulas(binary_image, tolerance=0):
    """
    Compara las dos fórmulas de Euler y valida su consistencia
    
    Args:
        binary_image: Imagen binaria
        tolerance: Tolerancia permitida entre las dos fórmulas
        
    Returns:
        dict: Diccionario con métricas y validación
    """
    # Calcular usando ambas fórmulas
    V, E, F = count_vertices_edges_faces_corrected(binary_image)
    beta0, beta1 = compute_betti_numbers_2d(binary_image)
    
    euler_vef = V - E + F
    euler_betti = beta0 - beta1
    
    # Validar consistencia
    is_consistent = abs(euler_vef - euler_betti) <= tolerance
    
    return {
        'vertices': V,
        'edges': E,
        'faces': F,
        'beta0': beta0,
        'beta1': beta1,
        'euler_vef': euler_vef,
        'euler_poincare': euler_betti,
        'is_consistent': is_consistent,
        'difference': abs(euler_vef - euler_betti)
    }

def compute_all_metrics(binary_image):
    """
    Calcula todas las métricas topológicas para una imagen
    
    Args:
        binary_image: Imagen binaria
        
    Returns:
        dict: Todas las métricas topológicas
    """
    metrics = validate_euler_formulas(binary_image)
    
    # Añadir información adicional
    metrics['area_fraction'] = np.sum(binary_image > 0.5) / binary_image.size
    metrics['perimeter'] = compute_perimeter(binary_image)
    
    # Generar códigos en secuencia F8 -> F4 -> VCC -> 3OT
    f8_code = get_f8_code(binary_image)
    f4_code = f8_to_f4(f8_code)
    
    # Añadir códigos topológicos
    vcc_results = compute_vcc(binary_image, f4_code)
    metrics['vcc'] = vcc_results
    
    # Calcular 3OT a partir de VCC
    ot3_results = compute_3ot(binary_image, vcc_results['code_string'])
    metrics['3ot'] = ot3_results
    
    return metrics

def compute_perimeter(binary_image):
    """
    Calcula el perímetro de la imagen binaria
    
    Args:
        binary_image: Imagen binaria
        
    Returns:
        float: Perímetro aproximado
    """
    binary_img = (binary_image > 0.5).astype(bool)
    
    # Erosión para encontrar el borde
    eroded = binary_erosion(binary_img)
    boundary = binary_img & ~eroded
    
    return np.sum(boundary)

def analyze_connectivity(binary_image):
    """
    Analiza las propiedades de conectividad detalladas
    
    Args:
        binary_image: Imagen binaria
        
    Returns:
        dict: Análisis de conectividad
    """
    binary_img = (binary_image > 0.5).astype(bool)
    labeled_array, num_components = label(binary_img)
    
    component_sizes = []
    component_holes = []
    
    for i in range(1, num_components + 1):
        component_mask = (labeled_array == i)
        size = np.sum(component_mask)
        component_sizes.append(size)
        
        # Contar agujeros en este componente usando el método corregido
        # Extraer solo esta componente para análisis individual
        coords = np.where(component_mask)
        if len(coords[0]) == 0:
            component_holes.append(0)
            continue
            
        min_row, max_row = coords[0].min(), coords[0].max()
        min_col, max_col = coords[1].min(), coords[1].max()
        
        # Extraer región con padding
        padded_min_row = max(0, min_row - 1)
        padded_max_row = min(binary_img.shape[0], max_row + 2)
        padded_min_col = max(0, min_col - 1)
        padded_max_col = min(binary_img.shape[1], max_col + 2)
        
        component_region = component_mask[padded_min_row:padded_max_row, 
                                        padded_min_col:padded_max_col]
        
        # Analizar agujeros en el complemento
        complement = ~component_region
        labeled_holes, num_bg = label(complement)
        
        holes = 0
        for hole_id in range(1, num_bg + 1):
            hole_mask = (labeled_holes == hole_id)
            
            # Verificar si toca el borde
            touches_border = (
                np.any(hole_mask[0, :]) or np.any(hole_mask[-1, :]) or
                np.any(hole_mask[:, 0]) or np.any(hole_mask[:, -1])
            )
            
            if not touches_border:
                holes += 1
        
        component_holes.append(holes)
    
    return {
        'num_components': num_components,
        'component_sizes': component_sizes,
        'component_holes': component_holes,
        'largest_component_size': max(component_sizes) if component_sizes else 0,
        'total_holes': sum(component_holes)
    }