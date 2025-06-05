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
Cada caso genera una visualización de 6 paneles:
- **Panel Superior Izquierdo**: Topología original con métricas β₀ y β₁
- **Panel Superior Derecho**: Campo vectorial superpuesto
- **Panel Central Izquierdo**: Comparación de fórmulas de Euler y VCC
- **Panel Central Derecho**: Análisis detallado de VCC (N1, N3)
- **Panel Inferior**: Análisis 3OT con distribución direccional
- **Panel Final**: Tabla completa de métricas y códigos generados

### 2. Comparación Multi-Caso
Gráfico de 4 paneles comparando todos los casos:
- **Números de Betti**: Barras comparativas de β₀ y β₁
- **Característica de Euler y VCC**: Valores de χ y x por caso
- **Análisis 3OT**: Distribución direccional por caso
- **Mapa de Calor**: Visualización matricial de todas las métricas

### 3. Campo Vectorial Detallado
Visualización dual del campo vectorial:
- Campo direccional superpuesto a la topología
- Mapa de magnitud del campo vectorial

### 4. Análisis de Códigos Topológicos
Visualización específica de códigos:
- **Panel VCC**: 
  * Distribución de vértices por tipo de conexión
  * Comparación x vs χ
  * Código binario generado
- **Panel 3OT**:
  * Distribución de segmentos por dirección
  * Longitudes medias y máximas
  * Rosas de dirección
  * Código binario generado

## 🧮 Fundamentos Matemáticos

### Números de Betti
- **β₀**: Número de componentes conectados
- **β₁**: Número de agujeros topológicos (genus)

### Códigos Topológicos

#### 1. VCC (Vertex Correction Code)
- **Definición**: Código basado en el análisis de vértices y sus conexiones
- **Componentes principales**:
  - N1: Número de vértices con una conexión
  - N3: Número de vértices con tres conexiones
  - x = (N1 - N3)/4: Valor de corrección que debe coincidir con χ
- **Validación**: El valor x debe ser igual a la característica de Euler (χ)
- **Aplicaciones**: 
  - Verificación de consistencia topológica
  - Detección de anomalías en la conectividad
  - Análisis de estructura local

#### 2. 3OT (Three Orthogonal Topology)
- **Definición**: Análisis basado en segmentos en tres direcciones principales
- **Componentes**:
  - N2h: Número de segmentos horizontales
  - N2v: Número de segmentos verticales
  - N2d: Número de segmentos diagonales
  - X = (N2h - N2v)/4: Valor que caracteriza la orientación predominante
- **Métricas adicionales**:
  - Longitud media y máxima por dirección
  - Ratio direccional
  - Distribución de longitudes
- **Aplicaciones**:
  - Análisis de orientación preferencial
  - Caracterización de anisotropía
  - Estudio de patrones direccionales

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

### Características de Seguridad
- Validación de límites para todas las operaciones
- Manejo robusto de casos extremos
- Sistema de respaldo para generación de características
- Prevención de superposición de elementos

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

Análisis VCC (Vertex Correction Code):
  N1 (vértices con una conexión): 4
  N3 (vértices con tres conexiones): 0
  N1 - N3: 4
  x = (N1 - N3)/4: 1.00
  Código binario: 1000
  Verificación con Euler-Poincaré:
    VCC (x): 1.00
    E-P (β₀-β₁): 1
    Diferencia: 0.000000
    Consistencia: ✓

Análisis 3OT (Three Orthogonal Topology):
  N2h (segmentos horizontales): 12
  N2v (segmentos verticales): 8
  N2d (segmentos diagonales): 6
  X = (N2h - N2v)/4: 1.00
  Código binario: 1100

  Dirección Horizontal:
    Número de segmentos: 12
    Longitud media: 8.50
    Longitud máxima: 15
    Distribución de longitudes: 5, 8, 10, 12, 15

  Dirección Vertical:
    Número de segmentos: 8
    Longitud media: 7.25
    Longitud máxima: 12
    Distribución de longitudes: 4, 7, 9, 12

  Dirección Diagonal:
    Número de segmentos: 6
    Longitud media: 5.33
    Longitud máxima: 8
    Distribución de longitudes: 3, 5, 8

  Métricas Combinadas 3OT:
    Total de segmentos: 26
    Longitud media global: 7.27
    Longitud máxima global: 15
    Ratio direccional: 1.50

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

### Mejoras Recientes

#### 1. Generación de Posiciones Seguras
- Implementación mejorada para la distribución de características
- Sistema de respaldo para posiciones determinísticas
- Mejor manejo de casos con múltiples componentes
- Distribución uniforme para 2 o más elementos

#### 2. Manejo de Agujeros
- Detección robusta de agujeros internos
- Validación mejorada de bordes
- Distribución angular para múltiples agujeros
- Sistema de respaldo para colocación de agujeros

#### 3. Análisis de Conectividad
- Análisis detallado de componentes individuales
- Métricas de tamaño y distribución
- Conteo preciso de agujeros por componente
- Validación topológica mejorada

## 📊 Guía de Interpretación de Resultados

### Interpretación de Números de Betti
1. **β₀ (Beta-0)**
   - Representa el número de componentes conectados
   - Un β₀ = 1 significa una única pieza
   - Un β₀ > 1 indica múltiples piezas separadas
   - Ejemplo: Dos círculos separados tienen β₀ = 2

2. **β₁ (Beta-1)**
   - Representa el número de agujeros o ciclos
   - Un β₁ = 0 significa que no hay agujeros
   - Cada agujero aumenta β₁ en 1
   - Ejemplo: Un anillo tiene β₁ = 1

