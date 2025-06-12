import numpy as np
from scipy import ndimage

def compute_betti_numbers_2d(imagen_binaria):
    """
    Calcula los números de Betti β₀ (N: componentes) y β₁ (H: agujeros) 
    para una imagen binaria 2D usando etiquetado de componentes conexas.
    
    Args:
        imagen_binaria: Imagen binaria donde 1=material, 0=poro
        
    Returns:
        tuple: (β₀, β₁) números de Betti (componentes, agujeros)
    """
    # Invertimos si fondo es blanco y objetos son negros
    if imagen_binaria[0,0] == 1:
        imagen_binaria = 1 - imagen_binaria

    # Etiquetado de componentes conexas (N)
    estructura = np.array([[1,1,1],
                          [1,1,1],
                          [1,1,1]])  # conectividad-8
    componentes, num_componentes = ndimage.label(imagen_binaria, structure=estructura)

    # Etiquetar los agujeros: 1 - imagen para que los huecos sean 1
    inversa = 1 - imagen_binaria
    agujeros, num_agujeros_totales = ndimage.label(inversa, structure=estructura)

    # El agujero de fondo no cuenta, lo quitamos si toca el borde
    borde = agujeros[0,:].tolist() + agujeros[-1,:].tolist() + \
            agujeros[:,0].tolist() + agujeros[:,-1].tolist()
    agujeros_en_borde = set(borde) - {0}
    num_agujeros = num_agujeros_totales - len(agujeros_en_borde)

    return num_componentes, num_agujeros

def calcular_V_E_F(imagen_binaria):
    """
    Calcula el número de vértices (V), aristas (E) y caras (F) en una imagen binaria
    usando análisis de bloques 2x2.
    
    Args:
        imagen_binaria: Imagen binaria donde 1=material, 0=poro
        
    Returns:
        tuple: (V, E, F) número de vértices, aristas y caras
    """
    # Vértices: contamos píxeles que son "esquinas"
    V = 0
    E = 0
    F = 0
    imagen = imagen_binaria.copy()

    filas, cols = imagen.shape
    for i in range(filas - 1):
        for j in range(cols - 1):
            # Tomar bloque 2x2
            bloque = imagen[i:i+2, j:j+2].flatten()
            suma = np.sum(bloque)

            # F cuenta regiones con al menos 1 píxel activo
            if suma > 0:
                F += 1

            if suma == 1:
                V += 1
                E += 1
            elif suma == 2:
                if (bloque[0] == bloque[3] and bloque[0] == 1) or (bloque[1] == bloque[2] and bloque[1] == 1):
                    # diagonal
                    V += 2
                    E += 2
                else:
                    V += 0
                    E += 2
            elif suma == 3:
                V += 1
                E += 3
            elif suma == 4:
                E += 4

    return V, E, F

def count_vertices_edges_faces_corrected(binary_image):
    """
    Calcula el número corregido de vértices (V), aristas (E) y caras (F)
    para una imagen binaria 2D.
    
    Args:
        binary_image: Imagen binaria donde 1=material, 0=poro
        
    Returns:
        tuple: (V, E, F) número de vértices, aristas y caras
    """
    # Asegurar que la imagen sea binaria
    binary = (binary_image > 0.5).astype(np.uint8)
    
    # Calcular V, E, F usando la nueva lógica de bloques 2x2
    V, E, F = calcular_V_E_F(binary)
    
    return V, E, F

