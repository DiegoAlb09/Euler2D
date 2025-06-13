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
from generator.topology_codes_extended import (compute_euler_from_freeman_chain, get_f8_code, f8_to_f4, compute_vcc, compute_3ot,
                                            normalize_code_length, verify_euler_equalities)
from generator.case_definitions import get_topology_cases, validate_case_topology
from generator.image_reader import read_binary_image, validate_binary_image, preprocess_binary_image
from generator.test_images import get_test_images, visualizar_imagenes_prueba
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

    euler_freeman_rot = compute_euler_from_freeman_chain(f8_code)
    metrics['freeman_chain'] = {'euler_from_chain_rotation': euler_freeman_rot}
    
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
    print(f"  Sumatoria de rotaciones locales: {euler_freeman_rot}")

    
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
    
    if not equalities['todas_igualdades_cumplen']:
        print("\nDiferencias encontradas:")
        for name, value in equalities['diferencias'].items():
            print(f"  {name}: {value:.6f}")
    
    return result

def analyze_test_images():
    """
    Analiza todas las imágenes de prueba y guarda los resultados.
    """
    # Crear directorios de salida
    output_dir = "output"
    test_images_dir = "test_images"
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(test_images_dir, exist_ok=True)
    
    # Obtener imágenes de prueba
    imagenes = get_test_images()
    
    print("\nANÁLISIS TOPOLÓGICO DE IMÁGENES DE PRUEBA")
    print("=" * 80)
    print(f"Fecha de ejecución: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Total de imágenes a analizar: {len(imagenes)}")
    print()
    
    # Lista para almacenar resultados
    resultados = []
    
    # Analizar cada imagen
    for nombre, imagen in imagenes.items():
        print(f"\nAnalizando: {nombre}")
        print("-" * 80)
        
        # Guardar imagen en test_images
        imagen_path = os.path.join(test_images_dir, f"{nombre}.png")
        plt.imsave(imagen_path, imagen, cmap='gray')
        
        # Generar campo vectorial
        u, v = generate_vector_field(imagen)
        
        # Calcular métricas
        metrics = compute_all_metrics(imagen)
        connectivity = analyze_connectivity(imagen)
        
        # Generar códigos
        f8_code = get_f8_code(imagen)
        euler_freeman_rot = compute_euler_from_freeman_chain(f8_code)  # ← Primero lo calculás
        f4_code = f8_to_f4(f8_code)
        vcc_results = compute_vcc(imagen, f4_code)
        ot3_results = compute_3ot(imagen, vcc_results['code_string'])

        metrics['freeman_chain'] = {'euler_from_chain_rotation': euler_freeman_rot}  # ← NUEVO
        
        # Verificar igualdades
        equalities = verify_euler_equalities(metrics)
        
        # Guardar resultado
        resultado = {
            'name': nombre,
            'field': imagen,
            'vector_field': (u, v),
            'metrics': metrics,
            'connectivity': connectivity,
            'codes': {
                'f8': f8_code,
                'f4': f4_code,
                'vcc': vcc_results['code_string'],
                'ot3': ot3_results['code_string']
            },
            'equalities': equalities
        }
        resultados.append(resultado)
        
        # Mostrar análisis detallado
        print(f"Píxeles: {np.sum(imagen)}")
        print(f"Vértices (V): {metrics['vertices']}")
        print(f"Aristas (E): {metrics['edges']}")
        print(f"Caras (F): {metrics['faces']}")
        print(f"Componentes (N): {metrics['beta0']}")
        print(f"Agujeros (H): {metrics['beta1']}")
        print("\nCódigos Topológicos:")
        print(f"  F8: {f8_code}")
        print(f"  F4: {f4_code}")
        print(f"  VCC: {vcc_results['code_string']}")
        print(f"  3OT: {ot3_results['code_string']}")
        print("\nAnálisis VCC:")
        print(f"  N1: {metrics['vcc']['N1']}")
        print(f"  N3: {metrics['vcc']['N3']}")
        print(f"  x = (N1 - N3)/4: {metrics['vcc']['x']:.2f}")
        print("\nAnálisis 3OT:")
        print(f"  N2h: {metrics['3ot']['N2h']}")
        print(f"  N2v: {metrics['3ot']['N2v']}")
        print(f"  N2d: {metrics['3ot']['N2d']}")
        print(f"  X = (N2h - N2v)/4: {metrics['3ot']['combined']['X_value']:.2f}")
        print("\nCaracterísticas de Euler:")
        print(f"  χ = V - E + F = {metrics['euler_vef']:.2f}")
        print(f"  χ = N - H = {metrics['euler_poincare']:.2f}")
        print(f"  χ = (N1 - N3)/4 = {metrics['vcc']['x']:.2f}")
        print(f"  χ = (N2h - N2v)/4 = {metrics['3ot']['combined']['X_value']:.2f}")
        print(f"  χ = ΣR(i)/4 (Freeman Chain) = {euler_freeman_rot:.2f}")
        print("\nVerificación de igualdades:")
        for name, value in equalities['verificaciones'].items():
            print(f"  {name}: {'✓' if value else '✗'}")
    
    # Guardar métricas en CSV
    save_metrics_to_csv(resultados, os.path.join(output_dir, "metricas.csv"))
    
    print("\nAnálisis completado exitosamente!")
    print(f"Los resultados se encuentran en el directorio: {os.path.abspath(output_dir)}")
    print(f"Las imágenes se encuentran en el directorio: {os.path.abspath(test_images_dir)}")

def main():
    """Función principal del programa"""
    print("ANÁLISIS TOPOLÓGICO 2D - CÓDIGOS Y FÓRMULAS DE EULER")
    print("=" * 60)
    print(f"Fecha de ejecución: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Directorio de trabajo: {os.getcwd()}")
    print()
    
    # Analizar imágenes de prueba
    analyze_test_images()

if __name__ == "__main__":
    # Configurar numpy para reproducibilidad
    np.random.seed(42)
    
    # Ejecutar análisis principal
    main()