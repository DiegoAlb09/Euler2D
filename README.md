# Euler2D

Euler2D es una biblioteca Python para el análisis topológico de imágenes 2D utilizando la característica de Euler y otros descriptores topológicos avanzados.

## Características Principales

- **Análisis Topológico Completo**
  - Cálculo de números de Betti (β₀, β₁)
  - Característica de Euler por dos métodos: V-E+F y β₀-β₁
  - Validación de consistencia entre fórmulas
  - Análisis de conectividad y componentes

- **Códigos Topológicos Avanzados**
  - VCC (Vertex Correction Code)
    - Análisis de vértices con una y tres conexiones
    - Verificación de consistencia con Euler-Poincaré
  - 3OT (Three Orthogonal Topology)
    - Análisis de segmentos horizontales, verticales y diagonales
    - Métricas direccionales y ratios de asimetría

- **Generación de Patrones**
  - Casos predefinidos con topologías específicas
  - Generación de blobs y agujeros
  - Patrones asimétricos y estructuras complejas
  - Campo vectorial asociado

- **Visualización Avanzada**
  - Gráficos detallados de análisis topológico
  - Visualización de campos vectoriales
  - Comparativas entre casos
  - Reportes y métricas detalladas

## Instalación

```bash
# Clonar el repositorio
git clone https://github.com/tu-usuario/Euler2D.git
cd Euler2D

# Instalar dependencias
pip install -r requirements.txt
```

## Uso Básico

```python
from generator import generate_topology_case, compute_all_metrics

# Generar un caso de topología
field = generate_topology_case('single_blob')

# Calcular métricas
metrics = compute_all_metrics(field)

print(f"β₀ = {metrics['beta0']}")  # Número de componentes
print(f"β₁ = {metrics['beta1']}")  # Número de agujeros
print(f"χ = {metrics['euler_poincare']}")  # Característica de Euler
```

## Casos de Topología Disponibles

- `single_blob`: Blob único sin agujeros
- `blob_with_hole`: Blob con un agujero
- `blob_with_three_holes`: Blob con tres agujeros
- `two_blobs`: Dos blobs separados
- `two_blobs_one_hole`: Dos blobs, uno con agujero
- `complex_topology`: Topología compleja con múltiples características
- `irregular_star`: Forma de estrella irregular
- `irregular_chain`: Cadena de blobs conectados
- `irregular_mesh`: Malla irregular con agujeros
- `irregular_clusters`: Clusters con conexiones
- `spiral_holes`: Espiral con agujeros distribuidos
- `horizontal_dominant`: Estructura con dominancia horizontal
- `vertical_dominant`: Estructura con dominancia vertical
- `asymmetric_mesh`: Malla asimétrica
- `asymmetric_spiral`: Espiral asimétrica
- `asymmetric_branches`: Estructura ramificada asimétrica

## Estructura del Proyecto

```
Euler2D/
├── config/
│   └── topology_config.py    # Configuraciones y parámetros
├── generator/
│   ├── __init__.py          # Exportación de módulos
│   ├── field_generator.py    # Generación de campos
│   ├── topology_metrics.py   # Cálculo de métricas
│   ├── topology_codes.py     # Códigos VCC y 3OT
│   ├── case_definitions.py   # Definición de casos
│   └── visualizer.py        # Visualización y reportes
└── main.py                  # Script principal
```

## Ejemplos de Uso

### Análisis Completo de un Caso

```python
from main import process_topology_case

# Procesar un caso específico
result = process_topology_case('complex_topology')

# Los resultados incluyen:
# - Campo escalar y vectorial
# - Métricas topológicas
# - Códigos VCC y 3OT
# - Análisis de conectividad
```

### Generación de Reportes

```python
from main import save_results

# Procesar múltiples casos y guardar resultados
results = [process_topology_case(case) for case in cases]
save_results(results, 'output_directory')

# Genera:
# - Visualizaciones individuales
# - Gráficos comparativos
# - Métricas en CSV
# - Reporte detallado
```

## Contribuir

Las contribuciones son bienvenidas. Por favor, sigue estos pasos:

1. Fork el repositorio
2. Crea una rama para tu característica (`git checkout -b feature/nueva-caracteristica`)
3. Realiza tus cambios y haz commit (`git commit -am 'Añade nueva característica'`)
4. Push a la rama (`git push origin feature/nueva-caracteristica`)
5. Crea un Pull Request

## Licencia

Este proyecto está licenciado bajo la Licencia MIT - ver el archivo LICENSE para más detalles.