import os
import sys
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt

# Añadir el directorio actual al path para importar módulos
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from generator.field_generator import generate_topology_case, generate_vector_field
from generator.topology_metrics import compute_all_metrics, analyze_connectivity
from generator.visualizer import (plot_topology_analysis, create_comparison_plot, 
                                 create_individual_case_visualization, 
                                 save_metrics_to_csv, create_summary_report,
                                 plot_vector_field_enhanced, plot_topology_codes, plot_topology_patterns)
from generator.case_definitions import get_topology_cases, validate_case_topology
from generator.image_reader import read_binary_image, validate_binary_image, preprocess_binary_image
from generator.topology_codes_extended import get_f8_code, f8_to_f4, normalize_code_length, verify_euler_equalities
from generator.topology_codes import compute_vcc, compute_3ot
from config.topology_config import IMAGE_CONFIG, VISUALIZATION_CONFIG

def analyze_binary_image(image_path):
    """
    Analiza una imagen binaria y calcula todos los códigos y métricas topológicas.
    
    Args:
        image_path: Ruta a la imagen binaria
        
    Returns:
        dict: Resultados del análisis
    """
    # Normalizar la ruta del archivo
    image_path = os.path.abspath(os.path.normpath(image_path))
    
    print(f"\nAnalizando imagen: {image_path}")
    print("=" * 50)
    
    # Verificar que el archivo existe
    if not os.path.exists(image_path):
        raise ValueError(f"La imagen no existe en la ruta: {image_path}")
    
    print(f"Ruta absoluta normalizada: {image_path}")
    print(f"Directorio actual: {os.getcwd()}")
    
    # Leer y preprocesar imagen
    try:
        binary_image = read_binary_image(image_path)
        print("Imagen leída correctamente")
        print(f"Dimensiones de la imagen: {binary_image.shape}")
    except Exception as e:
        print(f"Error al leer la imagen: {str(e)}")
        raise
    
    if not validate_binary_image(binary_image):
        raise ValueError("La imagen no es válida para análisis topológico")
    
    print("Imagen validada correctamente")
    binary_image = preprocess_binary_image(binary_image)
    print("Imagen preprocesada correctamente")
    
    # Generar campo vectorial
    u, v = generate_vector_field(binary_image)
    
    # Calcular métricas topológicas básicas
    metrics = compute_all_metrics(binary_image)
    connectivity = analyze_connectivity(binary_image)
    
    # Generar códigos en secuencia F8 -> F4 -> VCC -> 3OT
    f8_code = get_f8_code(binary_image)
    f4_code = f8_to_f4(f8_code)
    
    # Calcular VCC a partir de F4
    vcc_results = compute_vcc(binary_image, f4_code)
    metrics['vcc'] = vcc_results
    vcc_code = vcc_results['code_string']
    
    # Calcular 3OT a partir de VCC
    ot3_results = compute_3ot(binary_image, vcc_code)
    metrics['3ot'] = ot3_results
    ot3_code = ot3_results['code_string']
    
    # Verificar igualdades
    equalities = verify_euler_equalities(metrics)
    
    # Preparar resultado
    result = {
        'binary_image': binary_image,
        'vector_field': (u, v),
        'metrics': metrics,
        'connectivity': connectivity,
        'codes': {
            'f8': f8_code,
            'f4': f4_code,
            'vcc': vcc_code,
            'ot3': ot3_code
        },
        'equalities': equalities
    }
    
    # Mostrar resultados
    print("\nCódigos Topológicos:")
    print(f"  F8: {f8_code}")
    print(f"  F4: {f4_code}")
    print(f"  VCC: {vcc_code}")
    print(f"  3OT: {ot3_code}")
    
    print("\nMétricas Principales:")
    print(f"  β₀ (Componentes) = {metrics['beta0']}")
    print(f"  β₁ (Agujeros) = {metrics['beta1']}")
    print(f"  χ (V-E+F) = {metrics['euler_vef']}")
    print(f"  χ (β₀-β₁) = {metrics['euler_poincare']}")
    print(f"  VCC (N1-N3)/4 = {metrics['vcc']['x']:.2f}")
    print(f"  3OT (N2h-N2v)/4 = {metrics['3ot']['combined']['X_value']:.2f}")
    
    print("\nVerificación de Igualdades:")
    for name, value in equalities['verificaciones'].items():
        print(f"  {name}: {'✓' if value else '✗'}")
    print(f"  Todas las igualdades se cumplen: {'✓' if equalities['todas_igualdades_cumplen'] else '✗'}")
    
    if not equalities['todas_igualdades_cumplen']:
        print("\nDiferencias encontradas:")
        for name, value in equalities['diferencias'].items():
            print(f"  {name}: {value:.6f}")
    
    return result

