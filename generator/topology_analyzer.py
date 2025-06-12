import numpy as np
from .topology_base import compute_betti_numbers_2d, calcular_V_E_F
from .test_images import get_test_images, visualizar_imagenes_prueba

def analizar_imagen_topologica(imagen):
    """
    Analiza una imagen binaria y calcula sus características topológicas.
    
    Args:
        imagen: Imagen binaria a analizar
        
    Returns:
        dict: Diccionario con las métricas topológicas
    """
    # Calcular números de Betti
    N, H = compute_betti_numbers_2d(imagen)
    
    # Calcular V, E, F
    V, E, F = calcular_V_E_F(imagen)
    
    # Calcular característica de Euler de dos formas
    chi_vef = V - E + F
    chi_NH = N - H
    
    return {
        'N': N,
        'H': H,
        'V': V,
        'E': E,
        'F': F,
        'chi_vef': chi_vef,
        'chi_NH': chi_NH,
        'consistente': abs(chi_vef - chi_NH) < 1e-10
    }

def analizar_imagenes_prueba():
    """
    Analiza el conjunto de imágenes de prueba y muestra sus características topológicas.
    """
    imagenes = get_test_images()
    resultados = {}
    
    print("\nANÁLISIS TOPOLÓGICO DE IMÁGENES DE PRUEBA")
    print("=" * 50)
    
    for nombre, imagen in imagenes.items():
        print(f"\nAnalizando: {nombre}")
        print("-" * 30)
        
        metricas = analizar_imagen_topologica(imagen)
        resultados[nombre] = metricas
        
        print(f"Números de Betti:")
        print(f"  N (β₀) = {metricas['N']} componentes")
        print(f"  H (β₁) = {metricas['H']} agujeros")
        
        print(f"\nComplejo simplicial:")
        print(f"  V = {metricas['V']} vértices")
        print(f"  E = {metricas['E']} aristas")
        print(f"  F = {metricas['F']} caras")
        
        print(f"\nCaracterística de Euler:")
        print(f"  χ (V-E+F) = {metricas['chi_vef']}")
        print(f"  χ (N-H) = {metricas['chi_NH']}")
        print(f"  Consistencia: {'✓' if metricas['consistente'] else '✗'}")
    
    # Visualizar las imágenes
    fig = visualizar_imagenes_prueba(imagenes)
    
    return resultados, fig

if __name__ == "__main__":
    resultados, fig = analizar_imagenes_prueba()
    import matplotlib.pyplot as plt
    plt.show() 