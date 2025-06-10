import numpy as np
from scipy.ndimage import gaussian_filter
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.topology_config import TOPOLOGY_CONFIG

# All pattern generation functions are defined in this file

def generate_topology_case(case_name, size=(256, 256), seed=None):
    """
    Genera un caso específico de topología
    
    Args:
        case_name: Nombre del caso a generar
        size: Tamaño de la imagen
        seed: Semilla para reproducibilidad
        
    Returns:
        Array 2D binario con la topología especificada
    """
    if seed is not None:
        np.random.seed(seed)
    
    # Map case names to their generation functions
    topology_cases = {
        'single_blob': create_single_blob,
        'blob_with_hole': lambda s: create_single_blob_with_holes(s, num_holes=1),
        'blob_with_three_holes': lambda s: create_single_blob_with_holes(s, num_holes=3),
        'two_blobs': lambda s: create_multiple_blobs(s, num_blobs=2),
        'two_blobs_one_hole': create_two_blobs_one_with_hole,
        'complex_topology': create_complex_topology,
        'irregular_star': create_irregular_star,
        'irregular_chain': create_irregular_chain,
        'irregular_mesh': create_irregular_mesh,
        'irregular_clusters': create_irregular_clusters,
        'spiral_holes': create_spiral_holes,
        'horizontal_dominant': create_horizontal_dominant,
        'vertical_dominant': create_vertical_dominant,
        'asymmetric_mesh': create_asymmetric_mesh,
        'asymmetric_spiral': create_asymmetric_spiral,
        'asymmetric_branches': create_asymmetric_branches
    }
    
    if case_name not in topology_cases:
        raise ValueError(f"Caso desconocido: {case_name}")
        
    # Call the generation function with the specified size
    return topology_cases[case_name](size)

def create_single_blob(size):
    """Crea un blob único sin agujeros"""
    center_x = size[1] // 2
    center_y = size[0] // 2
    radius = min(size) // 4
    
    blob = create_blob((center_x, center_y), radius, size, smooth=False)
    return blob

