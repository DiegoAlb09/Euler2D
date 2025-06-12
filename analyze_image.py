import sys
import matplotlib.pyplot as plt
from generator.topology_analyzer import analizar_imagen_topologica
from generator.topology_base import compute_betti_numbers_2d, calcular_V_E_F
from generator.image_reader import read_binary_image

def main():
    """
    Script principal para analizar una imagen binaria.
    Uso: python analyze_image.py ruta/a/imagen.png
    """
    if len(sys.argv) < 2:
        print("Por favor proporciona la ruta a una imagen binaria.")
        print("Uso: python analyze_image.py ruta/a/imagen.png")
        sys.exit(1)
    
    # Leer la imagen
    imagen_path = sys.argv[1]
    try:
        imagen = read_binary_image(imagen_path)
        print(f"\nAnalizando imagen: {imagen_path}")
        print("=" * 50)
        
        # Analizar la imagen
        metricas = analizar_imagen_topologica(imagen)
        
        # Mostrar resultados
        print("\nNúmeros de Betti:")
        print(f"  N (β₀) = {metricas['N']} componentes")
        print(f"  H (β₁) = {metricas['H']} agujeros")
        
        print("\nComplejo simplicial:")
        print(f"  V = {metricas['V']} vértices")
        print(f"  E = {metricas['E']} aristas")
        print(f"  F = {metricas['F']} caras")
        
        print("\nCaracterística de Euler:")
        print(f"  χ (V-E+F) = {metricas['chi_vef']}")
        print(f"  χ (N-H) = {metricas['chi_NH']}")
        print(f"  Consistencia: {'✓' if metricas['consistente'] else '✗'}")
        
        # Visualizar la imagen
        plt.figure(figsize=(8, 8))
        plt.imshow(imagen, cmap='gray')
        plt.title(f"Imagen analizada\nχ = {metricas['chi_NH']}")
        plt.axis('off')
        plt.show()
        
    except Exception as e:
        print(f"Error al procesar la imagen: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main() 