def process_topology_case(case_name, size=None, seed=42):
    """
    Procesa un caso individual de topología
    
    Args:
        case_name: Nombre del caso a procesar
        size: Tamaño de la imagen (por defecto desde config)
        seed: Semilla para reproducibilidad
        
    Returns:
        dict: Diccionario con todos los datos del caso
    """
    if size is None:
        size = IMAGE_CONFIG['default_size']
    
    print(f"\nProcesando caso: {case_name}")
    print("=" * 50)
    
    # Generar campo con topología específica
    field = generate_topology_case(case_name, size, seed)
    
    # Generar campo vectorial
    u, v = generate_vector_field(field)
    
    # Calcular métricas topológicas
    metrics = compute_all_metrics(field)
    connectivity = analyze_connectivity(field)
    
    # Validar topología esperada
    validation = validate_case_topology(case_name, metrics)
    
    # Preparar resultado
    result = {
        'name': case_name,
        'field': field,
        'vector_field': (u, v),
        'metrics': metrics,
        'connectivity': connectivity,
        'validation': validation,
        'size': size,
        'seed': seed
    }
    
    # Mostrar métricas principales y conclusiones
    print("\nMétricas Principales:")
    print(f"  β₀ (Componentes) = {metrics['beta0']}")
    print(f"  β₁ (Agujeros) = {metrics['beta1']}")
    print(f"  χ (V-E+F) = {metrics['euler_vef']}")
    print(f"  χ (β₀-β₁) = {metrics['euler_poincare']}")
    
    # Mostrar códigos generados y verificaciones
    print("\nCódigos Topológicos:")
    print(f"  VCC: {metrics['vcc']['code_string']}")
    print(f"  3OT: {metrics['3ot']['code_string']}")
    
    # Verificación de relaciones
    vcc = metrics['vcc']
    ot3 = metrics['3ot']
    
    print("\nVerificación de Relaciones:")
    print("  VCC:")
    print(f"    x = (N1 - N3)/4 = {vcc['x']:.2f}")
    print(f"    χ (β₀-β₁) = {metrics['euler_poincare']}")
    print(f"    ¿Coinciden? {'✓' if vcc['is_consistent'] else '✗'}")
    print(f"    Diferencia: {abs(vcc['x'] - metrics['euler_poincare']):.6f}")
    
    print("\n  3OT:")
    print(f"    X = (N2h - N2v)/4 = {ot3['combined']['X_value']:.2f}")
    print(f"    χ (β₀-β₁) = {metrics['euler_poincare']}")
    print(f"    ¿Coinciden? {'✓' if ot3['combined']['is_consistent'] else '✗'}")
    print(f"    Diferencia: {ot3['combined']['difference']:.6f}")
    
    # Mostrar conclusiones
    print("\nConclusiones del Análisis:")
    
    # 1. Validación de fórmulas de Euler
    if metrics['is_consistent']:
        print("✓ Las fórmulas de Euler son consistentes:")
        print(f"  V-E+F = β₀-β₁ = {metrics['euler_poincare']}")
    else:
        print("✗ Inconsistencia en las fórmulas de Euler:")
        print(f"  V-E+F = {metrics['euler_vef']} ≠ β₀-β₁ = {metrics['euler_poincare']}")
    
    # 2. Validación de VCC
    if vcc['is_consistent']:
        print("✓ El código VCC coincide con Euler-Poincaré:")
        print(f"  VCC(x) = {vcc['x']:.2f} ≈ χ = {metrics['euler_poincare']}")
    else:
        print("✗ Discrepancia entre VCC y Euler-Poincaré:")
        print(f"  VCC(x) = {vcc['x']:.2f} ≠ χ = {metrics['euler_poincare']}")
    
    # 3. Validación de 3OT
    if ot3['combined']['is_consistent']:
        print("✓ El código 3OT coincide con Euler-Poincaré:")
        print(f"  3OT(X) = {ot3['combined']['X_value']:.2f} ≈ χ = {metrics['euler_poincare']}")
    else:
        print("✗ Discrepancia entre 3OT y Euler-Poincaré:")
        print(f"  3OT(X) = {ot3['combined']['X_value']:.2f} ≠ χ = {metrics['euler_poincare']}")
    
    # 4. Análisis direccional (3OT)
    print("\nAnálisis direccional (3OT):")
    print(f"  Horizontal (N2h): {ot3['N2h']} segmentos")
    print(f"  Vertical (N2v): {ot3['N2v']} segmentos")
    print(f"  Diagonal (N2d): {ot3['N2d']} segmentos")
    print(f"  X = (N2h - N2v)/4 = {ot3['combined']['X_value']:.2f}")
    
    # 5. Validación con caso esperado
    if validation:
        print("\n✓ La topología coincide con lo esperado")
    else:
        print("\n✗ La topología no coincide con lo esperado")
    
    print("\n" + "-" * 50)
    
    return result

