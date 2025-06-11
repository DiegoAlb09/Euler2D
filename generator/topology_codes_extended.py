import numpy as np

def get_f8_code(binary_image):
    """
    Genera el código F8 a partir de una imagen binaria.
    El código F8 considera los 8 vecinos de cada píxel.
    
    Args:
        binary_image: Imagen binaria donde 1=material, 0=poro
        
    Returns:
        str: Cadena que representa el código F8
    """
    h, w = binary_image.shape
    code = []
    
    for i in range(1, h-1):
        for j in range(1, w-1):
            if binary_image[i, j]:
                # Obtener los 8 vecinos
                neighbors = [
                    binary_image[i-1, j-1], binary_image[i-1, j], binary_image[i-1, j+1],
                    binary_image[i, j-1],                         binary_image[i, j+1],
                    binary_image[i+1, j-1], binary_image[i+1, j], binary_image[i+1, j+1]
                ]
                # Contar vecinos activos
                active_neighbors = sum(neighbors)
                code.append(str(active_neighbors))
    
    return ''.join(code)

def f8_to_f4(f8_code):
    """
    Convierte el código F8 a F4 considerando solo los 4 vecinos principales.
    
    Args:
        f8_code: Código F8 como string
        
    Returns:
        str: Código F4
    """
    f4_code = []
    for digit in f8_code:
        # Convertir el dígito F8 a un valor F4 aproximado
        f8_value = int(digit)
        # Mapeo aproximado de 8 vecinos a 4 vecinos
        if f8_value <= 2:
            f4_value = 1
        elif f8_value <= 4:
            f4_value = 2
        elif f8_value <= 6:
            f4_value = 3
        else:
            f4_value = 4
        f4_code.append(str(f4_value))
    
    return ''.join(f4_code)

def normalize_code_length(vcc_code, ot3_code, target_length=None):
    """
    Normaliza la longitud de los códigos VCC y 3OT.
    
    Args:
        vcc_code: Código VCC
        ot3_code: Código 3OT
        target_length: Longitud objetivo (opcional)
        
    Returns:
        tuple: (vcc_normalizado, ot3_normalizado)
    """
    if target_length is None:
        # Usar la longitud más larga
        target_length = max(len(vcc_code), len(ot3_code))
    
    # Función para extender un código
    def extend_code(code, length):
        if len(code) >= length:
            return code[:length]
        # Extender repitiendo el patrón
        pattern = code
        while len(code) < length:
            code += pattern[:length - len(code)]
        return code
    
    # Normalizar ambos códigos
    vcc_normalized = extend_code(vcc_code, target_length)
    ot3_normalized = extend_code(ot3_code, target_length)
    
    return vcc_normalized, ot3_normalized

def verify_euler_equalities(metrics):
    """
    Verifica las igualdades de las fórmulas de Euler.
    
    Args:
        metrics: Diccionario con las métricas topológicas
        
    Returns:
        dict: Resultados de la verificación
    """
    # Extraer valores
    euler_vef = metrics['euler_vef']  # V - E + F
    euler_poincare = metrics['euler_poincare']  # β₀ - β₁
    vcc_x = metrics['vcc']['x']  # (N1 - N3)/4
    ot3_x = metrics['3ot']['combined']['X_value']  # (N2h - N2v)/4
    
    # Calcular diferencias
    tolerancia = 1e-10
    diferencias = {
        'euler_vs_poincare': abs(euler_vef - euler_poincare),
        'euler_vs_vcc': abs(euler_vef - vcc_x),
        'euler_vs_3ot': abs(euler_vef - ot3_x),
        'vcc_vs_3ot': abs(vcc_x - ot3_x)
    }
    
    # Verificar igualdades
    verificaciones = {
        'euler_vs_poincare': diferencias['euler_vs_poincare'] < tolerancia,
        'euler_vs_vcc': diferencias['euler_vs_vcc'] < tolerancia,
        'euler_vs_3ot': diferencias['euler_vs_3ot'] < tolerancia,
        'vcc_vs_3ot': diferencias['vcc_vs_3ot'] < tolerancia
    }
    
    return {
        'diferencias': diferencias,
        'verificaciones': verificaciones,
        'todas_igualdades_cumplen': all(verificaciones.values())
    } 