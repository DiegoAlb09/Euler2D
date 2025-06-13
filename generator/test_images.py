import numpy as np
from skimage.draw import disk, rectangle, rectangle_perimeter

def crear_imagen_cuadrado_solido(pos, size, shape):
    """Crea una imagen con un cuadrado sólido"""
    img = np.zeros(shape, dtype=np.uint8)
    r, c = pos
    img[r:r+size, c:c+size] = 1
    return img

def crear_imagen_circulo(pos, radius, shape):
    """Crea una imagen con un círculo sólido"""
    img = np.zeros(shape, dtype=np.uint8)
    rr, cc = disk(pos, radius, shape=shape)
    img[rr, cc] = 1
    return img

def crear_imagen_dona(pos, r1, r2, shape):
    """Crea una imagen con una dona (círculo con agujero)"""
    img = np.zeros(shape, dtype=np.uint8)
    rr1, cc1 = disk(pos, r1, shape=shape)
    rr2, cc2 = disk(pos, r2, shape=shape)
    img[rr1, cc1] = 1
    img[rr2, cc2] = 0
    return img

def crear_imagen_rectangulo_hueco(pos1, pos2, shape):
    """Crea una imagen con un rectángulo hueco"""
    img = np.zeros(shape, dtype=np.uint8)
    rr1, cc1 = rectangle_perimeter(start=pos1, end=pos2, shape=shape)
    img[rr1, cc1] = 1
    r1, c1 = pos1
    r2, c2 = pos2
    inner_margin = 5
    rr2, cc2 = rectangle_perimeter(start=(r1+inner_margin, c1+inner_margin), 
                                 end=(r2-inner_margin, c2-inner_margin), 
                                 shape=shape)
    img[rr2, cc2] = 1
    return img

def crear_imagen_multiple_figuras(shape, figuras):
    """Crea una imagen combinando múltiples figuras"""
    img = np.zeros(shape, dtype=np.uint8)
    for figura in figuras:
        tipo = figura['tipo']
        if tipo == 'cuadrado':
            img += crear_imagen_cuadrado_solido(figura['pos'], figura['size'], shape)
        elif tipo == 'circulo':
            img += crear_imagen_circulo(figura['pos'], figura['radius'], shape)
        elif tipo == 'dona':
            img += crear_imagen_dona(figura['pos'], figura['r1'], figura['r2'], shape)
        elif tipo == 'rect_hueco':
            img += crear_imagen_rectangulo_hueco(figura['pos1'], figura['pos2'], shape)
    return np.clip(img, 0, 1)

def get_test_images():
    """Genera el conjunto de imágenes de prueba"""
    # Dimensión de las imágenes
    shape = (100, 100)
    
    # Lista de definiciones de imágenes
    imagenes_def = [
        {"nombre": "Cuadrado sólido", "figuras": [{"tipo": "cuadrado", "pos": (30, 30), "size": 40}]},
        {"nombre": "Círculo sólido", "figuras": [{"tipo": "circulo", "pos": (50, 50), "radius": 30}]},
        {"nombre": "Dona", "figuras": [{"tipo": "dona", "pos": (50, 50), "r1": 30, "r2": 15}]},
        {"nombre": "Rectángulo hueco", "figuras": [{"tipo": "rect_hueco", "pos1": (20, 20), "pos2": (80, 80)}]},
        {"nombre": "Dos cuadrados", "figuras": [{"tipo": "cuadrado", "pos": (20, 20), "size": 20}, {"tipo": "cuadrado", "pos": (60, 60), "size": 20}]},
        {"nombre": "Dos círculos", "figuras": [{"tipo": "circulo", "pos": (30, 30), "radius": 15}, {"tipo": "circulo", "pos": (70, 70), "radius": 15}]},
        {"nombre": "Círculo y cuadrado", "figuras": [{"tipo": "cuadrado", "pos": (20, 20), "size": 20}, {"tipo": "circulo", "pos": (70, 70), "radius": 15}]},
        {"nombre": "Círculo con hueco rectangular", "figuras": [
            {"tipo": "rect_hueco", "pos1": (20, 20), "pos2": (80, 80)},
            {"tipo": "circulo", "pos": (30, 30), "radius": 10},
            {"tipo": "circulo", "pos": (70, 30), "radius": 10},
            {"tipo": "circulo", "pos": (30, 70), "radius": 10},
            {"tipo": "circulo", "pos": (70, 70), "radius": 10}
        ]},
        {"nombre": "3 círculos", "figuras": [{"tipo": "circulo", "pos": (20, 20), "radius": 10}, {"tipo": "circulo", "pos": (50, 50), "radius": 10}, {"tipo": "circulo", "pos": (80, 80), "radius": 10}]},
        {"nombre": "3 cuadrados", "figuras": [{"tipo": "cuadrado", "pos": (10, 10), "size": 15}, {"tipo": "cuadrado", "pos": (40, 40), "size": 15}, {"tipo": "cuadrado", "pos": (70, 70), "size": 15}]},
        {"nombre": "Dos donas", "figuras": [{"tipo": "dona", "pos": (30, 30), "r1": 15, "r2": 5}, {"tipo": "dona", "pos": (70, 70), "r1": 15, "r2": 5}]},
        {"nombre": "Dona y cuadrado", "figuras": [{"tipo": "dona", "pos": (30, 30), "r1": 20, "r2": 10}, {"tipo": "cuadrado", "pos": (60, 60), "size": 20}]},
        {"nombre": "Círculo y dona", "figuras": [{"tipo": "circulo", "pos": (30, 30), "radius": 15}, {"tipo": "dona", "pos": (70, 70), "r1": 15, "r2": 7}]},
        {"nombre": "3 donas", "figuras": [{"tipo": "dona", "pos": (20, 20), "r1": 10, "r2": 4}, {"tipo": "dona", "pos": (50, 50), "r1": 10, "r2": 4}, {"tipo": "dona", "pos": (80, 80), "r1": 10, "r2": 4}]},
        {"nombre": "Rectángulo hueco y círculo", "figuras": [{"tipo": "rect_hueco", "pos1": (20, 20), "pos2": (80, 80)}, {"tipo": "circulo", "pos": (50, 50), "radius": 10}]}
    ]
    
    # Generar imágenes
    return {defn["nombre"]: crear_imagen_multiple_figuras(shape, defn["figuras"]) 
            for defn in imagenes_def}

def visualizar_imagenes_prueba(imagenes=None):
    """Visualiza las imágenes de prueba con sus características topológicas"""
    if imagenes is None:
        imagenes = get_test_images()
    
    import matplotlib.pyplot as plt
    
    # Calcular número de filas y columnas para una cuadrícula 3x5
    n_imagenes = len(imagenes)
    n_cols = 5
    n_rows = (n_imagenes + n_cols - 1) // n_cols
    
    fig, axs = plt.subplots(n_rows, n_cols, figsize=(18, 10))
    axs = axs.ravel()
    
    for i, (titulo, imagen) in enumerate(imagenes.items()):
        axs[i].imshow(imagen, cmap='gray')
        axs[i].set_title(titulo, fontsize=9)
        axs[i].axis('off')
    
    # Ocultar ejes vacíos
    for i in range(len(imagenes), len(axs)):
        axs[i].axis('off')
    
    plt.tight_layout()
    return fig 