### Fórmulas de Euler y su Significado

#### 1. Fórmula Clásica (χ = V - E + F)
- **V (Vértices)**: Puntos en la malla discreta
- **E (Aristas)**: Conexiones entre vértices
- **F (Caras)**: Áreas encerradas (píxeles)
- Esta fórmula es útil para:
  * Verificar la integridad de la malla
  * Detectar errores en la discretización
  * Analizar la estructura local

#### 2. Fórmula de Euler-Poincaré (χ = β₀ - β₁)
- Basada en características globales
- Más intuitiva para interpretar la forma general
- Ventajas:
  * No depende de la discretización
  * Captura propiedades topológicas globales
  * Más robusta ante pequeñas variaciones

### Relación entre Ambas Fórmulas
- Ambas deben dar el mismo resultado (χ)
- Si difieren, posibles causas:
  * Errores en la discretización
  * Problemas en la detección de bordes
  * Inconsistencias en la conectividad

### Ejemplos Prácticos de Interpretación

1. **Objeto Simple (χ = 1)**
   - Un círculo lleno o un cuadrado
   - β₀ = 1 (una pieza)
   - β₁ = 0 (sin agujeros)
   - V - E + F = 1

2. **Anillo (χ = 0)**
   - Un círculo con un agujero
   - β₀ = 1 (una pieza)
   - β₁ = 1 (un agujero)
   - V - E + F = 0

3. **Objeto Complejo (χ = -1)**
   - Una pieza con dos agujeros
   - β₀ = 1 (una pieza)
   - β₁ = 2 (dos agujeros)
   - V - E + F = -1

## 🔄 Funcionamiento del Proyecto

### Flujo de Ejecución

1. **Inicialización**
   ```python
   # En main.py
   output_dir = "output"
   image_size = IMAGE_CONFIG['default_size']
   seed = 42  # Para reproducibilidad
   ```

2. **Carga de Casos**
   ```python
   # Obtener casos definidos en topology_config.py
   topology_cases = get_topology_cases()
   case_names = list(topology_cases.keys())
   ```

3. **Procesamiento por Caso**
   ```python
   for case_name in case_names:
       result = process_topology_case(case_name, image_size, seed)
   ```

### Funciones Principales

#### 1. Generación de Topología
```python
def generate_topology_case(case_name, size=(256, 256), seed=None):
    """
    Genera un caso específico de topología.
    
    Casos disponibles:
    - single_blob: Un blob simple
    - blob_with_hole: Blob con un agujero
    - blob_with_three_holes: Blob con tres agujeros
    - two_blobs: Dos blobs separados
    - two_blobs_one_hole: Dos blobs, uno con agujero
    - complex_topology: Topología compleja
    """
```

#### 2. Cálculo de Métricas
```python
def compute_all_metrics(binary_image):
    """
    Calcula todas las métricas topológicas:
    - Números de Betti (β₀, β₁)
    - Vértices, Aristas, Caras
    - Características de Euler
    - Área y perímetro
    """
```

#### 3. Análisis de Conectividad
```python
def analyze_connectivity(binary_image):
    """
    Analiza propiedades de conectividad:
    - Número de componentes
    - Tamaño de componentes
    - Agujeros por componente
    - Distribución espacial
    """
```

### Proceso Detallado de Análisis

1. **Generación de Campo**
   - Creación de blobs y agujeros
   - Posicionamiento seguro de elementos
   - Validación de geometría

2. **Análisis Topológico**
   - Cálculo de números de Betti
   - Conteo de elementos discretos (V,E,F)
   - Validación de fórmulas de Euler

3. **Visualización**
   - Generación de campos vectoriales
   - Creación de gráficos comparativos
   - Exportación de resultados

### Funciones de Visualización

#### 1. Análisis Individual
```python
def plot_topology_analysis(field, u, v, metrics, save_path, case_name=""):
    """
    Crea visualización completa con:
    - Campo escalar
    - Campo vectorial
    - Métricas topológicas
    - Comparación de fórmulas
    """
```

#### 2. Comparación Multi-caso
```python
def create_comparison_plot(cases_data, save_path):
    """
    Genera gráficos comparativos:
    - Números de Betti
    - Características de Euler
    - Consistencia de fórmulas
    - Mapa de calor de métricas
    """
```

### Generación de Reportes

1. **Métricas CSV**
```python
def save_metrics_to_csv(cases_data, save_path):
    """
    Exporta métricas detalladas:
    - Métricas por caso
    - Valores numéricos
    - Estadísticas comparativas
    """
```

2. **Reporte de Texto**
```python
def create_summary_report(cases_data, save_path):
    """
    Genera reporte detallado:
    - Análisis por caso
    - Validación de fórmulas
    - Estadísticas globales
    """
```

### Validación y Control de Calidad

1. **Validación de Casos**
```python
def validate_case_topology(case_name, calculated_metrics):
    """
    Verifica que las métricas coincidan
    con los valores esperados para cada caso
    """
```

2. **Consistencia de Euler**
```python
def validate_euler_formulas(binary_image, tolerance=0):
    """
    Compara las dos formulaciones de Euler
    y valida su consistencia
    """
```

### Configuración y Personalización

Los parámetros clave se pueden ajustar en `config/topology_config.py`:

1. **Parámetros de Generación**
   - Tamaños de blob y agujeros
   - Distancias mínimas
   - Parámetros de suavizado

2. **Parámetros de Visualización**
   - Resolución de imágenes
   - Configuración de campos vectoriales
   - Estilos de gráficos