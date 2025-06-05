import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib.patches import Circle
from matplotlib.gridspec import GridSpec
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.topology_config import VISUALIZATION_CONFIG

def plot_topology_analysis(field, u, v, metrics, save_path, case_name=""):
    """
    Crea una visualización completa del análisis topológico
    
    Args:
        field: Campo escalar 2D
        u, v: Componentes del campo vectorial
        metrics: Diccionario con métricas topológicas
        save_path: Ruta donde guardar la imagen
        case_name: Nombre del caso para el título
    """
    fig = plt.figure(figsize=(15, 15))  # Aumentado para acomodar nuevos paneles
    gs = GridSpec(4, 2, figure=fig, height_ratios=[1, 1, 0.8, 1.2], hspace=0.4, wspace=0.3)
    
    # 1. Campo original con topología
    ax1 = fig.add_subplot(gs[0, 0])
    im1 = ax1.imshow(field, cmap='gray', origin='lower')
    ax1.set_title(f'Topología: {case_name}')
    ax1.set_xlabel(f'β₀={metrics["beta0"]}, β₁={metrics["beta1"]}')
    plt.colorbar(im1, ax=ax1, fraction=0.046, pad=0.04)
    
    # 2. Campo vectorial
    ax2 = fig.add_subplot(gs[0, 1])
    step = VISUALIZATION_CONFIG['vector_field_step']
    y_indices = np.arange(0, field.shape[0], step)
    x_indices = np.arange(0, field.shape[1], step)
    Y, X = np.meshgrid(y_indices, x_indices, indexing='ij')
    
    U = u[::step, ::step]
    V = v[::step, ::step]
    
    ax2.imshow(field, cmap='gray', origin='lower', alpha=0.7)
    ax2.quiver(X, Y, U, V, 
              color=VISUALIZATION_CONFIG['arrow_color'], 
              scale=VISUALIZATION_CONFIG['arrow_scale'],
              pivot='middle', alpha=0.8)
    ax2.set_title('Campo Vectorial')
    
    # 3. Análisis de Euler y VCC
    ax3 = fig.add_subplot(gs[1, 0])
    euler_data = {
        'V-E+F': metrics['euler_vef'],
        'β₀-β₁': metrics['euler_poincare'],
        'VCC': metrics['vcc']['x']
    }
    bars = ax3.bar(euler_data.keys(), euler_data.values(), 
                   color=['blue', 'orange', 'green'], alpha=0.7)
    ax3.set_title('Comparación Euler y VCC')
    ax3.set_ylabel('Característica de Euler (χ)')
    
    # Añadir valores en las barras
    for bar, value in zip(bars, euler_data.values()):
        ax3.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.05,
                f'{value:.2f}', ha='center', va='bottom', fontweight='bold')
    
    # 4. Análisis VCC detallado
    ax4 = fig.add_subplot(gs[1, 1])
    vcc = metrics['vcc']
    vcc_detail = {
        'N1': vcc['N1'],
        'N3': vcc['N3'],
        'N1-N3': vcc['N1'] - vcc['N3']
    }
    bars = ax4.bar(vcc_detail.keys(), vcc_detail.values(), 
                   color=['skyblue', 'lightcoral', 'lightgreen'], alpha=0.7)
    ax4.set_title('Análisis VCC Detallado')
    ax4.set_ylabel('Cantidad')
    
    # Añadir valores en las barras
    for bar, value in zip(bars, vcc_detail.values()):
        ax4.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.05,
                f'{value}', ha='center', va='bottom')
    
    # 5. Análisis 3OT con nueva fórmula
    ax5 = fig.add_subplot(gs[2, :])
    ot3 = metrics['3ot']
    directions = ['Horizontal (N2h)', 'Vertical (N2v)', 'Diagonal (N2d)']
    
    # Preparar datos para gráfico de barras agrupadas
    segments = [ot3['N2h'], ot3['N2v'], ot3['N2d']]
    lengths = [ot3[d.lower()]['avg_length'] for d in ['horizontal', 'vertical', 'diagonal']]
    max_lengths = [ot3[d.lower()]['max_length'] for d in ['horizontal', 'vertical', 'diagonal']]
    
    x = np.arange(len(directions))
    width = 0.25
    
    # Crear barras agrupadas
    ax5.bar(x - width, segments, width, label='Segmentos', color='skyblue')
    ax5.bar(x, lengths, width, label='Long. Media', color='lightcoral')
    ax5.bar(x + width, max_lengths, width, label='Long. Máx', color='lightgreen')
    
    ax5.set_title(f'Análisis 3OT - X = (N2h - N2v)/4 = {ot3["combined"]["X_value"]:.2f}')
    ax5.set_xticks(x)
    ax5.set_xticklabels(directions)
    ax5.legend()
    
    # Añadir valores de segmentos sobre las barras
    for i, v in enumerate(segments):
        ax5.text(i - width, v + 0.5, str(v), ha='center', va='bottom')
    
    # 6. Tabla de métricas
    ax6 = fig.add_subplot(gs[3, :])
    ax6.axis('off')
    
    # Crear tabla de métricas actualizada
    metrics_table = [
        ['Métrica', 'Valor', 'Descripción'],
        ['β₀ (Componentes)', f"{metrics['beta0']}", 'Número de componentes conectados'],
        ['β₁ (Agujeros)', f"{metrics['beta1']}", 'Número de agujeros topológicos'],
        ['χ (V-E+F)', f"{metrics['euler_vef']}", 'Característica de Euler clásica'],
        ['χ (β₀-β₁)', f"{metrics['euler_poincare']}", 'Característica de Euler-Poincaré'],
        ['VCC (x)', f"{metrics['vcc']['x']:.2f}", 'Código de Corrección de Vértices'],
        ['3OT Ratio', f"{metrics['3ot']['combined']['directional_ratio']:.2f}", 'Ratio Direccional 3OT'],
        ['Consistencia Euler', '✓' if metrics['is_consistent'] else '✗', 'Concordancia entre fórmulas'],
        ['Consistencia VCC', '✓' if metrics['vcc']['is_consistent'] else '✗', 'Concordancia VCC con Euler']
    ]
    
    table = ax6.table(cellText=metrics_table[1:], colLabels=metrics_table[0],
                     cellLoc='center', loc='center',
                     colWidths=[0.3, 0.2, 0.5])
    table.auto_set_font_size(False)
    table.set_fontsize(9)
    table.scale(1, 1.8)
    
    # Colorear encabezados y filas especiales
    for i in range(len(metrics_table[0])):
        table[(0, i)].set_facecolor('#40466e')
        table[(0, i)].set_text_props(weight='bold', color='white')
    
    # Colorear filas de consistencia
    for i in [6, 7]:
        for j in range(len(metrics_table[0])):
            table[(i, j)].set_facecolor('#f0f0f0')
    
    plt.suptitle(f'Análisis Topológico Completo - {case_name}', 
                fontsize=16, fontweight='bold')
    
    plt.savefig(save_path, dpi=VISUALIZATION_CONFIG['dpi'], 
                bbox_inches='tight', facecolor='white')
    plt.close()

