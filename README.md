# Análisis Topológico 2D

Este sistema realiza análisis topológico avanzado de imágenes binarias 2D, calculando diversos códigos y métricas topológicas con visualizaciones interactivas.

## 📋 Características Principales

- Análisis de características de Euler mediante múltiples métodos
- Cálculo de códigos topológicos (F8, F4, VCC, 3OT)
- Visualización interactiva de resultados
- Generación de casos de prueba
- Análisis estadístico detallado
- Exportación de resultados en formato HTML

## 🚀 Instalación

1. Clonar el repositorio:
```bash
git clone https://github.com/DiegoAlb09/Euler2D.git
cd Euler2D
```

2. Crear un entorno virtual (recomendado):
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3. Instalar dependencias:
```bash
pip install -r requirements.txt
```

## 💻 Uso

### Análisis de Imágenes

1. Análisis de imagenes:
```bash
python main.py
```

### Ejemplos de Código

```python
from main import analyze_binary_image

# Análisis básico
result = analyze_binary_image("imagen.png")
print(f"Números de Betti: β₀={result['metrics']['beta0']}, β₁={result['metrics']['beta1']}")

# Análisis con visualización
result = analyze_binary_image("imagen.png", visualize=True)
```

## 📊 Métricas y Cálculos

### 1. Características de Euler

#### Fórmula Clásica (V-E+F)
- V: Número de vértices
- E: Número de aristas
- F: Número de caras
- χ = V - E + F

#### Fórmula de Euler-Poincaré (β₀-β₁)
- β₀: Número de componentes conectadas
- β₁: Número de agujeros
- χ = β₀ - β₁

### 2. Códigos Topológicos

#### Código F8 (Freeman 8-direcciones)
- Representación del contorno en 8 direcciones (0-7)
- Análisis de vecindad 8-conectada
- Conversión automática a F4

#### Código F4 (Freeman 4-direcciones)
- Simplificación a 4 direcciones principales
- Mapeo: 0,1→0, 2,3→1, 4,5→2, 6,7→3
- Base para códigos VCC y 3OT

#### Código VCC (Vertex Correction Code)
- Análisis de vértices y conexiones
- Cálculo: χ = (N1-N3)/4
- N1: vértices con una conexión
- N3: vértices con tres conexiones

#### Código 3OT (Three Orthogonal Topology)
- Análisis direccional de segmentos
- Clasificación: H(horizontal), V(vertical), D(diagonal)
- Cálculo: χ = (N2h-N2v)/4

## 📈 Visualizaciones y Análisis

El sistema genera visualizaciones interactivas que incluyen:

1. **Distribución de Componentes**
   - Gráfico de barras de componentes conexas
   - Análisis de conectividad

2. **Análisis de Agujeros**
   - Distribución de genus
   - Patrones de agujeros

3. **Comparación de Métodos**
   - Gráficos comparativos de características de Euler
   - Validación de consistencia

4. **Métricas VCC vs 3OT**
   - Comparación de códigos topológicos
   - Análisis de correlación

## 📁 Estructura del Proyecto

```
Euler2D/
├── main.py                 # Punto de entrada principal
├── analyze_image.py        # Análisis de imágenes
├── generate_test_images.py # Generación de casos
├── config/
│   └── topology_config.py  # Configuración
├── generator/
│   ├── field_generator.py  # Generación de campos
│   ├── topology_codes.py   # Implementación de códigos
│   └── visualizer.py       # Visualización
├── images/                 # Imágenes de prueba
├── test_images/           # Imágenes generadas
└── output/                # Resultados y visualizaciones
```

## 📊 Resultados y Análisis

Los resultados se presentan en formato HTML interactivo (`topology_analysis.html`) e incluyen:

1. **Tabla de Métricas**
   - Componentes y agujeros
   - Características de Euler
   - Códigos topológicos
   - Verificación de consistencia

2. **Gráficos Analíticos**
   - Distribución de componentes
   - Análisis de agujeros
   - Comparación de métodos
   - Métricas VCC vs 3OT

3. **Análisis por Categorías**
   - Formas simples
   - Formas con agujeros
   - Estructuras complejas

## 🤝 Contribución

1. Fork el repositorio
2. Crea una rama para tu feature (`git checkout -b feature/nombre`)
3. Commit tus cambios (`git commit -am 'Añadir nueva feature'`)
4. Push a la rama (`git push origin feature/nombre`)
5. Crea un Pull Request

## 📝 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.
