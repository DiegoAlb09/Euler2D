# Análisis Topológico 2D - Fórmulas de Euler

Un sistema completo para generar, analizar y visualizar topologías 2D utilizando las fórmulas de Euler y números de Betti. Este proyecto implementa algoritmos para validar la consistencia entre diferentes formulaciones de la característica de Euler en espacios discretos 2D.

## 🔬 Características Principales

- **Generación de Topologías**: Creación automática de diferentes casos topológicos (blobs, agujeros, componentes múltiples)
- **Cálculo de Números de Betti**: Implementación de algoritmos para calcular β₀ (componentes conectados) y β₁ (agujeros topológicos)
- **Validación de Fórmulas de Euler**: Comparación entre χ = V - E + F y χ = β₀ - β₁
- **Visualización Avanzada**: Gráficos detallados con campos vectoriales y análisis métrico
- **Análisis Comparativo**: Evaluación simultánea de múltiples casos topológicos

## 📊 Ejemplos de Análisis

### Caso: Blob Simple
Un componente conectado sin agujeros.

**Métricas Esperadas:**
- β₀ = 1 (un componente)
- β₁ = 0 (sin agujeros)
- χ = 1 (característica de Euler)

```
Análisis Topológico:
├── β₀ (Componentes): 1
├── β₁ (Agujeros): 0
├── V (Vértices): 12,847
├── E (Aristas): 25,693
├── F (Caras): 12,847
├── χ (V-E+F): 1
├── χ (β₀-β₁): 1
└── Consistencia: ✓
```

### Caso: Blob con Agujero
Un componente con un agujero interno.

**Métricas Esperadas:**
- β₀ = 1 (un componente)
- β₁ = 1 (un agujero)
- χ = 0 (característica de Euler)

```
Análisis Topológico:
├── β₀ (Componentes): 1
├── β₁ (Agujeros): 1
├── V (Vértices): 15,234
├── E (Aristas): 30,467
├── F (Caras): 15,233
├── χ (V-E+F): 0
├── χ (β₀-β₁): 0
└── Consistencia: ✓
```

### Caso: Dos Blobs Separados
Dos componentes conectados independientes.

**Métricas Esperadas:**
- β₀ = 2 (dos componentes)
- β₁ = 0 (sin agujeros)
- χ = 2 (característica de Euler)

```
Análisis Topológico:
├── β₀ (Componentes): 2
├── β₁ (Agujeros): 0
├── V (Vértices): 8,456
├── E (Aristas): 16,910
├── F (Caras): 8,456
├── χ (V-E+F): 2
├── χ (β₀-β₁): 2
└── Consistencia: ✓
```

## 🏗️ Estructura del Proyecto

```
topology-analysis/
│
├── config/
│   └── topology_config.py          # Configuración de parámetros
│
├── generator/
│   ├── __init__.py                 # Exportaciones del módulo
│   ├── field_generator.py          # Generación de campos topológicos
│   ├── topology_metrics.py         # Cálculo de métricas topológicas
│   ├── visualizer.py              # Visualización y reportes
│   └── case_definitions.py        # Definiciones de casos de prueba
│
├── main.py                        # Programa principal
└── README.md                      # Este archivo
```

## 🚀 Instalación y Uso

### Requisitos

```bash
# Dependencias principales
pip install numpy scipy matplotlib pandas seaborn scikit-image
```

### Ejecución

```bash
# Ejecutar análisis completo
python main.py
```

### Salida Generada

El programa crea la siguiente estructura de archivos:

```
output/
├── individual/                    # Análisis por caso individual
│   ├── single_blob/
│   ├── blob_with_hole/
│   └── ...
├── comparison/                    # Gráficos comparativos
│   └── topology_comparison.png
├── metrics/                       # Datos y reportes
│   ├── topology_metrics.csv
│   └── topology_report.txt
└── images/                        # Imágenes adicionales
```

## 📈 Tipos de Visualización

### 1. Análisis Individual Completo
Cada caso genera una visualización de 4 paneles:
- **Panel Superior Izquierdo**: Topología original con métricas β₀ y β₁
- **Panel Superior Derecho**: Campo vectorial superpuesto
- **Panel Superior Derecho**: Comparación de fórmulas de Euler
- **Panel Inferior**: Tabla completa de métricas

