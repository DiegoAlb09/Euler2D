# Análisis Topológico 2D

Este sistema realiza análisis topológico de imágenes binarias 2D, calculando diversos códigos y métricas topológicas.

## Instalación

1. Clonar el repositorio:
```bash
git clone <url-del-repositorio>
cd Euler2D
```

2. Instalar dependencias:
```bash
pip install numpy scipy matplotlib scikit-image
```

## Uso

El sistema puede analizar imágenes binarias de dos formas:

1. Análisis de imagen individual:
```bash
python main.py ruta/a/tu/imagen.png
```

2. Generación y análisis de casos predefinidos:
```bash
python main.py --generate-cases
```

## Cálculos y Métricas

### 1. Códigos Topológicos

#### Código F8 (Freeman 8-direcciones)
- Recorre el contorno de la imagen siguiendo 8 direcciones posibles
- Cada número representa una dirección (0-7)
- Se genera analizando los 8 vecinos de cada píxel del contorno

#### Código F4 (Freeman 4-direcciones)
- Simplificación del F8 a 4 direcciones principales
- Conversión de F8 a F4:
  - 0,1 → 0 (derecha)
  - 2,3 → 1 (arriba)
  - 4,5 → 2 (izquierda)
  - 6,7 → 3 (abajo)

#### Código VCC (Vertex Correction Code)
- Basado en la secuencia de píxeles del código F4
- Representa los vértices y sus conexiones:
  - 0: No hay cambio de dirección
  - 1: Vértice con una conexión
  - 3: Vértice con tres conexiones
- Fórmula: x = (N1 - N3)/4 = β₀ - β₁

#### Código 3OT (Three Orthogonal Topology)
- Derivado del código VCC
- Representa la dirección de cada segmento:
  - 0 (h): Segmento horizontal
  - 1 (v): Segmento vertical
  - 2 (d): Segmento diagonal
- Fórmula: X = (N2h - N2v)/4 = β₀ - β₁

### 2. Números de Betti

- β₀: Número de componentes conectadas
- β₁: Número de agujeros
- Calculados usando análisis de componentes conectadas

### 3. Fórmulas de Euler

#### Característica de Euler (V-E+F)
- V: Número de vértices
- E: Número de aristas
- F: Número de caras
- χ = V - E + F

#### Euler-Poincaré (β₀-β₁)
- Relaciona los números de Betti
- χ = β₀ - β₁

### 4. Verificaciones

El sistema verifica la consistencia entre:
1. Fórmulas de Euler: V-E+F = β₀-β₁
2. VCC: x = (N1-N3)/4 = β₀-β₁
3. 3OT: X = (N2h-N2v)/4 = β₀-β₁

## Estructura del Proyecto

```
Euler2D/
├── main.py                 # Punto de entrada principal
├── config/
│   └── topology_config.py  # Configuración general
├── generator/
│   ├── field_generator.py  # Generación de casos
│   ├── topology_codes.py   # Implementación de códigos
│   ├── topology_metrics.py # Cálculo de métricas
│   └── visualizer.py       # Visualización de resultados
└── output/                 # Directorio de salida
```

## Visualizaciones

El sistema genera tres tipos de visualizaciones:
1. Análisis topológico general
2. Códigos topológicos (F8, F4, VCC, 3OT)
3. Patrones generados por cada código

## Ejemplos de Uso

1. Analizar una imagen binaria:
```python
from main import analyze_binary_image

result = analyze_binary_image("ruta/imagen.png")
print(f"Números de Betti: β₀={result['metrics']['beta0']}, β₁={result['metrics']['beta1']}")
```

2. Generar y analizar un caso específico:
```python
from generator.field_generator import generate_topology_case

field = generate_topology_case("single_blob", size=(256, 256))
result = analyze_binary_image(field)
```

## Contribución

1. Fork el repositorio
2. Crea una rama para tu feature (`git checkout -b feature/nombre`)
3. Commit tus cambios (`git commit -am 'Añadir nueva feature'`)
4. Push a la rama (`git push origin feature/nombre`)
5. Crea un Pull Request
