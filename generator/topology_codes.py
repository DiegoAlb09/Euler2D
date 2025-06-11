import numpy as np
from scipy.ndimage import label, rotate
from .topology_base import compute_betti_numbers_2d

def generate_vcc_string(N1, N3):
    """
    Genera la cadena de código VCC usando codificación cuaternaria (0,1,2,3)
    
    Args:
        N1: Número de vértices con una conexión
        N3: Número de vértices con tres conexiones
        
    Returns:
        str: Cadena que representa el código VCC en base 4
    """
    # Convertir N1 y N3 a base 4
    def to_base4(n):
        if n == 0:
            return "0"
        digits = []
        while n:
            digits.append(str(n % 4))
            n //= 4
        return "".join(reversed(digits))
    
    N1_base4 = to_base4(N1).zfill(6)  # 6 dígitos en base 4
    N3_base4 = to_base4(N3).zfill(6)
    
    # Combinar las cadenas
    vcc_string = f"{N1_base4}{N3_base4}"
    
    return vcc_string

def compute_vcc(binary_image, f4_code):
    """
    Calcula el código VCC (Vertex Correction Code) a partir del código F4
    VCC: x = (N1 - N3) / 4 = N - H (Euler-Poincaré)
    
    Args:
        binary_image: Imagen binaria donde 1=material, 0=poro
        f4_code: Código F4 de la imagen
        
    Returns:
        dict: Diccionario con los resultados del VCC
    """
    # Contar N1 y N3 para la fórmula VCC
    N1 = f4_code.count('1')  # Vértices con una conexión
    N3 = f4_code.count('3')  # Vértices con tres conexiones
    
    # Calcular x según la fórmula VCC
    x = (N1 - N3) / 4
    
    # Calcular Euler-Poincaré para verificación
    beta0, beta1 = compute_betti_numbers_2d(binary_image)
    euler_poincare = beta0 - beta1
    
    # Generar código VCC basado en la secuencia de píxeles
    vcc_sequence = ""
    prev_char = f4_code[0] if f4_code else '0'
    
    for char in f4_code:
        # Convertir de F4 a VCC usando las siguientes reglas:
        # - Si hay un cambio de dirección, es un vértice
        # - El número en VCC representa el tipo de vértice (1 o 3 conexiones)
        if char != prev_char:
            # Contar conexiones en este vértice
            connections = 1
            if char in ['1', '3']:
                connections = 3
            vcc_sequence += str(connections)
        else:
            # Si no hay cambio de dirección, usar 0
            vcc_sequence += '0'
        prev_char = char
    
    return {
        'N1': N1,
        'N3': N3,
        'x': x,
        'euler_poincare': euler_poincare,
        'is_consistent': abs(x - euler_poincare) < 1e-10,
        'code_string': vcc_sequence
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

def compute_3ot(binary_image, vcc_code):
    """
    Calcula el código 3OT (Three Orthogonal Topology) a partir del código VCC
    X = (N2h - N2v)/4 = N - H (Euler-Poincaré)
    
    Args:
        binary_image: Imagen binaria donde 1=material, 0=poro
        vcc_code: Código VCC de la imagen
        
    Returns:
        dict: Diccionario con los resultados del 3OT
    """
    # Generar código 3OT basado en la secuencia de píxeles
    ot3_sequence = ""
    prev_direction = 'h'  # Empezamos asumiendo dirección horizontal
    
    for i in range(len(vcc_code)):
        vertex_type = vcc_code[i]
        
        # Determinar dirección basada en el tipo de vértice y dirección previa
        if vertex_type in ['1', '3']:
            # Cambio de dirección en vértices
            if prev_direction == 'h':
                ot3_sequence += 'v'  # Cambio a vertical
                prev_direction = 'v'
            elif prev_direction == 'v':
                ot3_sequence += 'h'  # Cambio a horizontal
                prev_direction = 'h'
            else:
                ot3_sequence += 'd'  # Cambio a diagonal
                prev_direction = 'd'
        else:
            # Mantener dirección actual
            ot3_sequence += prev_direction
    
    # Convertir caracteres a números para consistencia
    ot3_numeric = ot3_sequence.replace('h', '0').replace('v', '1').replace('d', '2')
    
    # Calcular métricas para la fórmula 3OT
    N2h = ot3_sequence.count('h')
    N2v = ot3_sequence.count('v')
    N2d = ot3_sequence.count('d')
    
    # Calcular X según la fórmula 3OT
    X = (N2h - N2v) / 4
    
    # Calcular Euler-Poincaré para verificación
    beta0, beta1 = compute_betti_numbers_2d(binary_image)
    euler_poincare = beta0 - beta1
    
    # Información de segmentos
    horizontal_info = {
        'num_segments': N2h,
        'avg_length': N2h / (beta0 + 1) if beta0 > 0 else 0,
        'max_length': N2h
    }
    
    vertical_info = {
        'num_segments': N2v,
        'avg_length': N2v / (beta0 + 1) if beta0 > 0 else 0,
        'max_length': N2v
    }
    
    diagonal_info = {
        'num_segments': N2d,
        'avg_length': N2d / (beta0 + 1) if beta0 > 0 else 0,
        'max_length': N2d
    }
    
    # Métricas combinadas
    combined = {
        'total_segments': N2h + N2v + N2d,
        'avg_all_lengths': (horizontal_info['avg_length'] + 
                          vertical_info['avg_length'] + 
                          diagonal_info['avg_length']) / 3,
        'max_all_lengths': max(N2h, N2v, N2d),
        'directional_ratio': max(N2h, N2v, N2d) / 
                            (min(N2h, N2v, N2d) + 1e-6),
        'X_value': X,
        'euler_poincare': euler_poincare,
        'is_consistent': abs(X - euler_poincare) < 1e-10,
        'difference': abs(X - euler_poincare)
    }
    
    return {
        'horizontal': horizontal_info,
        'vertical': vertical_info,
        'diagonal': diagonal_info,
        'combined': combined,
        'code_string': ot3_numeric,
        'N2h': N2h,
        'N2v': N2v,
        'N2d': N2d,
        'debug_info': {
            'image_shape': binary_image.shape,
            'original_sequence': ot3_sequence
        }
    } 