def create_comparison_plot(cases_data, save_path):
    """
    Crea un gráfico comparativo de múltiples casos
    
    Args:
        cases_data: Lista de diccionarios con datos de cada caso
        save_path: Ruta donde guardar el gráfico
    """
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    
    # Preparar datos
    case_names = [case['name'] for case in cases_data]
    beta0_values = [case['metrics']['beta0'] for case in cases_data]
    beta1_values = [case['metrics']['beta1'] for case in cases_data]
    euler_values = [case['metrics']['euler_poincare'] for case in cases_data]
    consistency = [case['metrics']['is_consistent'] for case in cases_data]
    
    # 1. Números de Betti
    ax1 = axes[0, 0]
    x = np.arange(len(case_names))
    width = 0.35
    
    bars1 = ax1.bar(x - width/2, beta0_values, width, label='β₀ (Componentes)', 
                    color='skyblue', alpha=0.8)
    bars2 = ax1.bar(x + width/2, beta1_values, width, label='β₁ (Agujeros)', 
                    color='lightcoral', alpha=0.8)
    
    ax1.set_xlabel('Casos')
    ax1.set_ylabel('Número de Betti')
    ax1.set_title('Comparación de Números de Betti')
    ax1.set_xticks(x)
    ax1.set_xticklabels(case_names, rotation=45, ha='right')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Añadir valores en las barras
    for bars in [bars1, bars2]:
        for bar in bars:
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height + 0.05,
                    f'{int(height)}', ha='center', va='bottom')
    
    # 2. Característica de Euler
    ax2 = axes[0, 1]
    bars = ax2.bar(case_names, euler_values, color='gold', alpha=0.8)
    ax2.set_xlabel('Casos')
    ax2.set_ylabel('Característica de Euler (χ)')
    ax2.set_title('Característica de Euler por Caso')
    ax2.set_xticklabels(case_names, rotation=45, ha='right')
    ax2.grid(True, alpha=0.3)
    
    for bar, value in zip(bars, euler_values):
        ax2.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 0.05,
                f'{value}', ha='center', va='bottom')
    
    # 3. Consistencia de fórmulas
    ax3 = axes[1, 0]
    colors = ['green' if c else 'red' for c in consistency]
    bars = ax3.bar(case_names, [1 if c else 0 for c in consistency], 
                   color=colors, alpha=0.8)
    ax3.set_xlabel('Casos')
    ax3.set_ylabel('Consistencia')
    ax3.set_title('Consistencia entre Fórmulas de Euler')
    ax3.set_xticklabels(case_names, rotation=45, ha='right')
    ax3.set_ylim(0, 1.2)
    ax3.set_yticks([0, 1])
    ax3.set_yticklabels(['Inconsistente', 'Consistente'])
    
    # 4. Mapa de calor de métricas
    ax4 = axes[1, 1]
    
    # Crear matriz de datos para el mapa de calor
    metrics_matrix = np.array([
        beta0_values,
        beta1_values,
        euler_values,
        [case['metrics']['area_fraction'] for case in cases_data]
    ])
    
    im = ax4.imshow(metrics_matrix, cmap='viridis', aspect='auto')
    ax4.set_xticks(range(len(case_names)))
    ax4.set_xticklabels(case_names, rotation=45, ha='right')
    ax4.set_yticks(range(4))
    ax4.set_yticklabels(['β₀', 'β₁', 'χ', 'Área'])
    ax4.set_title('Mapa de Calor de Métricas')
    
    # Añadir valores en el mapa de calor
    for i in range(4):
        for j in range(len(case_names)):
            text = ax4.text(j, i, f'{metrics_matrix[i, j]:.2f}',
                           ha="center", va="center", color="white", fontweight='bold')
    
    plt.colorbar(im, ax=ax4, fraction=0.046, pad=0.04)
    
    plt.tight_layout()
    plt.savefig(save_path, dpi=VISUALIZATION_CONFIG['dpi'], 
                bbox_inches='tight', facecolor='white')
    plt.close()

