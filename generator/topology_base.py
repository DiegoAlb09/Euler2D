import numpy as np
from scipy.ndimage import label

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

