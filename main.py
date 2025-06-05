import os
import sys
import numpy as np
from datetime import datetime

# Añadir el directorio actual al path para importar módulos
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from generator.field_generator import generate_topology_case, generate_vector_field
from generator.topology_metrics import compute_all_metrics, analyze_connectivity
from generator.visualizer import (plot_topology_analysis, create_comparison_plot, 
                                 create_individual_case_visualization, 
                                 save_metrics_to_csv, create_summary_report)
from generator.case_definitions import get_topology_cases, validate_case_topology
from config.topology_config import IMAGE_CONFIG

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
    
    # Mostrar códigos generados
    print("\nCódigos Topológicos:")
    print(f"  VCC: {metrics['vcc']['code_string']}")
    print(f"  3OT: {metrics['3ot']['code_string']}")
    
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
    vcc = metrics['vcc']
    if vcc['is_consistent']:
        print("✓ El código VCC coincide con Euler-Poincaré:")
        print(f"  VCC(x) = {vcc['x']:.2f} ≈ χ = {metrics['euler_poincare']}")
    else:
        print("✗ Discrepancia entre VCC y Euler-Poincaré:")
        print(f"  VCC(x) = {vcc['x']:.2f} ≠ χ = {metrics['euler_poincare']}")
    
    # 3. Análisis 3OT
    ot3 = metrics['3ot']
    print("\nAnálisis direccional (3OT):")
    print(f"  Horizontal (N2h): {ot3['N2h']} segmentos")
    print(f"  Vertical (N2v): {ot3['N2v']} segmentos")
    print(f"  Diagonal (N2d): {ot3['N2d']} segmentos")
    print(f"  X = (N2h - N2v)/4 = {ot3['combined']['X_value']:.2f}")
    
    # 4. Validación con caso esperado
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
    os.makedirs(f"{output_dir}/images", exist_ok=True)
    os.makedirs(f"{output_dir}/individual", exist_ok=True)
    os.makedirs(f"{output_dir}/metrics", exist_ok=True)
    os.makedirs(f"{output_dir}/comparison", exist_ok=True)
    
    print(f"Guardando resultados en: {output_dir}")
    
    # Guardar visualizaciones individuales
    for result in results:
        case_name = result['name']
        field = result['field']
        u, v = result['vector_field']
        metrics = result['metrics']
        
        # Análisis completo individual
        save_path = f"{output_dir}/individual/complete_{case_name}.png"
        plot_topology_analysis(field, u, v, metrics, save_path, case_name)
        
        # Visualizaciones detalladas
        case_dir = f"{output_dir}/individual/{case_name}"
        create_individual_case_visualization(field, u, v, metrics, case_name, case_dir)
    
    # Guardar comparación general
    comparison_path = f"{output_dir}/comparison/topology_comparison.png"
    create_comparison_plot(results, comparison_path)
    
    # Guardar métricas en CSV
    csv_path = f"{output_dir}/metrics/topology_metrics.csv"
    save_metrics_to_csv(results, csv_path)
    
    # Crear reporte resumen
    report_path = f"{output_dir}/metrics/topology_report.txt"
    create_summary_report(results, report_path)
    
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
    print("ANÁLISIS TOPOLÓGICO 2D - FÓRMULAS DE EULER")
    print("="*60)
    print(f"Fecha de ejecución: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Configuración
    output_dir = "output"
    image_size = IMAGE_CONFIG['default_size']
    seed = 42  # Para reproducibilidad
    
    # Obtener casos de topología definidos
    topology_cases = get_topology_cases()
    case_names = list(topology_cases.keys())
    
    print(f"Casos a procesar: {len(case_names)}")
    print(f"Tamaño de imagen: {image_size}")
    print(f"Semilla: {seed}")
    print()
    
    # Procesar todos los casos
    results = []
    
    for case_name in case_names:
        try:
            result = process_topology_case(case_name, image_size, seed)
            results.append(result)
        except Exception as e:
            print(f"Error procesando {case_name}: {str(e)}")
            continue
    
    # Validar resultados
    validation_summary = validate_all_cases(results)
    print_validation_summary(validation_summary)
    
    # Guardar todos los resultados
    if results:
        save_results(results, output_dir)
        
        # Mostrar casos problemáticos si los hay
        problematic_cases = [r for r in results if not r['metrics']['is_consistent']]
        if problematic_cases:
            print(f"\nCasos con inconsistencia en fórmulas de Euler:")
            for case in problematic_cases:
                metrics = case['metrics']
                print(f"  {case['name']}: V-E+F={metrics['euler_vef']}, β₀-β₁={metrics['euler_poincare']}")
        
        invalid_cases = [r for r in results if not r['validation']]
        if invalid_cases:
            print(f"\nCasos que no coinciden con la topología esperada:")
            for case in invalid_cases:
                print(f"  {case['name']}")
    
    print(f"\nAnálisis completado. Revisa los archivos en: {output_dir}/")

if __name__ == "__main__":
    # Configurar numpy para reproducibilidad
    np.random.seed(42)
    
    # Ejecutar análisis principal
    main()