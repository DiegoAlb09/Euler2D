import os
import matplotlib.pyplot as plt
from generator.test_images import get_test_images

def main():
    """
    Genera y guarda las imágenes de prueba en el directorio 'test_images'
    """
    # Crear directorio si no existe
    output_dir = "test_images"
    os.makedirs(output_dir, exist_ok=True)
    
    # Obtener imágenes de prueba
    imagenes = get_test_images()
    
    print("\nGenerando imágenes de prueba...")
    print("=" * 50)
    
    # Guardar cada imagen
    for nombre, imagen in imagenes.items():
        # Limpiar nombre para archivo
        nombre_archivo = nombre.replace(" ", "_").replace("(", "").replace(")", "").replace("'", "").replace("=", "_")
        ruta_salida = os.path.join(output_dir, f"{nombre_archivo}.png")
        
        # Guardar imagen
        plt.imsave(ruta_salida, imagen, cmap='gray')
        print(f"Imagen guardada: {ruta_salida}")
    
    print("\nImágenes generadas exitosamente!")
    print(f"Las imágenes se encuentran en el directorio: {os.path.abspath(output_dir)}")

if __name__ == "__main__":
    main() 