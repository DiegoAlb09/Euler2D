import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Arrow, Rectangle, FancyArrowPatch
import os

def create_base_vector_visualization(save_path):
    """
    Crea la visualización de los vectores base del código VCC
    siguiendo el formato de la imagen de referencia
    """
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(15, 4))
    fig.suptitle('Vectores base', y=1.05)
    
    # Configuración común para todos los ejes
    for ax in [ax1, ax2, ax3]:
        ax.set_xlim(-0.5, 2.5)
        ax.set_ylim(-0.5, 2.5)
        ax.grid(True)
        ax.set_aspect('equal')
        ax.axis('off')
    
    # Vector 0: Flecha horizontal
    grid1 = np.zeros((2, 2))
    grid1[0:1, 0:1] = 1
    ax1.imshow(grid1, cmap='gray', extent=[-0.5, 1.5, -0.5, 1.5])
    arrow = FancyArrowPatch((0, 0), (1, 0),
                           arrowstyle='->',
                           color='black',
                           linewidth=2)
    ax1.add_patch(arrow)
    ax1.text(-0.3, 0, '0', fontsize=12)
    
    # Vector 1: Flecha vertical
    grid2 = np.zeros((3, 2))
    grid2[0:2, 0:2] = 1
    ax2.imshow(grid2, cmap='gray', extent=[-0.5, 1.5, -0.5, 1.5])
    arrow = FancyArrowPatch((0, 0), (0, 1),
                           arrowstyle='->',
                           color='black',
                           linewidth=2)
    ax2.add_patch(arrow)
    ax2.text(-0.3, 0, '1', fontsize=12)
    
    # Vector 2: Flecha en esquina
    grid3 = np.zeros((3, 3))
    grid3[0:2, 0:2] = 1
    ax3.imshow(grid3, cmap='gray', extent=[-0.5, 1.5, -0.5, 1.5])
    arrow = FancyArrowPatch((0, 0), (0, 1),
                           arrowstyle='->',
                           color='black',
                           linewidth=2)
    ax3.add_patch(arrow)
    ax3.text(-0.3, 0, '2', fontsize=12)
    
    plt.tight_layout()
    plt.savefig(save_path, dpi=150, bbox_inches='tight')
    plt.close()

def visualize_vcc_code(field, vcc_data, save_path):
    """
    Visualiza el código VCC siguiendo el formato de la imagen de referencia
    
    Args:
        field: Campo binario original
        vcc_data: Diccionario con datos VCC
        save_path: Ruta donde guardar la imagen
    """
    # Crear directorio base_vectors si no existe
    base_vectors_dir = os.path.dirname(save_path)
    os.makedirs(base_vectors_dir, exist_ok=True)
    
    # Generar imagen de vectores base
    base_vectors_path = os.path.join(base_vectors_dir, 'vcc_base_vectors.png')
    create_base_vector_visualization(base_vectors_path)
    
    # Visualizar el campo con los vectores
    fig, ax = plt.subplots(figsize=(8, 8))
    
    # Mostrar campo binario
    ax.imshow(field, cmap='gray', origin='lower')
    
    # Recorrer el borde y añadir vectores
    h, w = field.shape
    for i in range(h):
        for j in range(w):
            if field[i, j]:
                # Determinar tipo de vector basado en vecinos
                neighbors = []
                if i > 0: neighbors.append(field[i-1, j])
                if i < h-1: neighbors.append(field[i+1, j])
                if j > 0: neighbors.append(field[i, j-1])
                if j < w-1: neighbors.append(field[i, j+1])
                
                active_neighbors = sum(neighbors)
                
                # Dibujar vector según el tipo
                if active_neighbors == 1:  # Vector tipo 0
                    arrow = FancyArrowPatch((j, i), (j+1, i),
                                          arrowstyle='->',
                                          color='black',
                                          linewidth=1)
                    ax.add_patch(arrow)
                elif active_neighbors == 2:  # Vector tipo 1
                    arrow = FancyArrowPatch((j, i), (j, i+1),
                                          arrowstyle='->',
                                          color='black',
                                          linewidth=1)
                    ax.add_patch(arrow)
                elif active_neighbors == 3:  # Vector tipo 2
                    arrow = FancyArrowPatch((j, i), (j, i+1),
                                          arrowstyle='->',
                                          color='black',
                                          linewidth=1)
                    ax.add_patch(arrow)
    
    ax.set_title('Código VCC')
    ax.axis('off')
    
    # Añadir información del código
    plt.figtext(0.02, 0.02, f"Código: {vcc_data['code_string']}", fontsize=10)
    
    plt.tight_layout()
    plt.savefig(save_path, dpi=150, bbox_inches='tight')
    plt.close()