def plot_vector_field_enhanced(u, v, mask, save_path, title="Campo Vectorial"):
    """
    Visualización mejorada del campo vectorial
    
    Args:
        u, v: Componentes del campo vectorial
        mask: Máscara de la topología
        save_path: Ruta donde guardar
        title: Título del gráfico
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    
    # Campo vectorial con topología
    step = VISUALIZATION_CONFIG['vector_field_step']
    y_indices = np.arange(0, mask.shape[0], step)
    x_indices = np.arange(0, mask.shape[1], step)
    Y, X = np.meshgrid(y_indices, x_indices, indexing='ij')
    
    U = u[::step, ::step]
    V = v[::step, ::step]
    
    # Subplot 1: Campo vectorial sobre topología
    ax1.imshow(mask, cmap='gray', origin='lower', alpha=0.8)
    ax1.quiver(X, Y, U, V, 
              color=VISUALIZATION_CONFIG['arrow_color'], 
              scale=VISUALIZATION_CONFIG['arrow_scale'],
              pivot='middle', alpha=0.9)
    ax1.set_title(f'{title} - Sobre Topología')
    ax1.set_xlabel('X')
    ax1.set_ylabel('Y')
    
    # Subplot 2: Magnitud del campo vectorial
    magnitude = np.sqrt(u**2 + v**2)
    im2 = ax2.imshow(magnitude, cmap='plasma', origin='lower')
    ax2.set_title('Magnitud del Campo Vectorial')
    ax2.set_xlabel('X')
    ax2.set_ylabel('Y')
    plt.colorbar(im2, ax=ax2, fraction=0.046, pad=0.04)
    
    plt.tight_layout()
    plt.savefig(save_path, dpi=VISUALIZATION_CONFIG['dpi'], 
                bbox_inches='tight', facecolor='white')
    plt.close()

def add_topology_annotations(ax, metrics):
    """
    Añade anotaciones topológicas a un gráfico
    
    Args:
        ax: Eje de matplotlib
        metrics: Diccionario con métricas
    """
    # Crear caja de texto con métricas principales
    textstr = f"""β₀ = {metrics['beta0']}
