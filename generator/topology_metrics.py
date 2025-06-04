import numpy as np
from scipy.ndimage import label, binary_erosion

def euler_characteristic(binary_image):
    labeled_array, num_features = label(binary_image)

    # Vértices, Aristas y Caras usando aproximación basada en conteo de bloques
    F = np.sum(binary_image)
    V = np.sum(binary_image[1:, 1:] & binary_image[:-1, 1:] & binary_image[1:, :-1] & binary_image[:-1, :-1])
    E = np.sum(binary_image[:, 1:] & binary_image[:, :-1]) + np.sum(binary_image[1:, :] & binary_image[:-1, :])

    χ = F - E + V
    return χ

def euler_poincare(binary_image):
    # β₀ = número de componentes conectados
    labeled_array, beta0 = label(binary_image)

    # β₁ = número de huecos internos
    inverted = ~binary_image.astype(bool)
    eroded = binary_erosion(inverted)
    labeled_holes, beta1 = label(eroded)

    return beta0 - beta1

def compute_betti_numbers(binary_image):
    """
    Calcula los números de Betti β0 y β1 para una imagen binaria 2D
    
    Args:
        binary_image: Imagen binaria donde 1=material, 0=poro
        
    Returns:
        beta0: Número de componentes conectados
        beta1: Número de agujeros
    """
    # β0: número de componentes conectados
    labeled_array, beta0 = label(binary_image)
    
    # β1: número de agujeros (usando complemento)
    # En 2D, los agujeros son componentes conectados en el complemento menos 1
    complement = ~binary_image.astype(bool)
    _, num_holes = label(complement)
    beta1 = num_holes - 1  # Restamos 1 para no contar el "agujero" exterior
    
    return beta0, max(0, beta1)  # Aseguramos que β1 no sea negativo
