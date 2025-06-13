import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.patches import Circle
from matplotlib.gridspec import GridSpec
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.topology_config import VISUALIZATION_CONFIG
import cv2

# Configuración global de estilo para todas las visualizaciones
plt.style.use('default')

# Colores personalizados para visualizaciones
COLORS = {
    'background': '#f0f0f0',
    'bar_colors': {
        '0': '#3498db',  # Azul
        '1': '#e74c3c',  # Rojo
        '2': '#2ecc71'   # Verde
    },
    'comparison': {
        'beta0': '#3498db',    # Azul
        'beta1': '#e74c3c',    # Rojo
        'euler': '#f1c40f',    # Amarillo
        'consistent': '#2ecc71',# Verde
        'inconsistent': '#e74c3c'  # Rojo
    }
}

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
    fig.patch.set_facecolor('white')
    gs = GridSpec(4, 2, figure=fig, height_ratios=[1, 1, 0.8, 1.2], hspace=0.4, wspace=0.3)
    
    # 1. Campo original con topología
    ax1 = fig.add_subplot(gs[0, 0])
    ax1.set_facecolor(COLORS['background'])
    im1 = ax1.imshow(field, cmap='gray', origin='lower')
    ax1.set_title(f'Topología: {case_name}', fontsize=12, fontweight='bold')
    ax1.set_xlabel(f'β₀={metrics["beta0"]}, β₁={metrics["beta1"]}', fontsize=10, fontweight='bold')
    plt.colorbar(im1, ax=ax1, fraction=0.046, pad=0.04)
    
    # 2. Campo vectorial
    ax2 = fig.add_subplot(gs[0, 1])
    ax2.set_facecolor(COLORS['background'])
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
    ax2.set_title('Campo Vectorial', fontsize=12, fontweight='bold')
    
    # 3. Análisis de Euler y VCC
    ax3 = fig.add_subplot(gs[1, 0])
    ax3.set_facecolor(COLORS['background'])
    euler_data = {
        'V-E+F': metrics['euler_vef'],
        'β₀-β₁': metrics['euler_poincare'],
        'VCC': metrics['vcc']['x']
    }
    bars = ax3.bar(euler_data.keys(), euler_data.values(), 
                   color=[COLORS['comparison']['beta0'], 
                         COLORS['comparison']['beta1'],
                         COLORS['comparison']['euler']], 
                   alpha=0.8, edgecolor='black', linewidth=1)
    ax3.set_title('Comparación Euler y VCC', fontsize=12, fontweight='bold')
    ax3.set_ylabel('Característica de Euler (χ)', fontsize=10, fontweight='bold')
    ax3.grid(True, linestyle='--', alpha=0.3)
    
    # Añadir valores en las barras
    for bar, value in zip(bars, euler_data.values()):
        ax3.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.05,
                f'{value:.2f}', ha='center', va='bottom', fontweight='bold')
    
    # 4. Análisis VCC detallado
    ax4 = fig.add_subplot(gs[1, 1])
    ax4.set_facecolor(COLORS['background'])
    vcc = metrics['vcc']
    vcc_detail = {
        'N1': vcc['N1'],
        'N3': vcc['N3'],
        'N1-N3': vcc['N1'] - vcc['N3']
    }
    bars = ax4.bar(vcc_detail.keys(), vcc_detail.values(), 
                   color=[COLORS['bar_colors']['0'], 
                         COLORS['bar_colors']['1'],
                         COLORS['bar_colors']['2']], 
                   alpha=0.8, edgecolor='black', linewidth=1)
    ax4.set_title('Análisis VCC Detallado', fontsize=12, fontweight='bold')
    ax4.set_ylabel('Cantidad', fontsize=10, fontweight='bold')
    ax4.grid(True, linestyle='--', alpha=0.3)
    
    # Añadir valores en las barras
    for bar, value in zip(bars, vcc_detail.values()):
        ax4.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.05,
                f'{value}', ha='center', va='bottom', fontweight='bold')
    
    # 5. Análisis 3OT con nueva fórmula
    ax5 = fig.add_subplot(gs[2, :])
    ax5.set_facecolor(COLORS['background'])
    ot3 = metrics['3ot']
    directions = ['Horizontal (N2h)', 'Vertical (N2v)', 'Diagonal (N2d)']
    
    # Preparar datos para gráfico de barras agrupadas
    segments = [ot3['N2h'], ot3['N2v'], ot3['N2d']]
    lengths = [ot3[d.lower()]['avg_length'] for d in ['horizontal', 'vertical', 'diagonal']]
    max_lengths = [ot3[d.lower()]['max_length'] for d in ['horizontal', 'vertical', 'diagonal']]
    
    x = np.arange(len(directions))
    width = 0.25
    
    # Crear barras agrupadas
    ax5.bar(x - width, segments, width, label='Segmentos', 
            color=COLORS['bar_colors']['0'], edgecolor='black', linewidth=1)
    ax5.bar(x, lengths, width, label='Long. Media', 
            color=COLORS['bar_colors']['1'], edgecolor='black', linewidth=1)
    ax5.bar(x + width, max_lengths, width, label='Long. Máx', 
            color=COLORS['bar_colors']['2'], edgecolor='black', linewidth=1)
    
    ax5.set_title(f'Análisis 3OT - X = (N2h - N2v)/4 = {ot3["combined"]["X_value"]:.2f}',
                  fontsize=12, fontweight='bold')
    ax5.set_xticks(x)
    ax5.set_xticklabels(directions, fontsize=10)
    ax5.legend(fontsize=10)
    ax5.grid(True, linestyle='--', alpha=0.3)
    
    # Añadir valores de segmentos sobre las barras
    for i, v in enumerate(segments):
        ax5.text(i - width, v + 0.5, str(v), ha='center', va='bottom', fontweight='bold')
    
    # 6. Tabla de métricas
    ax6 = fig.add_subplot(gs[3, :])
    ax6.set_facecolor(COLORS['background'])
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
            if j == 1:  # Columna de valor
                color = COLORS['comparison']['consistent'] if '✓' in metrics_table[i+1][1] else COLORS['comparison']['inconsistent']
                table[(i, j)].set_facecolor(color)
                table[(i, j)].set_text_props(color='white', weight='bold')
    
    plt.suptitle(f'Análisis Topológico Completo - {case_name}', 
                fontsize=16, fontweight='bold', y=1.02)
    
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
    fig.patch.set_facecolor('white')
    
    # Preparar datos
    case_names = [case['name'] for case in cases_data]
    beta0_values = [case['metrics']['beta0'] for case in cases_data]
    beta1_values = [case['metrics']['beta1'] for case in cases_data]
    euler_values = [case['metrics']['euler_poincare'] for case in cases_data]
    consistency = [case['metrics']['is_consistent'] for case in cases_data]
    
    # 1. Números de Betti
    ax1 = axes[0, 0]
    ax1.set_facecolor(COLORS['background'])
    x = np.arange(len(case_names))
    width = 0.35
    
    bars1 = ax1.bar(x - width/2, beta0_values, width, label='β₀ (Componentes)', 
                    color=COLORS['comparison']['beta0'], alpha=0.8,
                    edgecolor='black', linewidth=1)
    bars2 = ax1.bar(x + width/2, beta1_values, width, label='β₁ (Agujeros)', 
                    color=COLORS['comparison']['beta1'], alpha=0.8,
                    edgecolor='black', linewidth=1)
    
    ax1.set_xlabel('Casos', fontsize=10, fontweight='bold')
    ax1.set_ylabel('Número de Betti', fontsize=10, fontweight='bold')
    ax1.set_title('Comparación de Números de Betti', fontsize=12, fontweight='bold')
    ax1.set_xticks(x)
    ax1.set_xticklabels(case_names, rotation=45, ha='right')
    ax1.legend()
    ax1.grid(True, linestyle='--', alpha=0.3)
    
    # Añadir valores en las barras
    for bars in [bars1, bars2]:
        for bar in bars:
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height + 0.05,
                    f'{int(height)}', ha='center', va='bottom', fontweight='bold')
    
    # 2. Característica de Euler
    ax2 = axes[0, 1]
    ax2.set_facecolor(COLORS['background'])
    bars = ax2.bar(case_names, euler_values, color=COLORS['comparison']['euler'], 
                   alpha=0.8, edgecolor='black', linewidth=1)
    ax2.set_xlabel('Casos', fontsize=10, fontweight='bold')
    ax2.set_ylabel('Característica de Euler (χ)', fontsize=10, fontweight='bold')
    ax2.set_title('Característica de Euler por Caso', fontsize=12, fontweight='bold')
    ax2.set_xticklabels(case_names, rotation=45, ha='right')
    ax2.grid(True, linestyle='--', alpha=0.3)
    
    for bar, value in zip(bars, euler_values):
        ax2.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 0.05,
                f'{value}', ha='center', va='bottom', fontweight='bold')
    
    # 3. Consistencia de fórmulas
    ax3 = axes[1, 0]
    ax3.set_facecolor(COLORS['background'])
    colors = [COLORS['comparison']['consistent'] if c else COLORS['comparison']['inconsistent'] 
              for c in consistency]
    bars = ax3.bar(case_names, [1 if c else 0 for c in consistency], 
                   color=colors, alpha=0.8, edgecolor='black', linewidth=1)
    ax3.set_xlabel('Casos', fontsize=10, fontweight='bold')
    ax3.set_ylabel('Consistencia', fontsize=10, fontweight='bold')
    ax3.set_title('Consistencia entre Fórmulas de Euler', fontsize=12, fontweight='bold')
    ax3.set_xticklabels(case_names, rotation=45, ha='right')
    ax3.set_ylim(0, 1.2)
    ax3.set_yticks([0, 1])
    ax3.set_yticklabels(['Inconsistente', 'Consistente'], fontweight='bold')
    ax3.grid(True, linestyle='--', alpha=0.3)
    
    # 4. Mapa de calor de métricas
    ax4 = axes[1, 1]
    ax4.set_facecolor(COLORS['background'])
    
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
    ax4.set_yticklabels(['β₀', 'β₁', 'χ', 'Área'], fontweight='bold')
    ax4.set_title('Mapa de Calor de Métricas', fontsize=12, fontweight='bold')
    
    # Añadir valores en el mapa de calor
    for i in range(4):
        for j in range(len(case_names)):
            text = ax4.text(j, i, f'{metrics_matrix[i, j]:.2f}',
                           ha="center", va="center", color="white", 
                           fontweight='bold')
    
    plt.colorbar(im, ax=ax4, fraction=0.046, pad=0.04)
    
    plt.suptitle('Comparación de Casos Topológicos', 
                fontsize=16, fontweight='bold', y=1.02)
    
    plt.tight_layout()
    plt.savefig(save_path, dpi=VISUALIZATION_CONFIG['dpi'], 
                bbox_inches='tight', facecolor='white')
    plt.close()