### 2. Comparación Multi-Caso
Gráfico de 4 paneles comparando todos los casos:
- **Números de Betti**: Barras comparativas de β₀ y β₁
- **Característica de Euler**: Valores de χ por caso
- **Consistencia**: Estado de validación de fórmulas
- **Mapa de Calor**: Visualización matricial de todas las métricas

### 3. Campo Vectorial Detallado
Visualización dual del campo vectorial:
- Campo direccional superpuesto a la topología
- Mapa de magnitud del campo vectorial

## 🧮 Fundamentos Matemáticos

### Números de Betti
- **β₀**: Número de componentes conectados
- **β₁**: Número de agujeros topológicos (genus)

### Fórmulas de Euler
1. **Clásica**: χ = V - E + F
   - V: Vértices de la malla discreta
   - E: Aristas de la malla discreta
   - F: Caras (píxeles activos)

2. **Euler-Poincaré**: χ = β₀ - β₁
   - Basada en números de Betti

### Casos de Prueba Implementados

| Caso | Descripción | β₀ | β₁ | χ |
|------|-------------|----|----|---|
| `single_blob` | Un blob sin agujeros | 1 | 0 | 1 |
| `blob_with_hole` | Un blob con un agujero | 1 | 1 | 0 |
| `blob_with_three_holes` | Un blob con tres agujeros | 1 | 3 | -2 |
| `two_blobs` | Dos blobs separados | 2 | 0 | 2 |
| `two_blobs_one_hole` | Dos blobs, uno con agujero | 2 | 1 | 1 |
| `complex_topology` | Topología compleja | 3 | 2 | 1 |

## 🔧 Configuración

### Parámetros de Imagen
```python
IMAGE_CONFIG = {
    'default_size': (256, 256),
    'output_format': 'png',
    'dpi': 150
}
```

### Parámetros de Visualización
```python
VISUALIZATION_CONFIG = {
    'vector_field_step': 8,        # Paso para flechas del campo
    'arrow_scale': 15,             # Escala de flechas
    'arrow_color': 'red',          # Color de flechas
    'background_cmap': 'gray',     # Mapa de colores de fondo
    'figsize': (10, 8),           # Tamaño de figura
    'dpi': 150                     # Resolución
}
```

### Parámetros Topológicos
```python
TOPOLOGY_CONFIG = {
    'blob_radius_range': (30, 50),          # Rango de radios para blobs
    'hole_radius_range': (15, 25),          # Rango de radios para agujeros
    'min_distance_between_features': 40,     # Distancia mínima entre características
    'smoothing_sigma': 2.0                  # Parámetro de suavizado gaussiano
}
```

## 📝 Ejemplo de Reporte

```
REPORTE DE ANÁLISIS TOPOLÓGICO
==================================================

CASO: single_blob
------------------------------
Números de Betti:
  β₀ (Componentes conectados): 1
  β₁ (Agujeros topológicos): 0

Características de Euler:
  χ = V - E + F = 12847 - 25693 + 12847 = 1
  χ = β₀ - β₁ = 1 - 0 = 1

Consistencia: ✓
Fracción de área: 0.1962
Perímetro: 1847

==================================================
```

## 🎯 Aplicaciones

- **Investigación en Topología Computacional**: Validación de algoritmos topológicos
- **Análisis de Materiales**: Caracterización de porosidad y conectividad
- **Procesamiento de Imágenes**: Análisis topológico de estructuras binarias
- **Educación**: Demostración visual de conceptos topológicos fundamentales
- **Validación Numérica**: Verificación de implementaciones de fórmulas de Euler

## 📚 Referencias

1. Hatcher, A. (2002). *Algebraic Topology*. Cambridge University Press.
2. Edelsbrunner, H., & Harer, J. (2010). *Computational Topology: An Introduction*. American Mathematical Society.
3. Zomorodian, A. (2005). *Topology for Computing*. Cambridge University Press.

---

**Desarrollado para el análisis y visualización de topologías discretas 2D**