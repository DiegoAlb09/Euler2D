import numpy as np
from scipy.ndimage import label, rotate
from .topology_base import compute_betti_numbers_2d

def generate_vcc_string(N1, N3):
    """
    Genera la cadena de código VCC
    
    Args:
        N1: Número de vértices con una conexión
        N3: Número de vértices con tres conexiones
        
    Returns:
        str: Cadena que representa el código VCC
    """
    # Convertir N1 y N3 a binario y eliminar el '0b' del inicio
    N1_bin = bin(N1)[2:].zfill(8)  # Asegurar 8 bits
    N3_bin = bin(N3)[2:].zfill(8)
    
    # Combinar las cadenas binarias
    vcc_string = f"{N1_bin}{N3_bin}"
    
    return vcc_string

def compute_vcc(binary_image):
    """
    Calcula el código VCC (Vertex Correction Code)
    VCC: x = (N1 - N3) / 4 = N - H (Euler-Poincaré)
    
    Args:
        binary_image: Imagen binaria donde 1=material, 0=poro
        
    Returns:
        dict: Diccionario con los resultados del VCC
            - N1: Número de vértices con una conexión
            - N3: Número de vértices con tres conexiones
            - x: Valor del código VCC
            - euler_poincare: Valor de N-H (β₀-β₁)
    """
    # Asegurar que la imagen sea binaria
    binary = (binary_image > 0.5).astype(bool)
    h, w = binary.shape
    
    # Inicializar contadores
    N1 = 0  # Vértices con una conexión
    N3 = 0  # Vértices con tres conexiones
    
    # Analizar cada vértice y sus conexiones
    for i in range(h + 1):
        for j in range(w + 1):
            # Obtener los 4 píxeles adyacentes al vértice
            pixels = []
            
            # Superior izquierdo
            if i > 0 and j > 0:
                pixels.append(binary[i-1, j-1])
            else:
                pixels.append(False)
            
            # Superior derecho
            if i > 0 and j < w:
                pixels.append(binary[i-1, j])
            else:
                pixels.append(False)
            
            # Inferior izquierdo
            if i < h and j > 0:
                pixels.append(binary[i, j-1])
            else:
                pixels.append(False)
            
            # Inferior derecho
            if i < h and j < w:
                pixels.append(binary[i, j])
            else:
                pixels.append(False)
            
            # Contar conexiones activas
            active_pixels = sum(pixels)
            
            if active_pixels == 1:
                N1 += 1
            elif active_pixels == 3:
                N3 += 1
    
    # Calcular x según la fórmula VCC
    x = (N1 - N3) / 4
    
    # Calcular Euler-Poincaré para verificación
    beta0, beta1 = compute_betti_numbers_2d(binary)
    euler_poincare = beta0 - beta1
    
    # Generar cadena VCC
    vcc_string = generate_vcc_string(N1, N3)
    
    return {
        'N1': N1,
        'N3': N3,
        'x': x,
        'euler_poincare': euler_poincare,
        'is_consistent': abs(x - euler_poincare) < 1e-10,
        'code_string': vcc_string
    }

def generate_3ot_string(N2h, N2v, N2d):
    """
    Genera la cadena de código 3OT
    
    Args:
        N2h: Número de segmentos horizontales
        N2v: Número de segmentos verticales
        N2d: Número de segmentos diagonales
        
    Returns:
        str: Cadena que representa el código 3OT
    """
    # Convertir cada valor a binario y asegurar 8 bits
    N2h_bin = bin(N2h)[2:].zfill(8)
    N2v_bin = bin(N2v)[2:].zfill(8)
    N2d_bin = bin(N2d)[2:].zfill(8)
    
    # Combinar las cadenas binarias
    ot3_string = f"{N2h_bin}{N2v_bin}{N2d_bin}"
    
    return ot3_string

def compute_3ot(binary_image):
    """
    Calcula el código 3OT (Three Orthogonal Topology)
    X = (N2h - N2v)/4
    
    Args:
        binary_image: Imagen binaria donde 1=material, 0=poro
        
    Returns:
        dict: Diccionario con los resultados del 3OT
    """
    # Asegurar que la imagen sea binaria
    binary = (binary_image > 0.5).astype(bool)
    h, w = binary.shape
    
    def analyze_direction(img):
        """Analiza una dirección específica"""
        labeled, num_components = label(img)
        
        lengths = []
        for i in range(1, num_components + 1):
            segment = (labeled == i)
            length = np.sum(segment)
            lengths.append(length)
        
        return {
            'num_segments': len(lengths),
            'avg_length': np.mean(lengths) if lengths else 0,
            'max_length': np.max(lengths) if lengths else 0,
            'lengths': lengths
        }
    
    # Análisis horizontal (0°)
    horizontal = analyze_direction(binary)
    N2h = horizontal['num_segments']
    
    # Análisis vertical (90°)
    vertical = analyze_direction(binary.T)
    N2v = vertical['num_segments']
    
    # Análisis diagonal (45°)
    h_pad = w
    w_pad = h
    diagonal_img = np.zeros((h_pad + w_pad, h_pad + w_pad), dtype=bool)
    
    start_h = h_pad // 2
    start_w = w_pad // 2
    diagonal_img[start_h:start_h+h, start_w:start_w+w] = binary
    
    rotated = rotate(diagonal_img.astype(float), 45, reshape=True)
    rotated = (rotated > 0.5)
    
    diagonal = analyze_direction(rotated)
    N2d = diagonal['num_segments']
    
    # Calcular X según la nueva fórmula
    X = (N2h - N2v) / 4
    
    # Generar cadena 3OT
    ot3_string = generate_3ot_string(N2h, N2v, N2d)
    
    # Métricas combinadas
    combined = {
        'total_segments': N2h + N2v + N2d,
        'avg_all_lengths': np.mean([horizontal['avg_length'], 
                                  vertical['avg_length'], 
                                  diagonal['avg_length']]),
        'max_all_lengths': max(horizontal['max_length'], 
                             vertical['max_length'], 
                             diagonal['max_length']),
        'directional_ratio': max(N2h, N2v, N2d) / 
                            (min(N2h, N2v, N2d) + 1e-6),
        'X_value': X
    }
    
    return {
        'horizontal': horizontal,
        'vertical': vertical,
        'diagonal': diagonal,
        'combined': combined,
        'code_string': ot3_string,
        'N2h': N2h,
        'N2v': N2v,
        'N2d': N2d
    } 