def visualize_3ot_code(field, ot3_data, save_path):
    """
    Visualiza el código 3OT
    
    Args:
        field: Campo binario original
        ot3_data: Diccionario con datos 3OT
        save_path: Ruta donde guardar la imagen
    """
    fig = plt.figure(figsize=(15, 12))
    gs = plt.GridSpec(3, 2, height_ratios=[2, 1.5, 1])
    
    # Campo original con segmentos marcados
    ax1 = plt.subplot(gs[0, 0])
    ax1.imshow(field, cmap='gray', origin='lower')
    ax1.set_title('Campo Original con Segmentos 3OT')
    
    # Marcar segmentos horizontales
    if 'segments' in ot3_data['horizontal']:
        for segment in ot3_data['horizontal']['segments']:
            y = segment['start'][0]
            x1 = segment['start'][1]
            x2 = segment['end'][1]
            ax1.plot([x1, x2], [y, y], 'r-', linewidth=2, 
                    label='Horizontal' if segment == ot3_data['horizontal']['segments'][0] else "")
    
    # Marcar segmentos verticales
    if 'segments' in ot3_data['vertical']:
        for segment in ot3_data['vertical']['segments']:
            x = segment['start'][0]  # Nota: x e y están intercambiados por la transposición
            y1 = segment['start'][1]
            y2 = segment['end'][1]
            ax1.plot([x, x], [y1, y2], 'b-', linewidth=2,
                    label='Vertical' if segment == ot3_data['vertical']['segments'][0] else "")
    
    ax1.legend()
    
    # Histograma de longitudes de segmentos
    ax2 = plt.subplot(gs[0, 1])
    if ot3_data['horizontal']['lengths']:
        ax2.hist(ot3_data['horizontal']['lengths'], bins=10, alpha=0.5, color='red', label='Horizontal')
    if ot3_data['vertical']['lengths']:
        ax2.hist(ot3_data['vertical']['lengths'], bins=10, alpha=0.5, color='blue', label='Vertical')
    ax2.set_title('Distribución de Longitudes de Segmentos')
    ax2.set_xlabel('Longitud')
    ax2.set_ylabel('Frecuencia')
    ax2.legend()
    
    # Gráfico de barras para N2h, N2v, N2d
    ax3 = plt.subplot(gs[1, :])
    segments = ['N2h', 'N2v', 'N2d']
    values = [ot3_data['N2h'], ot3_data['N2v'], ot3_data['N2d']]
    colors = ['red', 'blue', 'green']
    
    bars = ax3.bar(segments, values, color=colors)
    ax3.set_title('Número de Segmentos por Dirección')
    
    # Añadir valores sobre las barras
    for bar in bars:
        height = bar.get_height()
        ax3.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(height)}', ha='center', va='bottom')
    
    # Información detallada
    ax4 = plt.subplot(gs[2, :])
    ax4.axis('off')
    
    combined = ot3_data['combined']
    debug_info = ot3_data['debug_info']
    
    text = f"Código 3OT: {ot3_data['code_string']}\n\n"
    text += f"Cálculo de X:\n"
    text += f"  N2h = {ot3_data['N2h']} segmentos horizontales\n"
    text += f"  N2v = {ot3_data['N2v']} segmentos verticales\n"
    text += f"  X = (N2h - N2v)/4 = ({ot3_data['N2h']} - {ot3_data['N2v']})/4 = {combined['X_value']:.2f}\n\n"
    text += f"Euler-Poincaré (N-H) = {combined['euler_poincare']}\n"
    text += f"¿Coinciden? {'✓' if combined['is_consistent'] else '✗'} "
    text += f"(diferencia: {combined['difference']:.6f})\n\n"
    text += f"Información adicional:\n"
    text += f"  Tamaño de imagen: {debug_info['image_shape']}\n"
    text += f"  Longitud media horizontal: {ot3_data['horizontal']['avg_length']:.2f}\n"
    text += f"  Longitud media vertical: {ot3_data['vertical']['avg_length']:.2f}\n"
    
    ax4.text(0.05, 1.0, text, fontsize=10, va='top', family='monospace')
    
    plt.tight_layout()
    plt.savefig(save_path, dpi=150, bbox_inches='tight')
    plt.close()

def save_code_visualizations(field, metrics, output_dir, case_name):
    """
    Guarda las visualizaciones de los códigos VCC y 3OT
    
    Args:
        field: Campo binario original
        metrics: Diccionario con métricas incluyendo VCC y 3OT
        output_dir: Directorio de salida
        case_name: Nombre del caso
    """
    os.makedirs(output_dir, exist_ok=True)
    
    # Visualizar VCC
    vcc_path = os.path.join(output_dir, f'vcc_{case_name}.png')
    visualize_vcc_code(field, metrics['vcc'], vcc_path)
    
    # Visualizar 3OT
    ot3_path = os.path.join(output_dir, f'3ot_{case_name}.png')
    visualize_3ot_code(field, metrics['3ot'], ot3_path) 