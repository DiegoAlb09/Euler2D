import numpy as np
from skimage.draw import disk, rectangle_perimeter

def crear_imagen_cuadrado_solido(tamaño=100):
    """
    Crea una imagen binaria con un cuadrado sólido (χ=1)
    
    Args:
        tamaño: Tamaño de la imagen (cuadrada)
        
    Returns:
        numpy.ndarray: Imagen binaria con un cuadrado sólido
    """
    img = np.zeros((tamaño, tamaño), dtype=np.uint8)
    img[30:70, 30:70] = 1
    return img

def crear_imagen_circulo_hueco(tamaño=100):
    """
    Crea una imagen binaria con un círculo hueco (χ=0)
    
    Args:
        tamaño: Tamaño de la imagen (cuadrada)
        
    Returns:
        numpy.ndarray: Imagen binaria con un círculo hueco
    """
    img = np.zeros((tamaño, tamaño), dtype=np.uint8)
    rr1, cc1 = disk((50, 50), 30)
    rr2, cc2 = disk((50, 50), 15)
    img[rr1, cc1] = 1
    img[rr2, cc2] = 0
    return img

def crear_imagen_dos_circulos(tamaño=100):
    """
    Crea una imagen binaria con dos círculos sólidos (χ=2)
    
    Args:
        tamaño: Tamaño de la imagen (cuadrada)
        
    Returns:
        numpy.ndarray: Imagen binaria con dos círculos
    """
    img = np.zeros((tamaño, tamaño), dtype=np.uint8)
    rr1, cc1 = disk((30, 30), 15)
    rr2, cc2 = disk((70, 70), 15)
    img[rr1, cc1] = 1
    img[rr2, cc2] = 1
    return img

def crear_imagen_letra_O(tamaño=100):
    """
    Crea una imagen binaria con forma de letra 'O' (χ=0)
    
    Args:
        tamaño: Tamaño de la imagen (cuadrada)
        
    Returns:
        numpy.ndarray: Imagen binaria con forma de 'O'
    """
    img = np.zeros((tamaño, tamaño), dtype=np.uint8)
    rr1, cc1 = rectangle_perimeter(start=(30, 30), end=(70, 70), shape=img.shape)
    img[rr1, cc1] = 1
    rr2, cc2 = rectangle_perimeter(start=(40, 40), end=(60, 60), shape=img.shape)
    img[rr2, cc2] = 1
    return img

def get_test_images():
    """
    Genera un conjunto de imágenes de prueba con diferentes características topológicas.
    
    Returns:
        dict: Diccionario con las imágenes y sus descripciones
    """
    return {
        "Cuadrado sólido (χ=1)": crear_imagen_cuadrado_solido(),
        "Círculo con agujero (χ=0)": crear_imagen_circulo_hueco(),
        "Dos círculos (χ=2)": crear_imagen_dos_circulos(),
        "Letra 'O' (χ=0)": crear_imagen_letra_O()
    }

def visualizar_imagenes_prueba(imagenes=None):
    """
    Visualiza las imágenes de prueba con sus características topológicas.
    
    Args:
        imagenes: Diccionario de imágenes a visualizar. Si es None, usa get_test_images()
    """
    if imagenes is None:
        imagenes = get_test_images()
    
    import matplotlib.pyplot as plt
    
    fig, axs = plt.subplots(1, len(imagenes), figsize=(4*len(imagenes), 4))
    for ax, (titulo, imagen) in zip(axs, imagenes.items()):
        ax.imshow(imagen, cmap='gray')
        ax.set_title(titulo)
        ax.axis('off')
    
    plt.tight_layout()
    return fig 