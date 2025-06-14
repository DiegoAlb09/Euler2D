import numpy as np
import cv2
from .topology_base import compute_betti_numbers_2d

def get_f8_code(binary_image):
    """
    Genera el código F8 (Freeman) a partir de una imagen binaria.
    El código F8 considera los 8 vecinos y genera una cadena de direcciones.
    
    Args:
        binary_image: Imagen binaria donde 1=material, 0=poro
        
    Returns:
        str: Cadena que representa el código F8 de Freeman
    """
    # Tabla de movimientos relativos y su código Freeman (8 direcciones)
    freeman_table = {
        (1, 0): '0',    # Este
        (1, -1): '1',   # Noreste
        (0, -1): '2',   # Norte
        (-1, -1): '3',  # Noroeste
        (-1, 0): '4',   # Oeste
        (-1, 1): '5',   # Suroeste
        (0, 1): '6',    # Sur
        (1, 1): '7'     # Sureste
    }
    
    def freeman_chain_code(contorno):
        """Genera el código Freeman para un contorno dado"""
        code = []
        for i in range(len(contorno) - 1):
            y1, x1 = contorno[i][0][1], contorno[i][0][0]
            y2, x2 = contorno[i + 1][0][1], contorno[i + 1][0][0]
            dy = y2 - y1
            dx = x2 - x1
            direction = (dx, dy)
            if direction in freeman_table:
                code.append(freeman_table[direction])
        return ''.join(code)
    
    # Asegurar que la imagen sea del tipo correcto
    binary_image = binary_image.astype(np.uint8) * 255
    
    # Encontrar contornos (tanto externos como internos)
    contours, hierarchy = cv2.findContours(binary_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    
    # Si no hay contornos, retornar cadena vacía
    if not contours:
        return ''
    
    # Obtener el código Freeman para cada contorno
    f8_codes = []
    for i, contour in enumerate(contours):
        # Verificar si es un contorno válido (área > 0)
        if cv2.contourArea(contour) > 0:
            code = freeman_chain_code(contour)
            if code:  # Solo añadir códigos no vacíos
                f8_codes.append(code)
    
    # Unir todos los códigos en orden
    return ''.join(f8_codes)

def f8_to_f4(f8_code, metodo='filtrar'):
    """
    Convierte el código F8 a F4 usando un método específico de conversión.
    
    Args:
        f8_code: Código F8 como string
        metodo: Método de conversión ('aproximar' o 'filtrar')
        
    Returns:
        str: Código F4
    """
    if metodo == 'aproximar':
        # Mapeo que aproxima las diagonales a la dirección más cercana
        mapa_f8_f4 = {
            '0': '0',  # Este (→)
            '1': '0',  # Noreste (↗) → Este (→)
            '2': '2',  # Norte (↑)
            '3': '2',  # Noroeste (↖) → Norte (↑)
            '4': '4',  # Oeste (←)
            '5': '4',  # Suroeste (↙) → Oeste (←)
            '6': '6',  # Sur (↓)
            '7': '6'   # Sureste (↘) → Sur (↓)
        }
    elif metodo == 'filtrar':
        # Mapeo que solo mantiene las direcciones principales
        mapa_f8_f4 = {
            '0': '0',  # Este (→)
            '2': '2',  # Norte (↑)
            '4': '4',  # Oeste (←)
            '6': '6'   # Sur (↓)
        }
    else:
        raise ValueError(f"Método de conversión '{metodo}' no válido. Use 'aproximar' o 'filtrar'.")
    
    # Convertir cada dígito del código F8
    codigo_f4 = []
    for digito in f8_code:
        if digito in mapa_f8_f4:
            codigo_f4.append(mapa_f8_f4[digito])
    
    # Unir los dígitos en una cadena
    return ''.join(codigo_f4)

def compute_euler_from_freeman_chain(f8_code):
    """
    Calcula la característica de Euler usando rotaciones del código Freeman F8,
    como se describe en el artículo.

    Args:
        f8_code (str): Código de contorno Freeman (cadena de números 0–7)

    Returns:
        float: Característica de Euler χ
    """
    if not f8_code or len(f8_code) < 2:
        return 0.0

    directions = [int(c) for c in f8_code]
    total_rotation = 0

    for i in range(1, len(directions)):
        diff = (directions[i] - directions[i - 1]) % 8
        if diff == 1 or diff == 2 or diff == 3:
            total_rotation += 1
        elif diff == 5 or diff == 6 or diff == 7:
            total_rotation -= 1
        elif diff == 4:
            total_rotation += 0  # giro de 180° no cambia χ

    return total_rotation / 4.0


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

def compute_vcc(binary_image, f4_code):
    """
    Calcula el código VCC (Vertex Correction Code) a partir del código F4.
    El VCC se basa en los cambios de dirección entre segmentos consecutivos:
    0: sin cambio (recto)
    1: giro a la izquierda
    -1: giro a la derecha
    2: giro de 180°
    
    Args:
        binary_image: Imagen binaria donde 1=material, 0=poro
        f4_code: Código F4 de la imagen
        
    Returns:
        dict: Diccionario con los resultados del VCC
    """
    def freeman4_to_vcc(codigo_f4):
        """Convierte código F4 a VCC basado en cambios de dirección"""
        vcc = []
        # Convertir string a lista de enteros
        f4_nums = [int(d) for d in codigo_f4]
        
        for i in range(1, len(f4_nums)):
            anterior = f4_nums[i - 1]
            actual = f4_nums[i]
            # Calcular la diferencia de dirección (rotación circular)
            diferencia = (actual - anterior) % 8
            
            # Mapear las diferencias a los códigos VCC
            if diferencia == 0:
                vcc.append('0')    # recto
            elif diferencia == 2:
                vcc.append('1')    # giro a la izquierda (+1)
            elif diferencia == 6:
                vcc.append('-1')   # giro a la derecha (-1)
            else:
                vcc.append('2')    # giro de 180° (cambio brusco)
        
        return vcc
    
    def calcular_N1_N3(vcc):
        """
        Calcula N1 y N3 según la definición:
        - N1: número de vértices para el que VCC=1
        - N3: número de vértices para el que VCC=2
        
        Args:
            vcc: Lista de códigos VCC
            
        Returns:
            tuple: (N1, N3) número de vértices con VCC=1 y VCC=2 respectivamente
        """
        N1 = sum(1 for giro in vcc if giro == '1')  # Vértices con VCC=1
        N3 = sum(1 for giro in vcc if giro == '2')  # Vértices con VCC=2
        return N1, N3
    
    # Generar el código VCC como lista
    vcc_list = freeman4_to_vcc(f4_code)
    
    # Calcular N1 y N3
    N1, N3 = calcular_N1_N3(vcc_list)
    
    # Calcular x según la fórmula VCC
    x = (N1 - N3) / 4
    
    # Calcular Euler-Poincaré para verificación
    beta0, beta1 = compute_betti_numbers_2d(binary_image)
    euler_poincare = beta0 - beta1
    
    # Convertir la lista VCC a string para mantener compatibilidad
    vcc_code = ''.join(str(x) if x != '-1' else '3' for x in vcc_list)
    
    return {
        'N1': N1,
        'N3': N3,
        'x': x,
        'euler_poincare': euler_poincare,
        'is_consistent': abs(x - euler_poincare) < 1e-10,
        'code_string': vcc_code
    }

def vcc_to_3ot(vcc_code):
    """
    Convierte código VCC a 3OT basado en la dirección de los segmentos.
    El código 3OT clasifica los segmentos en:
    H: horizontal (movimiento horizontal dominante)
    V: vertical (movimiento vertical dominante)
    D: diagonal (movimiento diagonal)
    
    Args:
        vcc_code: Código VCC de la imagen
        
    Returns:
        list: Lista de direcciones (H, V, D)
    """
    ot3 = []
    # Determinar dirección inicial basada en el primer segmento
    if vcc_code[0] == '0':  # Sin cambio
        current_direction = 'H'
    elif vcc_code[0] == '1':  # Giro izquierda
        current_direction = 'V'
    elif vcc_code[0] == '3':  # Giro derecha
        current_direction = 'D'
    else:  # Giro 180°
        current_direction = 'H'
    
    ot3.append(current_direction)
    
    # Mapeo de transiciones de dirección
    transitions = {
        'H': {'0': 'H', '1': 'V', '3': 'D', '2': 'H'},  # Desde horizontal
        'V': {'0': 'V', '1': 'D', '3': 'H', '2': 'V'},  # Desde vertical
        'D': {'0': 'D', '1': 'H', '3': 'V', '2': 'D'}   # Desde diagonal
    }
    
    # Procesar el resto del código
    for i in range(1, len(vcc_code)):
        vertex_type = vcc_code[i]
        current_direction = transitions[current_direction][vertex_type]
        ot3.append(current_direction)
    
    return ot3

def calcular_N2h_N2v(ot3, ventana=5):
    """
    Calcula N2h y N2v como la cantidad de ventanas en las que hay predominancia
    horizontal (H) o vertical (V) en secuencias de 5 direcciones.
    """
    N2h = 0
    N2v = 0
    for i in range(len(ot3) - ventana + 1):
        ventana_actual = ot3[i:i + ventana]
        h = ventana_actual.count('H')
        v = ventana_actual.count('V')
        
        if h >= 3 and h > v:
            N2h += 1
        elif v >= 3 and v > h:
            N2v += 1

    return N2h, N2v


def compute_3ot(binary_image, vcc_code):
    """
    Calcula el código 3OT (Three Orthogonal Topology) a partir del código VCC.
    El código 3OT clasifica los segmentos en:
    H: horizontal (movimiento horizontal dominante)
    V: vertical (movimiento vertical dominante)
    D: diagonal (movimiento diagonal)
    
    La característica de Euler χ se calcula como:
    χ = (N2h - N2v)/4
    
    Donde:
    - N2h: número de patrones horizontales dominantes
    - N2v: número de patrones verticales dominantes
    
    Args:
        binary_image: Imagen binaria donde 1=material, 0=poro
        vcc_code: Código VCC de la imagen
        
    Returns:
        dict: Diccionario con los resultados del 3OT
    """
    # Generar código 3OT como lista
    ot3_list = vcc_to_3ot(vcc_code)
    
    # Calcular N2h y N2v según los patrones
    N2h, N2v = calcular_N2h_N2v(ot3_list)
    
    # Contar segmentos diagonales
    N2d = ot3_list.count('D')
    
    # Calcular X según la fórmula 3OT
    X = (N2h - N2v) / 4
    
    # Calcular Euler-Poincaré para verificación
    beta0, beta1 = compute_betti_numbers_2d(binary_image)
    euler_poincare = beta0 - beta1
    
    # Convertir la lista 3OT a string para mantener compatibilidad
    ot3_code = ''.join('0' if x == 'H' else '1' if x == 'V' else '2' for x in ot3_list)
    
    # Información de segmentos por dirección
    horizontal_info = {
        'num_segments': N2h,
        'avg_length': N2h / (beta0 + 1) if beta0 > 0 else 0,
        'max_length': N2h,
        'lengths': [N2h]
    }
    
    vertical_info = {
        'num_segments': N2v,
        'avg_length': N2v / (beta0 + 1) if beta0 > 0 else 0,
        'max_length': N2v,
        'lengths': [N2v]
    }
    
    diagonal_info = {
        'num_segments': N2d,
        'avg_length': N2d / (beta0 + 1) if beta0 > 0 else 0,
        'max_length': N2d,
        'lengths': [N2d]
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
    print("Código VCC:", vcc_code)
    print("Código 3OT:", ''.join(ot3_list))
    print("Direcciones únicas en 3OT:", set(ot3_list))
    print("N2h:", N2h, "N2v:", N2v)

    
    return {
        'horizontal': horizontal_info,
        'vertical': vertical_info,
        'diagonal': diagonal_info,
        'combined': combined,
        'code_string': ot3_code,
        'N2h': N2h,
        'N2v': N2v,
        'N2d': N2d
    } 