β₁ = {metrics['beta1']}
χ = {metrics['euler_poincare']}
Área = {metrics['area_fraction']:.3f}"""
    
    props = dict(boxstyle='round', facecolor='wheat', alpha=0.8)
    ax.text(0.02, 0.98, textstr, transform=ax.transAxes, fontsize=10,
            verticalalignment='top', bbox=props)

def create_individual_case_visualization(field, u, v, metrics, case_name, save_dir):
    """
    Crea visualizaciones individuales detalladas para un caso
    
    Args:
        field: Campo escalar
        u, v: Campo vectorial
        metrics: Métricas topológicas
        case_name: Nombre del caso
        save_dir: Directorio donde guardar
    """
    os.makedirs(save_dir, exist_ok=True)
    
    # 1. Topología simple
    plt.figure(figsize=(8, 8))
    plt.imshow(field, cmap='gray', origin='lower')
    plt.title(f'Topología: {case_name}')
    plt.colorbar(fraction=0.046, pad=0.04)
    plt.xlabel(f'β₀={metrics["beta0"]}, β₁={metrics["beta1"]}, χ={metrics["euler_poincare"]}')
    plt.savefig(f'{save_dir}/topology_{case_name}.png', 
                dpi=VISUALIZATION_CONFIG['dpi'], bbox_inches='tight')
    plt.close()
    
    # 2. Campo vectorial mejorado
    plot_vector_field_enhanced(u, v, field, 
                              f'{save_dir}/vector_field_{case_name}.png',
                              f'Campo Vectorial - {case_name}')
    
    # 3. Análisis completo
    plot_topology_analysis(field, u, v, metrics, 
                          f'{save_dir}/analysis_{case_name}.png', 
                          case_name)

def save_metrics_to_csv(cases_data, save_path):
    """
    Guarda las métricas en un archivo CSV
    
    Args:
        cases_data: Lista con datos de casos
        save_path: Ruta del archivo CSV
    """
    records = []
    for case in cases_data:
        record = {
            'case_name': case['name'],
            'beta0': case['metrics']['beta0'],
            'beta1': case['metrics']['beta1'],
            'vertices': case['metrics']['vertices'],
            'edges': case['metrics']['edges'],
            'faces': case['metrics']['faces'],
            'euler_vef': case['metrics']['euler_vef'],
            'euler_poincare': case['metrics']['euler_poincare'],
            'is_consistent': case['metrics']['is_consistent'],
            'area_fraction': case['metrics']['area_fraction'],
            'perimeter': case['metrics']['perimeter']
        }
        records.append(record)
    
    df = pd.DataFrame(records)
    df.to_csv(save_path, index=False)
    print(f"Métricas guardadas en: {save_path}")

def create_summary_report(cases_data, save_path):
    """
    Crea un reporte resumen en texto
    
    Args:
        cases_data: Lista con datos de casos
        save_path: Ruta del archivo de reporte
    """
    with open(save_path, 'w', encoding='utf-8') as f:
        f.write("REPORTE DE ANÁLISIS TOPOLÓGICO\n")
        f.write("=" * 50 + "\n\n")
        
        for case in cases_data:
            f.write(f"CASO: {case['name']}\n")
            f.write("-" * 30 + "\n")
            m = case['metrics']
            
            # Imprimir en terminal las cadenas de código
            print(f"\nCódigos generados para {case['name']}:")
            print(f"VCC: {m['vcc']['code_string']}")
            print(f"3OT: {m['3ot']['code_string']}")
            print("-" * 30)
            
            # Métricas básicas
            f.write(f"Números de Betti:\n")
            f.write(f"  β₀ (Componentes conectados): {m['beta0']}\n")
            f.write(f"  β₁ (Agujeros topológicos): {m['beta1']}\n")
            
            f.write(f"\nCaracterísticas de Euler:\n")
            f.write(f"  χ = V - E + F = {m['vertices']} - {m['edges']} + {m['faces']} = {m['euler_vef']}\n")
            f.write(f"  χ = β₀ - β₁ = {m['beta0']} - {m['beta1']} = {m['euler_poincare']}\n")
            
            # Análisis VCC detallado
            vcc = m['vcc']
            f.write(f"\nAnálisis VCC (Vertex Correction Code):\n")
            f.write(f"  N1 (vértices con una conexión): {vcc['N1']}\n")
            f.write(f"  N3 (vértices con tres conexiones): {vcc['N3']}\n")
            f.write(f"  N1 - N3: {vcc['N1'] - vcc['N3']}\n")
            f.write(f"  x = (N1 - N3)/4: {vcc['x']:.2f}\n")
            f.write(f"  Código binario: {vcc['code_string']}\n")
            f.write(f"  Verificación con Euler-Poincaré:\n")
            f.write(f"    VCC (x): {vcc['x']:.2f}\n")
            f.write(f"    E-P (β₀-β₁): {m['euler_poincare']}\n")
            f.write(f"    Diferencia: {abs(vcc['x'] - m['euler_poincare']):.6f}\n")
            f.write(f"    Consistencia: {'✓' if vcc['is_consistent'] else '✗'}\n")
            
            # Análisis 3OT detallado
            ot3 = m['3ot']
            f.write(f"\nAnálisis 3OT (Three Orthogonal Topology):\n")
            f.write(f"  N2h (segmentos horizontales): {ot3['N2h']}\n")
            f.write(f"  N2v (segmentos verticales): {ot3['N2v']}\n")
            f.write(f"  N2d (segmentos diagonales): {ot3['N2d']}\n")
            f.write(f"  X = (N2h - N2v)/4: {ot3['combined']['X_value']:.2f}\n")
            f.write(f"  Código binario: {ot3['code_string']}\n")
            
            # Análisis por dirección
            directions = ['Horizontal', 'Vertical', 'Diagonal']
            for dir_name, dir_key in zip(directions, ['horizontal', 'vertical', 'diagonal']):
                dir_data = ot3[dir_key]
                f.write(f"\n  Dirección {dir_name}:\n")
                f.write(f"    Número de segmentos: {dir_data['num_segments']}\n")
                f.write(f"    Longitud media: {dir_data['avg_length']:.2f}\n")
                f.write(f"    Longitud máxima: {dir_data['max_length']}\n")
                if dir_data['lengths']:
                    f.write(f"    Distribución de longitudes: {', '.join(map(str, dir_data['lengths']))}\n")
            
            # Métricas combinadas 3OT
            combined = ot3['combined']
            f.write(f"\n  Métricas Combinadas 3OT:\n")
            f.write(f"    Total de segmentos: {combined['total_segments']}\n")
            f.write(f"    Longitud media global: {combined['avg_all_lengths']:.2f}\n")
            f.write(f"    Longitud máxima global: {combined['max_all_lengths']}\n")
            f.write(f"    Ratio direccional: {combined['directional_ratio']:.2f}\n")
            
            f.write("\n" + "="*50 + "\n\n")
    
    print(f"\nReporte guardado en: {save_path}")