def plot_vector_field_enhanced(u, v, mask, save_path, title="Campo Vectorial"):
    """
    Visualización mejorada del campo vectorial
    
    Args:
        u, v: Componentes del campo vectorial (ya enmascarados)
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
    
    # Submuestrear los campos vectoriales ya enmascarados
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
    
    # Subplot 2: Magnitud del campo vectorial (solo donde hay material)
    magnitude = np.sqrt(u**2 + v**2)
    magnitude = magnitude * (mask > 0.5)  # Aplicar máscara a la magnitud
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
        # Calcular número de píxeles
        num_pixeles = np.sum(case['field'])
        
        record = {
            'imagen': case['name'],
            'pixeles': num_pixeles,
            'vertices': case['metrics']['vertices'],
            'aristas': case['metrics']['edges'],
            'caras': case['metrics']['faces'],
            'componentes': case['metrics']['beta0'],
            'agujeros': case['metrics']['beta1'],
            'codigo_f8': case['codes']['f8'],
            'codigo_f4': case['codes']['f4'],
            'codigo_vcc': case['codes']['vcc'],
            'codigo_3ot': case['codes']['ot3'],
            'N1': case['metrics']['vcc']['N1'],
            'N3': case['metrics']['vcc']['N3'],
            'N2h': case['metrics']['3ot']['N2h'],
            'N2v': case['metrics']['3ot']['N2v'],
            'euler_vef': case['metrics']['euler_vef'],
            'euler_poincare': case['metrics']['euler_poincare'],
            'vcc_x': case['metrics']['vcc']['x'],
            '3ot_x': case['metrics']['3ot']['combined']['X_value'],
            'euler_freeman': case['metrics']['freeman_chain']['euler_from_chain_rotation']
        }
        records.append(record)
    
    # Crear DataFrame y guardar
    df = pd.DataFrame(records)
    
    # Asegurar que el directorio existe
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    
    # Evitar exportación como notación científica: forzamos a string
    df['codigo_f8'] = df['codigo_f8'].astype(str)
    df['codigo_f4'] = df['codigo_f4'].astype(str)
    df['codigo_vcc'] = df['codigo_vcc'].astype(str)
    df['codigo_3ot'] = df['codigo_3ot'].astype(str)

    # Alternativa rápida: proteger como texto para Excel
    for col in ['codigo_f8', 'codigo_f4', 'codigo_vcc', 'codigo_3ot']:
        df[col] = df[col].apply(lambda x: f'="{x}"')
        
    # Guardar CSV
    df.to_csv(save_path, index=False, encoding='utf-8')
    print(f"\nMétricas guardadas en: {save_path}")

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

def plot_topology_codes(codes, save_path, case_name=""):
    """
    Visualiza los códigos VCC y 3OT
    
    Args:
        codes: Diccionario con los códigos
        save_path: Ruta donde guardar la visualización
        case_name: Nombre del caso (opcional)
    """
    # Configuración de colores y estilos
    background_color = '#f0f0f0'
    bar_colors = {
        # Colores para VCC (base 4)
        '0': '#1f77b4',  # Azul
        '1': '#2ca02c',  # Verde
        '2': '#ff7f0e',  # Naranja
        '3': '#d62728',  # Rojo
        # Colores para 3OT (base 3)
        'h': '#1f77b4',  # Azul para horizontal
        'v': '#2ca02c',  # Verde para vertical
        'd': '#ff7f0e'   # Naranja para diagonal
    }
    
    # Crear figura con dos subplots
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(15, 10))
    fig.patch.set_facecolor('white')
    
    # Configurar el primer subplot para VCC
    ax1.set_facecolor(background_color)
    
    vcc_code = list(codes['vcc'])
    x = np.arange(len(vcc_code))
    colors = [bar_colors[d] for d in vcc_code]
    
    bars = ax1.bar(x, [1]*len(vcc_code), color=colors, edgecolor='black', linewidth=1)
    ax1.set_title('Código VCC (Vertex Correction Code)', pad=20, fontsize=12, fontweight='bold')
    ax1.set_xticks(x)
    ax1.set_xticklabels(vcc_code, fontsize=10)
    ax1.set_ylim(0, 1.5)
    ax1.grid(True, linestyle='--', alpha=0.3)
    
    # Añadir valores sobre las barras
    for i, bar in enumerate(bars):
        ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1,
                vcc_code[i], ha='center', va='bottom', fontweight='bold')
    
    # Crear leyenda para VCC
    legend_elements = [plt.Rectangle((0,0),1,1, facecolor=bar_colors[str(i)], 
                                   edgecolor='black', label=f'Valor {i}')
                      for i in range(4)]  # 4 valores para VCC
    ax1.legend(handles=legend_elements, title='Valores VCC',
              loc='upper right', bbox_to_anchor=(1, -0.1))
    
    # Configurar el segundo subplot para 3OT
    ax2.set_facecolor(background_color)
    
    ot3_code = list(codes['ot3'])
    x = np.arange(len(ot3_code))
    colors = [bar_colors[d] for d in ot3_code]
    
    bars = ax2.bar(x, [1]*len(ot3_code), color=colors, edgecolor='black', linewidth=1)
    ax2.set_title('Código 3OT (Three Orthogonal Topology)', pad=20, fontsize=12, fontweight='bold')
    ax2.set_xticks(x)
    ax2.set_xticklabels(ot3_code, fontsize=10)
    ax2.set_ylim(0, 1.5)
    ax2.grid(True, linestyle='--', alpha=0.3)
    
    # Añadir valores sobre las barras
    for i, bar in enumerate(bars):
        ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1,
                ot3_code[i], ha='center', va='bottom', fontweight='bold')
    
    # Crear leyenda para 3OT
    legend_elements = [plt.Rectangle((0,0),1,1, facecolor=bar_colors[str(i)], 
                                   edgecolor='black', label=f'Valor {i}')
                      for i in range(3)]  # 3 valores para 3OT
    ax2.legend(handles=legend_elements, title='Valores 3OT',
              loc='upper right', bbox_to_anchor=(1, -0.1))
    
    # Añadir título general
    if case_name:
        plt.suptitle(f'Códigos Topológicos - {case_name}', 
                    fontsize=16, fontweight='bold', y=1.02)
    
    # Añadir información adicional
    info_text = f"""
    Longitud de códigos: {len(vcc_code)}
    VCC: {codes['vcc']}
    3OT: {codes['ot3']}
    """
    fig.text(0.02, 0.02, info_text, fontsize=10, 
             bbox=dict(facecolor='white', edgecolor='black', alpha=0.8))
    
    # Guardar la figura
    plt.savefig(save_path, dpi=VISUALIZATION_CONFIG['dpi'], 
                bbox_inches='tight', facecolor='white')
    plt.close()

def create_topology_pattern(code, size=(256, 256)):
    """
    Crea una imagen binaria basada en un código topológico.
    
    Args:
        code: String con el código (VCC o 3OT)
        size: Tupla con el tamaño de la imagen (height, width)
        
    Returns:
        numpy.ndarray: Imagen binaria generada
    """
    pattern = np.zeros(size, dtype=np.uint8)
    h, w = size
    cell_width = w // len(code)
    
    for i, digit in enumerate(code):
        value = int(digit)
        if value == 0:
            # Crear un punto
            x = i * cell_width + cell_width // 2
            y = h // 2
            cv2.circle(pattern, (x, y), 5, 1, -1)
        elif value == 1:
            # Crear una línea vertical
            x = i * cell_width + cell_width // 2
            cv2.line(pattern, (x, h//4), (x, 3*h//4), 1, 2)
        else:  # value == 2
            # Crear una cruz
            x = i * cell_width + cell_width // 2
            y = h // 2
            size = min(cell_width, h) // 3
            cv2.line(pattern, (x-size, y), (x+size, y), 1, 2)
            cv2.line(pattern, (x, y-size), (x, y+size), 1, 2)
    
    return pattern

def plot_topology_patterns(codes, save_path, case_name=""):
    """
    Crea una visualización de los patrones topológicos generados a partir de los códigos
    
    Args:
        codes: Diccionario con los códigos ('vcc' y 'ot3')
        save_path: Ruta donde guardar la imagen
        case_name: Nombre del caso para el título
    """
    # Configurar el estilo de la visualización
    plt.style.use('default')
    
    fig = plt.figure(figsize=(15, 8))
    fig.patch.set_facecolor('white')
    gs = GridSpec(1, 2, figure=fig, wspace=0.3)
    
    # 1. Patrón VCC
    ax1 = fig.add_subplot(gs[0, 0])
    ax1.set_facecolor(COLORS['background'])
    vcc_pattern = create_topology_pattern(codes['vcc'])
    im1 = ax1.imshow(vcc_pattern, cmap='viridis', origin='lower')
    ax1.set_title('Patrón VCC', fontsize=12, fontweight='bold')
    plt.colorbar(im1, ax=ax1, fraction=0.046, pad=0.04)
    
    # Añadir código como texto
    ax1.text(0.02, -0.1, f'Código: {codes["vcc"]}', 
             transform=ax1.transAxes, fontsize=10,
             bbox=dict(facecolor='white', edgecolor='black', alpha=0.8))
    
    # 2. Patrón 3OT
    ax2 = fig.add_subplot(gs[0, 1])
    ax2.set_facecolor(COLORS['background'])
    ot3_pattern = create_topology_pattern(codes['ot3'])
    im2 = ax2.imshow(ot3_pattern, cmap='viridis', origin='lower')
    ax2.set_title('Patrón 3OT', fontsize=12, fontweight='bold')
    plt.colorbar(im2, ax=ax2, fraction=0.046, pad=0.04)
    
    # Añadir código como texto
    ax2.text(0.02, -0.1, f'Código: {codes["ot3"]}', 
             transform=ax2.transAxes, fontsize=10,
             bbox=dict(facecolor='white', edgecolor='black', alpha=0.8))
    
    # Título general
    if case_name:
        plt.suptitle(f'Patrones Topológicos - {case_name}', 
                    fontsize=16, fontweight='bold', y=1.05)
    
    # Añadir información adicional
    info_text = f"""
    Longitud de códigos: {len(codes['vcc'])}
    VCC: {codes['vcc']}
    3OT: {codes['ot3']}
    """
    fig.text(0.02, 0.02, info_text, fontsize=10, 
             bbox=dict(facecolor='white', edgecolor='black', alpha=0.8))
    
    # Guardar la figura
    plt.savefig(save_path, dpi=VISUALIZATION_CONFIG['dpi'], 
                bbox_inches='tight', facecolor='white')
    plt.close()