def save_results(results, output_dir):
    """
    Guarda todos los resultados en archivos organizados
    
    Args:
        results: Lista de resultados de casos
        output_dir: Directorio base de salida
    """
    # Crear directorios
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(f"{output_dir}/cases", exist_ok=True)
    
    print(f"Guardando resultados en: {output_dir}")
    
    # Guardar visualizaciones individuales
    for result in results:
        case_name = result['name']
        field = result['field']
        
        # Guardar solo la imagen de la topología
        plt.figure(figsize=(8, 8))
        plt.imshow(field, cmap='gray', origin='lower')
        plt.axis('off')  # Quitar ejes
        plt.savefig(f'{output_dir}/cases/{case_name}.png', 
                    dpi=VISUALIZATION_CONFIG['dpi'], 
                    bbox_inches='tight',
                    pad_inches=0)  # Quitar padding
        plt.close()
    
    print("Resultados guardados exitosamente!")

def validate_all_cases(results):
    """
    Valida la consistencia de todos los casos procesados
    
    Args:
        results: Lista de resultados
        
    Returns:
        dict: Resumen de validación
    """
    total_cases = len(results)
    consistent_euler = sum(1 for r in results if r['metrics']['is_consistent'])
    valid_topology = sum(1 for r in results if r['validation'])
    
    validation_summary = {
        'total_cases': total_cases,
        'consistent_euler_formulas': consistent_euler,
        'valid_expected_topology': valid_topology,
        'euler_consistency_rate': consistent_euler / total_cases if total_cases > 0 else 0,
        'topology_validation_rate': valid_topology / total_cases if total_cases > 0 else 0
    }
    
    return validation_summary

def print_validation_summary(validation_summary):
    """Imprime un resumen de la validación"""
    print("\n" + "="*60)
    print("RESUMEN DE VALIDACIÓN")
    print("="*60)
    print(f"Total de casos procesados: {validation_summary['total_cases']}")
    print(f"Casos con fórmulas de Euler consistentes: {validation_summary['consistent_euler_formulas']}")
    print(f"Casos con topología esperada válida: {validation_summary['valid_expected_topology']}")
    print(f"Tasa de consistencia de Euler: {validation_summary['euler_consistency_rate']:.2%}")
    print(f"Tasa de validación topológica: {validation_summary['topology_validation_rate']:.2%}")
    print("="*60)

def main():
    """Función principal del programa"""
    print("ANÁLISIS TOPOLÓGICO 2D - CÓDIGOS Y FÓRMULAS DE EULER")
    print("="*60)
    print(f"Fecha de ejecución: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Directorio de trabajo: {os.getcwd()}")
    print()
    
    # Configuración
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    
    # Procesar imagen de ejemplo o casos predefinidos
    if len(sys.argv) > 1:
        # Analizar imagen proporcionada
        image_path = sys.argv[1]
        try:
            # Convertir a ruta absoluta y normalizada
            image_path = os.path.abspath(os.path.normpath(image_path))
            print(f"Procesando imagen: {image_path}")
            
            result = analyze_binary_image(image_path)
            
            # Obtener nombre base para los archivos de salida
            base_name = os.path.splitext(os.path.basename(image_path))[0]
            
            # Guardar análisis general
            output_path = os.path.join(output_dir, f"{base_name}_analysis.png")
            print(f"Guardando análisis general en: {output_path}")
            plot_topology_analysis(
                result['binary_image'],
                result['vector_field'][0],
                result['vector_field'][1],
                result['metrics'],
                output_path,
                base_name
            )
            
            # Guardar visualización de códigos
            codes_path = os.path.join(output_dir, f"{base_name}_codes.png")
            print(f"Guardando visualización de códigos en: {codes_path}")
            plot_topology_codes(
                result['codes'],
                codes_path,
                base_name
            )
            
            # Guardar patrones generados
            patterns_path = os.path.join(output_dir, f"{base_name}_patterns.png")
            print(f"Guardando patrones topológicos en: {patterns_path}")
            plot_topology_patterns(
                result['codes'],
                patterns_path,
                base_name
            )
            
            print("Análisis completado exitosamente")
            
        except Exception as e:
            print(f"Error procesando imagen: {str(e)}")
            import traceback
            print("Detalles del error:")
            traceback.print_exc()
    else:
        print("Por favor proporciona una ruta a una imagen binaria como argumento.")
        print("Ejemplo: python main.py ruta/a/tu/imagen.png")
        sys.exit(1)

if __name__ == "__main__":
    # Configurar numpy para reproducibilidad
    np.random.seed(42)
    
    # Ejecutar análisis principal
    main()