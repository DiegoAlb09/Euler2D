import matplotlib.pyplot as plt
import numpy as np

def plot_field_with_vectors(field, vx, vy, step=10, save_path="output.png"):
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.imshow(field, cmap="gray", origin="lower")

    y, x = field.shape
    X, Y = range(0, x, step), range(0, y, step)
    X, Y = np.meshgrid(X, Y)

    U = vx[::step, ::step]
    V = vy[::step, ::step]

    ax.quiver(X, Y, U, V, color="red", pivot="middle", scale=20)

    ax.set_xticks([])
    ax.set_yticks([])
    plt.tight_layout()
    plt.savefig(save_path)
    plt.close()

def plot_vector_field_with_mask(u, v, mask, output_file):
    """
    Visualiza un campo vectorial con una máscara de porosidad
    
    Args:
        u, v: Componentes x,y del campo vectorial
        mask: Máscara binaria (1=material, 0=poro)
        output_file: Ruta donde guardar la imagen
    """
    plt.figure(figsize=(10, 10))
    
    # Crear malla de puntos
    y, x = np.mgrid[0:mask.shape[0]:1, 0:mask.shape[1]:1]
    
    # Plotear el campo vectorial
    plt.quiver(x[::5, ::5], y[::5, ::5], 
              u[::5, ::5], v[::5, ::5],
              color='blue', alpha=0.6)
    
    # Plotear la máscara
    plt.imshow(mask, cmap='gray', alpha=0.3)
    
    plt.axis('equal')
    plt.title('Campo Vectorial con Porosidad')
    plt.savefig(output_file, dpi=150, bbox_inches='tight')
    plt.close()