def create_single_blob_with_holes(size, num_holes=3):
    """
    Crea un blob con agujeros internos - VERSIÓN CORREGIDA
    
    Args:
        size: Tamaño de la imagen
        num_holes: Número de agujeros a crear
        
    Returns:
        Array 2D con el blob y agujeros
    """
    # Crear blob principal más grande para acomodar agujeros
    center_x = size[1] // 2
    center_y = size[0] // 2
    blob_radius = int(min(size) * 0.35)  # Blob más grande
    
    field = create_blob((center_x, center_y), blob_radius, size, smooth=False)
    
    # Configuración para agujeros
    hole_radius = max(8, blob_radius // 6)  # Agujeros más pequeños pero visibles
    min_distance_from_center = hole_radius + 5
    max_distance_from_center = blob_radius - hole_radius - 5
    min_distance_between_holes = hole_radius * 2.2
    
    # Generar posiciones para agujeros usando distribución angular
    hole_positions = []
    
    if num_holes == 1:
        # Un agujero en el centro
        hole_positions.append((center_x, center_y))
    else:
        # Múltiples agujeros distribuidos
        for i in range(num_holes):
            attempts = 0
            max_attempts = 50
            
            while attempts < max_attempts:
                # Posición angular uniforme
                angle = (2 * np.pi * i / num_holes) + np.random.uniform(-0.3, 0.3)
                
                # Distancia del centro
                if num_holes <= 3:
                    distance = np.random.uniform(min_distance_from_center, 
                                               max_distance_from_center * 0.7)
                else:
                    distance = np.random.uniform(min_distance_from_center, 
                                               max_distance_from_center * 0.6)
                
                hole_x = center_x + distance * np.cos(angle)
                hole_y = center_y + distance * np.sin(angle)
                
                # Verificar límites
                if (hole_radius < hole_x < size[1] - hole_radius and 
                    hole_radius < hole_y < size[0] - hole_radius):
                    
                    # Verificar distancia con otros agujeros
                    valid = True
                    for hx, hy in hole_positions:
                        dist = np.sqrt((hole_x - hx)**2 + (hole_y - hy)**2)
                        if dist < min_distance_between_holes:
                            valid = False
                            break
                    
                    if valid:
                        hole_positions.append((hole_x, hole_y))
                        break
                
                attempts += 1
            
            # Si no se pudo colocar, usar posición de respaldo
            if len(hole_positions) <= i:
                backup_angle = 2 * np.pi * i / num_holes
                backup_distance = (min_distance_from_center + max_distance_from_center) / 2
                backup_x = center_x + backup_distance * np.cos(backup_angle)
                backup_y = center_y + backup_distance * np.sin(backup_angle)
                hole_positions.append((backup_x, backup_y))
    
    # Crear agujeros
    for hole_x, hole_y in hole_positions:
        hole = create_hole((hole_x, hole_y), hole_radius, size)
        field = field * (1 - hole)  # Restar agujero del campo
    
    # Asegurar que el resultado sea binario
    field = (field > 0.5).astype(float)
    
    return field

def create_multiple_blobs(size, num_blobs=2):
    """
    Crea múltiples blobs separados - VERSIÓN CORREGIDA
    
    Args:
        size: Tamaño de la imagen
        num_blobs: Número de blobs a crear
        
    Returns:
        Array 2D con múltiples blobs
    """
    blob_radius = min(size) // 7  # Blobs más pequeños para evitar superposición
    min_distance = blob_radius * 2.5
    
    # Generar posiciones más controladas
    positions = []
    
    if num_blobs == 2:
        # Dos blobs: uno a la izquierda, otro a la derecha
        left_x = size[1] // 4
        right_x = 3 * size[1] // 4
        center_y = size[0] // 2
        
        positions = [(left_x, center_y), (right_x, center_y)]
    else:
        positions = get_safe_positions(size, num_blobs, blob_radius, min_distance)
    
    field = np.zeros(size)
    for x, y in positions:
        blob = create_blob((x, y), blob_radius, size, smooth=False)
        field = np.maximum(field, blob)  # Unión de blobs
    
    return field

def create_two_blobs_one_with_hole(size):
    """Crea dos blobs, uno de ellos con un agujero - VERSIÓN CORREGIDA"""
    blob_radius = min(size) // 6
    
    # Posiciones fijas para mejor control
    left_x = size[1] // 4
    right_x = 3 * size[1] // 4
    center_y = size[0] // 2
    
    positions = [(left_x, center_y), (right_x, center_y)]
    
    field = np.zeros(size)
    
    # Primer blob sin agujero
    blob1 = create_blob(positions[0], blob_radius, size, smooth=False)
    field = np.maximum(field, blob1)
    
    # Segundo blob con agujero
    blob2 = create_blob(positions[1], blob_radius, size, smooth=False)
    
    # Crear agujero en el segundo blob
    hole_radius = max(6, blob_radius // 4)
    hole = create_hole(positions[1], hole_radius, size)
    blob2 = blob2 * (1 - hole)
    
    field = np.maximum(field, blob2)
    
    # Asegurar resultado binario
    field = (field > 0.5).astype(float)
    
    return field

def create_complex_topology(size):
    """
    Crea una topología compleja con múltiples características - VERSIÓN CORREGIDA
    
    Expected: β₀=3, β₁=2, χ=1
    """
    field = np.zeros(size)
    
    # Tres blobs con posiciones controladas
    blob_radius = min(size) // 8
    
    # Posiciones en triángulo
    center_x, center_y = size[1] // 2, size[0] // 2
    offset = min(size) // 4
    
    positions = [
        (center_x, center_y - offset),      # Blob superior
        (center_x - offset, center_y + offset//2),  # Blob inferior izquierdo
        (center_x + offset, center_y + offset//2)   # Blob inferior derecho
    ]
    
    # Primer blob: sin agujero
    blob1 = create_blob(positions[0], blob_radius, size, smooth=False)
    field = np.maximum(field, blob1)
    
    # Segundo blob: con un agujero
    blob2 = create_blob(positions[1], blob_radius, size, smooth=False)
    hole_radius = max(5, blob_radius // 4)
    hole2 = create_hole(positions[1], hole_radius, size)
    blob2 = blob2 * (1 - hole2)
    field = np.maximum(field, blob2)
    
    # Tercer blob: con un agujero
    blob3 = create_blob(positions[2], blob_radius, size, smooth=False)
    hole_radius = max(5, blob_radius // 4)
    hole3 = create_hole(positions[2], hole_radius, size)
    blob3 = blob3 * (1 - hole3)
    field = np.maximum(field, blob3)
    
    # Asegurar resultado binario
    field = (field > 0.5).astype(float)
    
    return field

def create_irregular_star(size):
    """Crea una forma de estrella irregular con agujeros"""
    center_x = size[1] // 2
    center_y = size[0] // 2
    radius = min(size) // 4
    
    # Crear puntas irregulares
    field = np.zeros(size)
    num_points = 7  # Número impar para asimetría
    
    for i in range(num_points):
        angle = 2 * np.pi * i / num_points
        length = radius * (1 + 0.5 * np.random.random())
        width = radius * 0.3 * (1 + 0.5 * np.random.random())
        
        end_x = int(center_x + length * np.cos(angle))
        end_y = int(center_y + length * np.sin(angle))
        
        # Crear punta irregular
        blob = create_blob((end_x, end_y), width, size, smooth=True)
        field = np.maximum(field, blob)
    
    # Añadir agujeros irregulares
    for i in range(4):
        angle = 2 * np.pi * (i + 0.5) / 4
        dist = radius * 0.6
        hole_x = int(center_x + dist * np.cos(angle))
        hole_y = int(center_y + dist * np.sin(angle))
        
        hole_radius = radius * 0.2 * (1 + 0.3 * np.random.random())
        hole = create_hole((hole_x, hole_y), hole_radius, size)
        field = field * (1 - hole)
    
    return (field > 0.5).astype(float)

def create_irregular_chain(size):
    """Crea una cadena de blobs irregulares conectados"""
    field = np.zeros(size)
    num_blobs = 5
    base_radius = min(size) // 12
    
    # Crear camino serpenteante
    x = size[1] // 4
    y = size[0] // 2
    for i in range(num_blobs):
        # Blob principal
        radius = base_radius * (1 + 0.3 * np.random.random())
        blob = create_blob((x, y), radius, size, smooth=True)
        field = np.maximum(field, blob)
        
        # Conexión al siguiente blob
        if i < num_blobs - 1:
            next_x = x + base_radius * 2 * (1 + 0.2 * np.random.random())
            next_y = y + base_radius * (np.random.random() - 0.5)
            
            # Crear conexión
            connection = create_blob(((x + next_x)//2, (y + next_y)//2), 
                                   base_radius * 0.5, size, smooth=True)
            field = np.maximum(field, connection)
            
            x, y = next_x, next_y
    
    # Añadir agujeros
    for _ in range(3):
        hole_x = np.random.randint(size[1]//4, 3*size[1]//4)
        hole_y = np.random.randint(size[0]//3, 2*size[0]//3)
        hole_radius = base_radius * 0.6
        hole = create_hole((hole_x, hole_y), hole_radius, size)
        field = field * (1 - hole)
    
    return (field > 0.5).astype(float)

def create_irregular_mesh(size):
    """Crea una malla irregular con múltiples agujeros"""
    field = np.zeros(size)
    base_radius = min(size) // 16
    
    # Crear grid irregular de puntos
    points = []
    for i in range(4):
        for j in range(4):
            x = size[1]//5 + (size[1]*3//5) * i//3 + np.random.randint(-base_radius, base_radius)
            y = size[0]//5 + (size[0]*3//5) * j//3 + np.random.randint(-base_radius, base_radius)
            points.append((x, y))
    
    # Conectar puntos
    for i, (x1, y1) in enumerate(points):
        for j, (x2, y2) in enumerate(points[i+1:], i+1):
            if np.random.random() < 0.4:  # 40% de probabilidad de conexión
                mid_x = (x1 + x2) // 2
                mid_y = (y1 + y2) // 2
                
                # Crear conexión irregular
                connection = create_blob((mid_x, mid_y), base_radius, size, smooth=True)
                field = np.maximum(field, connection)
    
    # Añadir nodos en las intersecciones
    for x, y in points:
        node = create_blob((x, y), base_radius * 1.2, size, smooth=True)
        field = np.maximum(field, node)
    
    # Añadir agujeros en espacios vacíos
    for _ in range(6):
        hole_x = np.random.randint(size[1]//4, 3*size[1]//4)
        hole_y = np.random.randint(size[0]//4, 3*size[0]//4)
        
        if field[hole_y, hole_x] > 0.5:  # Si hay material
            hole_radius = base_radius * 1.5
            hole = create_hole((hole_x, hole_y), hole_radius, size)
            field = field * (1 - hole)
    
    return (field > 0.5).astype(float)

def create_irregular_clusters(size):
    """Crea clusters irregulares con conexiones"""
    field = np.zeros(size)
    base_radius = min(size) // 10
    
    # Crear tres clusters principales
    cluster_centers = [
        (size[1]//4, size[0]//4),
        (3*size[1]//4, size[0]//4),
        (size[1]//2, 3*size[0]//4)
    ]
    
    # Generar cada cluster
    for cx, cy in cluster_centers:
        # Blob principal del cluster
        main_blob = create_blob((cx, cy), base_radius * 1.5, size, smooth=True)
        field = np.maximum(field, main_blob)
        
        # Añadir blobs satélite
        for _ in range(3):
            angle = 2 * np.pi * np.random.random()
            dist = base_radius * (1 + 0.5 * np.random.random())
            x = int(cx + dist * np.cos(angle))
            y = int(cy + dist * np.sin(angle))
            
            satellite = create_blob((x, y), base_radius * 0.7, size, smooth=True)
            field = np.maximum(field, satellite)
    
    # Añadir conexiones entre clusters
    for i, (x1, y1) in enumerate(cluster_centers):
        for x2, y2 in cluster_centers[i+1:]:
            if np.random.random() < 0.5:  # 50% de probabilidad de conexión
                connection = create_blob(((x1+x2)//2, (y1+y2)//2), 
                                      base_radius * 0.4, size, smooth=True)
                field = np.maximum(field, connection)
    
    # Añadir agujeros
    for _ in range(4):
        hole_x = np.random.randint(size[1]//4, 3*size[1]//4)
        hole_y = np.random.randint(size[0]//4, 3*size[0]//4)
        
        if field[hole_y, hole_x] > 0.5:
            hole_radius = base_radius * 0.8
            hole = create_hole((hole_x, hole_y), hole_radius, size)
            field = field * (1 - hole)
    
    return (field > 0.5).astype(float)

def create_spiral_holes(size):
    """Crea una espiral con agujeros distribuidos"""
    field = np.zeros(size)
    center_x = size[1] // 2
    center_y = size[0] // 2
    max_radius = min(size) // 3
    
    # Crear espiral
    theta = np.linspace(0, 6*np.pi, 200)
    r = np.linspace(max_radius * 0.2, max_radius, len(theta))
    
    # Generar puntos de la espiral
    points = []
    for t, rad in zip(theta, r):
        x = int(center_x + rad * np.cos(t))
        y = int(center_y + rad * np.sin(t))
        points.append((x, y))
    
    # Crear la espiral con blobs conectados
    base_radius = max_radius * 0.15
    for i, (x, y) in enumerate(points):
        if i % 5 == 0:  # Reducir densidad de puntos
            blob = create_blob((x, y), base_radius, size, smooth=True)
            field = np.maximum(field, blob)
    
    # Añadir agujeros siguiendo un patrón espiral interno
    hole_theta = np.linspace(0, 4*np.pi, 5)
    hole_r = np.linspace(max_radius * 0.3, max_radius * 0.8, len(hole_theta))
    
    for t, rad in zip(hole_theta, hole_r):
        x = int(center_x + rad * np.cos(t))
        y = int(center_y + rad * np.sin(t))
        
        hole_radius = base_radius * 1.2
        hole = create_hole((x, y), hole_radius, size)
        field = field * (1 - hole)
    
    return (field > 0.5).astype(float)

def generate_vector_field(field):
    """
    Genera un campo vectorial basado en el gradiente del campo escalar
    
    Args:
        field: Campo escalar 2D
        
    Returns:
        Tupla (u, v) con componentes del campo vectorial
    """
    # Suavizar el campo para mejores gradientes
    smoothed_field = gaussian_filter(field.astype(float), sigma=2.0)
    
    # Calcular gradiente
    grad_y, grad_x = np.gradient(smoothed_field)
    
    # Normalizar y añadir componente rotacional para visualización
    norm = np.sqrt(grad_x**2 + grad_y**2) + 1e-8
    
    # Campo vectorial normalizado con componente tangencial
    u = grad_x / norm + 0.3 * (-grad_y / norm)
    v = grad_y / norm + 0.3 * (grad_x / norm)
    
    # Aplicar máscara del campo original
    mask = field > 0.1
    u = u * mask
    v = v * mask
    
    return u, v

def add_noise_to_field(field, noise_level=0.05):
    """
    Añade ruido controlado al campo para hacerlo más realista
    
    Args:
        field: Campo original
        noise_level: Nivel de ruido (0-1)
        
    Returns:
        Campo con ruido añadido
    """
    noise = np.random.normal(0, noise_level, field.shape)
    noisy_field = field + noise
    return np.clip(noisy_field, 0, 1)

# Functions moved from case_definitions.py to avoid circular imports
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

def create_horizontal_dominant(size):
    """
    Crea una topología con dominancia de segmentos horizontales
    """
    field = np.zeros(size)
    
    # Crear varios segmentos horizontales de diferentes longitudes
    y_positions = [size[0]//4, size[0]//2, 3*size[0]//4]
    lengths = [size[1]//2, 3*size[1]//4, size[1]//3]
    
    for y, length in zip(y_positions, lengths):
        start_x = np.random.randint(0, size[1] - length)
        field[y, start_x:start_x+length] = 1
    
    # Añadir algunos segmentos verticales más cortos para conectividad
    x_positions = [size[1]//3, 2*size[1]//3]
    for x in x_positions:
        start_y = np.random.randint(size[0]//4, 3*size[0]//4)
        length = size[0]//6
        field[start_y:start_y+length, x] = 1
    
    return field

def create_vertical_dominant(size):
    """
    Crea una topología con dominancia de segmentos verticales
    """
    field = np.zeros(size)
    
    # Crear varios segmentos verticales de diferentes longitudes
    x_positions = [size[1]//4, size[1]//2, 3*size[1]//4]
    lengths = [size[0]//2, 3*size[0]//4, size[0]//3]
    
    for x, length in zip(x_positions, lengths):
        start_y = np.random.randint(0, size[0] - length)
        field[start_y:start_y+length, x] = 1
    
    # Añadir algunos segmentos horizontales más cortos para conectividad
    y_positions = [size[0]//3, 2*size[0]//3]
    for y in y_positions:
        start_x = np.random.randint(size[1]//4, 3*size[1]//4)
        length = size[1]//6
        field[y, start_x:start_x+length] = 1
    
    return field

def create_asymmetric_mesh(size):
    """
    Crea una malla asimétrica con más segmentos en una dirección
    """
    field = np.zeros(size)
    
    # Más líneas horizontales que verticales
    h_spacing = size[0] // 6
    v_spacing = size[1] // 4
    
    # Líneas horizontales con variación
    for i in range(1, 6):
        y = i * h_spacing
        length = size[1] - np.random.randint(0, size[1]//4)
        start_x = np.random.randint(0, size[1]//4)
        field[y, start_x:start_x+length] = 1
    
    # Menos líneas verticales
    for i in range(1, 4):
        x = i * v_spacing
        length = size[0] - np.random.randint(0, size[0]//4)
        start_y = np.random.randint(0, size[0]//4)
        field[start_y:start_y+length, x] = 1
    
    return field

def create_asymmetric_spiral(size):
    """
    Crea una espiral asimétrica con segmentos de diferentes longitudes
    """
    field = np.zeros(size)
    center = (size[0]//2, size[1]//2)
    max_radius = min(size) // 3
    
    # Crear espiral con segmentos asimétricos
    radius = max_radius
    angle = 0
    while radius > max_radius//4:
        # Segmento horizontal más largo
        x1 = int(center[1] + radius * np.cos(angle))
        x2 = int(center[1] + radius * 1.5 * np.cos(angle))
        y = int(center[0] + radius * np.sin(angle))
        if 0 <= y < size[0]:
            x_min, x_max = max(0, min(x1, x2)), min(size[1], max(x1, x2))
            field[y, x_min:x_max] = 1
        
        # Segmento vertical más corto
        x = int(center[1] + radius * np.cos(angle + np.pi/2))
        y1 = int(center[0] + radius * np.sin(angle + np.pi/2))
        y2 = int(center[0] + radius * 0.7 * np.sin(angle + np.pi/2))
        if 0 <= x < size[1]:
            y_min, y_max = max(0, min(y1, y2)), min(size[0], max(y1, y2))
            field[y_min:y_max, x] = 1
        
        radius -= max_radius//8
        angle += np.pi/2
    
    return field

def create_asymmetric_branches(size):
    """
    Crea una estructura ramificada asimétrica
    """
    field = np.zeros(size)
    
    # Tronco principal vertical
    trunk_x = size[1]//2
    field[:, trunk_x] = 1
    
    # Ramas horizontales de diferentes longitudes
    y_positions = [size[0]//4, size[0]//2, 3*size[0]//4]
    lengths = [size[1]//2, 3*size[1]//4, size[1]//3]
    
    for y, length in zip(y_positions, lengths):
        # Rama hacia la derecha
        field[y, trunk_x:trunk_x+length] = 1
        
        # Algunas ramas más cortas hacia la izquierda
        left_length = length//2
        field[y, trunk_x-left_length:trunk_x] = 1
        
        # Añadir algunas ramas verticales pequeñas
        for x in [trunk_x + length//2, trunk_x - left_length//2]:
            if 0 <= x < size[1]:
                vert_length = size[0]//8
                start_y = max(0, y - vert_length//2)
                end_y = min(size[0], y + vert_length//2)
                field[start_y:end_y, x] = 1
    
    return field
