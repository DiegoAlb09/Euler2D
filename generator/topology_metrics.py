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
    # Asegurar que sea binario
    binary_img = (binary_image > 0.5).astype(bool)
    
    # β₀: número de componentes conectados del material
    labeled_array, beta0 = label(binary_img)
    
    # β₁: número de agujeros usando el método de Euler
    # Para cada componente, contar sus agujeros
    beta1 = 0
    
    for component_id in range(1, beta0 + 1):
        component_mask = (labeled_array == component_id)
        
        # Contar agujeros en este componente usando el complemento
        # Invertir solo dentro del bounding box del componente
        props = regionprops(component_mask.astype(int))
        if props:
            minr, minc, maxr, maxc = props[0].bbox
            # Añadir padding para asegurar conectividad del fondo
            minr = max(0, minr - 1)
            minc = max(0, minc - 1)
            maxr = min(binary_img.shape[0], maxr + 1)
            maxc = min(binary_img.shape[1], maxc + 1)
            
            component_region = component_mask[minr:maxr, minc:maxc]
            inverted_region = ~component_region
            
            # Contar componentes conectados en el complemento
            _, num_background_components = label(inverted_region)
            
            # El número de agujeros es num_background_components - 1
            # (restamos 1 para no contar el fondo exterior)
            holes_in_component = max(0, num_background_components - 1)
            beta1 += holes_in_component
    
    return beta0, beta1

def count_vertices_edges_faces(binary_image):
    """
    Cuenta vértices, aristas y caras usando aproximación discreta para 2D
    
    Args:
        binary_image: Imagen binaria
        
    Returns:
        tuple: (V, E, F) vértices, aristas, caras
    """
    # Convertir a binario
    binary_img = (binary_image > 0.5).astype(bool)
    h, w = binary_img.shape
    
    # Contar caras (píxeles activos)
    F = np.sum(binary_img)
    
    # Contar aristas horizontales y verticales
    # Aristas horizontales: conexiones entre píxeles adyacentes horizontalmente
    E_horizontal = 0
    for i in range(h):
        for j in range(w - 1):
            if binary_img[i, j] and binary_img[i, j + 1]:
                E_horizontal += 1
    
    # Aristas verticales: conexiones entre píxeles adyacentes verticalmente
    E_vertical = 0
    for i in range(h - 1):
        for j in range(w):
            if binary_img[i, j] and binary_img[i + 1, j]:
                E_vertical += 1
    
    E = E_horizontal + E_vertical
    
    # Contar vértices usando la aproximación de intersecciones
    # Un vértice existe donde se encuentran píxeles activos
    V = 0
    for i in range(h - 1):
        for j in range(w - 1):
            # Contar configuraciones de 2x2 que forman vértices
            block = binary_img[i:i+2, j:j+2]
            active_pixels = np.sum(block)
            
            if active_pixels >= 1:
                # Diferentes configuraciones contribuyen diferente número de vértices
                if active_pixels == 1:
                    V += 1  # Esquina
                elif active_pixels == 2:
                    # Verificar si están en diagonal o adyacentes
                    if (block[0,0] and block[1,1]) or (block[0,1] and block[1,0]):
                        V += 2  # Diagonal
                    else:
                        V += 1  # Adyacentes
                elif active_pixels == 3:
                    V += 1  # Tres esquinas
                elif active_pixels == 4:
                    V += 1  # Bloque completo
    
    return V, E, F

def euler_characteristic_2d(binary_image):
    """
    Calcula la característica de Euler usando χ = V - E + F
    
    Args:
        binary_image: Imagen binaria
        
    Returns:
        int: Característica de Euler
    """
    V, E, F = count_vertices_edges_faces(binary_image)
    return V - E + F

def euler_poincare_2d(binary_image):
    """
    Calcula la característica de Euler usando χ = β₀ - β₁
    
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
    V, E, F = count_vertices_edges_faces(binary_image)
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
        
        # Contar agujeros en este componente
        props = regionprops(component_mask.astype(int))
        if props:
            minr, minc, maxr, maxc = props[0].bbox
            minr = max(0, minr - 1)
            minc = max(0, minc - 1)
            maxr = min(binary_img.shape[0], maxr + 1)
            maxc = min(binary_img.shape[1], maxc + 1)
            
            component_region = component_mask[minr:maxr, minc:maxc]
            inverted_region = ~component_region
            _, num_bg = label(inverted_region)
            holes = max(0, num_bg - 1)
            component_holes.append(holes)
        else:
            component_holes.append(0)
    
    return {
        'num_components': num_components,
        'component_sizes': component_sizes,
        'component_holes': component_holes,
        'largest_component_size': max(component_sizes) if component_sizes else 0,
        'total_holes': sum(component_holes)
    }