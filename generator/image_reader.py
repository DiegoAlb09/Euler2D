import numpy as np
from PIL import Image
import cv2
import os

def read_binary_image(image_path, threshold=127):
    """
    Lee una imagen y la convierte a binaria.
    
    Args:
        image_path: Ruta a la imagen
        threshold: Valor umbral para binarización (0-255)
        
    Returns:
        numpy.ndarray: Imagen binaria (0s y 1s)
    """
    # Normalizar la ruta del archivo
    image_path = os.path.normpath(image_path)
    
    if not os.path.exists(image_path):
        raise ValueError(f"La imagen no existe en la ruta: {image_path}")
    
    try:
        # Intentar leer con PIL primero
        with Image.open(image_path) as img:
            # Convertir a escala de grises si es necesario
            if img.mode != 'L':
                img = img.convert('L')
            # Convertir a numpy array
            img_array = np.array(img)
            print(f"Imagen leída exitosamente con PIL: {image_path}")
            print(f"Dimensiones: {img_array.shape}")
    except Exception as e:
        print(f"Error al leer con PIL: {str(e)}")
        try:
            # Intentar con OpenCV si PIL falla
            img = cv2.imread(str(image_path), cv2.IMREAD_GRAYSCALE)
            if img is None:
                raise ValueError(f"OpenCV no pudo leer la imagen: {image_path}")
            img_array = img
            print(f"Imagen leída exitosamente con OpenCV: {image_path}")
            print(f"Dimensiones: {img_array.shape}")
        except Exception as e:
            print(f"Error al leer con OpenCV: {str(e)}")
            raise ValueError(f"No se pudo leer la imagen con ningún método. Ruta: {image_path}")
    
    # Binarizar
    binary_image = (img_array > threshold).astype(np.uint8)
    
    return binary_image

def validate_binary_image(binary_image):
    """
    Valida que una imagen sea binaria y tenga el formato correcto.
    
    Args:
        binary_image: Array de numpy
        
    Returns:
        bool: True si la imagen es válida
    """
    # Verificar que sea un array de numpy
    if not isinstance(binary_image, np.ndarray):
        print("Error: La imagen no es un array de numpy")
        return False
    
    # Verificar que sea 2D
    if len(binary_image.shape) != 2:
        print(f"Error: La imagen no es 2D. Forma actual: {binary_image.shape}")
        return False
    
    # Verificar que solo contenga 0s y 1s
    unique_values = np.unique(binary_image)
    if not np.array_equal(unique_values, np.array([0, 1])) and \
       not np.array_equal(unique_values, np.array([0])) and \
       not np.array_equal(unique_values, np.array([1])):
        print(f"Error: La imagen contiene valores no binarios. Valores encontrados: {unique_values}")
        return False
    
    return True

def preprocess_binary_image(binary_image):
    """
    Preprocesa una imagen binaria para análisis topológico.
    
    Args:
        binary_image: Imagen binaria
        
    Returns:
        numpy.ndarray: Imagen binaria preprocesada
    """
    # Asegurar que sea binaria
    processed = binary_image.astype(bool).astype(np.uint8)
    
    # Eliminar ruido pequeño (opcional)
    kernel = np.ones((3,3), np.uint8)
    processed = cv2.morphologyEx(processed, cv2.MORPH_OPEN, kernel)
    processed = cv2.morphologyEx(processed, cv2.MORPH_CLOSE, kernel)
    
    return processed 