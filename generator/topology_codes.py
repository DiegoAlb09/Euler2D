import numpy as np
from scipy.ndimage import label, rotate
from .topology_base import compute_betti_numbers_2d

def generate_vcc_string(N1, N3):
    """
    Genera la cadena de código VCC usando codificación ternaria (0,1,2)
    
    Args:
        N1: Número de vértices con una conexión
        N3: Número de vértices con tres conexiones
        
    Returns:
        str: Cadena que representa el código VCC en base 3
    """
    # Convertir N1 y N3 a base 3
    def to_base3(n):
        if n == 0:
            return "0"
        digits = []
        while n:
            digits.append(str(n % 3))
            n //= 3
        return "".join(reversed(digits))
    
    N1_base3 = to_base3(N1).zfill(6)  # 6 dígitos en base 3
    N3_base3 = to_base3(N3).zfill(6)
    
    # Combinar las cadenas
    vcc_string = f"{N1_base3}{N3_base3}"
    
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
    Genera la cadena de código 3OT usando codificación ternaria (0,1,2)
    
    Args:
        N2h: Número de segmentos horizontales
        N2v: Número de segmentos verticales
        N2d: Número de segmentos diagonales
        
    Returns:
        str: Cadena que representa el código 3OT en base 3
    """
    # Convertir cada valor a base 3
    def to_base3(n):
        if n == 0:
            return "0"
        digits = []
        while n:
            digits.append(str(n % 3))
            n //= 3
        return "".join(reversed(digits))
    
    N2h_base3 = to_base3(N2h).zfill(6)
    N2v_base3 = to_base3(N2v).zfill(6)
    N2d_base3 = to_base3(N2d).zfill(6)
    
    # Combinar las cadenas
    ot3_string = f"{N2h_base3}{N2v_base3}{N2d_base3}"
    
    return ot3_string

def compute_3ot(binary_image):
    """
    Calcula el código 3OT (Three Orthogonal Topology)
    X = (N2h - N2v)/4 = N - H (Euler-Poincaré)
    
    Args:
        binary_image: Imagen binaria donde 1=material, 0=poro
        
    Returns:
        dict: Diccionario con los resultados del 3OT
    """
    # Asegurar que la imagen sea binaria
    binary = (binary_image > 0.5).astype(bool)
    h, w = binary.shape
    
    def find_segments_with_neighbors(img):
        """
        Encuentra segmentos conectados considerando vecinos
        Retorna lista de segmentos con sus coordenadas y longitudes
        """
        segments = []
        h, w = img.shape
        visited = np.zeros_like(img, dtype=bool)
        
        def is_valid_segment(i, j, direction='h'):
            """Verifica si un píxel puede ser parte de un segmento"""
            if not img[i, j] or visited[i, j]:
                return False
                
            # Verificar vecinos perpendiculares
            if direction == 'h':
                # Para segmentos horizontales, verificar vecinos arriba y abajo
                has_vertical_neighbor = False
                if i > 0:
                    has_vertical_neighbor = has_vertical_neighbor or img[i-1, j]
                if i < h-1:
                    has_vertical_neighbor = has_vertical_neighbor or img[i+1, j]
                return not has_vertical_neighbor
            else:
                # Para segmentos verticales, verificar vecinos izquierda y derecha
                has_horizontal_neighbor = False
                if j > 0:
                    has_horizontal_neighbor = has_horizontal_neighbor or img[i, j-1]
                if j < w-1:
                    has_horizontal_neighbor = has_horizontal_neighbor or img[i, j+1]
                return not has_horizontal_neighbor
        
        # Buscar segmentos horizontales
        for i in range(h):
            start = None
            for j in range(w):
                if is_valid_segment(i, j, 'h'):
                    if start is None:
                        start = j
                    visited[i, j] = True
                elif start is not None:
                    segments.append({
                        'start': (i, start),
                        'end': (i, j-1),
                        'length': j - start,
                        'direction': 'h'
                    })
                    start = None
            if start is not None:
                segments.append({
                    'start': (i, start),
                    'end': (i, w-1),
                    'length': w - start,
                    'direction': 'h'
                })
        
        # Reiniciar visited para segmentos verticales
        visited = np.zeros_like(img, dtype=bool)
        
        # Buscar segmentos verticales
        for j in range(w):
            start = None
            for i in range(h):
                if is_valid_segment(i, j, 'v'):
                    if start is None:
                        start = i
                    visited[i, j] = True
                elif start is not None:
                    segments.append({
                        'start': (j, start),
                        'end': (j, i-1),
                        'length': i - start,
                        'direction': 'v'
                    })
                    start = None
            if start is not None:
                segments.append({
                    'start': (j, start),
                    'end': (j, h-1),
                    'length': h - start,
                    'direction': 'v'
                })
        
        return segments
    
    # Análisis horizontal y vertical
    segments = find_segments_with_neighbors(binary)
    
    # Separar segmentos horizontales y verticales
    horizontal_segments = [s for s in segments if s['direction'] == 'h']
    vertical_segments = [s for s in segments if s['direction'] == 'v']
    
    N2h = len(horizontal_segments)
    N2v = len(vertical_segments)
    
    horizontal_lengths = [seg['length'] for seg in horizontal_segments]
    vertical_lengths = [seg['length'] for seg in vertical_segments]
    
    # Análisis diagonal (45°)
    h_pad = w
    w_pad = h
    diagonal_img = np.zeros((h_pad + w_pad, h_pad + w_pad), dtype=bool)
    
    start_h = h_pad // 2
    start_w = w_pad // 2
    diagonal_img[start_h:start_h+h, start_w:start_w+w] = binary
    
    rotated = rotate(diagonal_img.astype(float), 45, reshape=True)
    rotated = (rotated > 0.5)
    
    diagonal_segments = find_segments_with_neighbors(rotated)
    N2d = len([s for s in diagonal_segments if s['direction'] == 'h'])  # Solo contar una dirección
    diagonal_lengths = [seg['length'] for seg in diagonal_segments]
    
    # Calcular X según la fórmula 3OT
    X = (N2h - N2v) / 4
    
    # Calcular Euler-Poincaré para verificación
    beta0, beta1 = compute_betti_numbers_2d(binary)
    euler_poincare = beta0 - beta1
    
    # Verificar relación con Euler-Poincaré
    is_consistent = abs(X - euler_poincare) < 1e-10
    
    # Generar cadena 3OT
    ot3_string = generate_3ot_string(N2h, N2v, N2d)
    
    # Información detallada de segmentos
    horizontal_info = {
        'segments': horizontal_segments,
        'num_segments': N2h,
        'lengths': horizontal_lengths,
        'avg_length': np.mean(horizontal_lengths) if horizontal_lengths else 0,
        'max_length': max(horizontal_lengths) if horizontal_lengths else 0
    }
    
    vertical_info = {
        'segments': vertical_segments,
        'num_segments': N2v,
        'lengths': vertical_lengths,
        'avg_length': np.mean(vertical_lengths) if vertical_lengths else 0,
        'max_length': max(vertical_lengths) if vertical_lengths else 0
    }
    
    diagonal_info = {
        'segments': diagonal_segments,
        'num_segments': N2d,
        'lengths': diagonal_lengths,
        'avg_length': np.mean(diagonal_lengths) if diagonal_lengths else 0,
        'max_length': max(diagonal_lengths) if diagonal_lengths else 0
    }
    
    # Métricas combinadas
    combined = {
        'total_segments': N2h + N2v + N2d,
        'avg_all_lengths': np.mean([horizontal_info['avg_length'], 
                                  vertical_info['avg_length'], 
                                  diagonal_info['avg_length']]),
        'max_all_lengths': max(horizontal_info['max_length'], 
                             vertical_info['max_length'], 
                             diagonal_info['max_length']),
        'directional_ratio': max(N2h, N2v, N2d) / 
                            (min(N2h, N2v, N2d) + 1e-6),
        'X_value': X,
        'euler_poincare': euler_poincare,
        'is_consistent': is_consistent,
        'difference': abs(X - euler_poincare)
    }
    
    return {
        'horizontal': horizontal_info,
        'vertical': vertical_info,
        'diagonal': diagonal_info,
        'combined': combined,
        'code_string': ot3_string,
        'N2h': N2h,
        'N2v': N2v,
        'N2d': N2d,
        'debug_info': {
            'image_shape': binary.shape,
            'rotated_shape': rotated.shape,
            'horizontal_segments_detail': [f"({s['start']} -> {s['end']}, len={s['length']})" for s in horizontal_segments],
            'vertical_segments_detail': [f"({s['start']} -> {s['end']}, len={s['length']})" for s in vertical_segments]
        }
    } 