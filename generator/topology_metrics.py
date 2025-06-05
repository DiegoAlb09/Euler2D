import numpy as np
from scipy.ndimage import label, binary_erosion, binary_dilation
from skimage.morphology import skeletonize
from skimage.measure import regionprops

def compute_betti_numbers_2d(binary_image):
    """
    Calcula los números de Betti β₀ y β₁ para una imagen binaria 2D
    
    Args:
        binary_image: Imagen binaria donde 1=material, 0=poro
        
    Returns:
        tuple: (beta0, beta1) donde beta0 es componentes conectados y beta1 es agujeros
    """
    # Asegurar que sea binario y que el fondo esté rodeado por ceros
    binary_img = (binary_image > 0.5).astype(bool)
    
    # Crear una imagen con padding de ceros para asegurar conectividad del fondo
    padded_img = np.pad(binary_img, pad_width=1, mode='constant', constant_values=False)
    
    # β₀: número de componentes conectados del material
    labeled_array, beta0 = label(padded_img)
    
    # β₁: número de agujeros usando análisis de conectividad del complemento
    beta1 = 0
    
    # Para cada componente del material, encontrar cuántos agujeros tiene
    for component_id in range(1, beta0 + 1):
        component_mask = (labeled_array == component_id)
        
        # Obtener el bounding box del componente
        coords = np.where(component_mask)
        if len(coords[0]) == 0:
            continue
            
        min_row, max_row = coords[0].min(), coords[0].max()
        min_col, max_col = coords[1].min(), coords[1].max()
        
        # Extraer la región del componente con padding adicional
        region_mask = component_mask[min_row:max_row+1, min_col:max_col+1]
        
        # El complemento dentro de esta región
        complement = ~region_mask
        
        # Etiquetar componentes del complemento
        labeled_holes, num_holes = label(complement)
        
        # Los agujeros son los componentes del complemento que NO tocan el borde
        holes_count = 0
        for hole_id in range(1, num_holes + 1):
            hole_mask = (labeled_holes == hole_id)
            
            # Verificar si el agujero toca el borde de la región
            touches_border = (
                np.any(hole_mask[0, :]) or    # borde superior
                np.any(hole_mask[-1, :]) or   # borde inferior
                np.any(hole_mask[:, 0]) or    # borde izquierdo
                np.any(hole_mask[:, -1])      # borde derecho
            )
            
            if not touches_border:
                holes_count += 1
        
        beta1 += holes_count
    
    return beta0, beta1

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