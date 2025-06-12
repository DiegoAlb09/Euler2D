"""
Definiciones de casos de topología y sus validaciones
"""

def get_topology_cases():
    """
    Retorna un diccionario con los casos de topología predefinidos y sus características esperadas
    
    Returns:
        dict: Diccionario con los casos y sus métricas esperadas
    """
    return {
        'single_blob': {
            'beta0': 1,  # Un componente conectado
            'beta1': 0,  # Sin agujeros
            'euler': 1   # χ = β₀ - β₁ = 1
        },
        'blob_with_hole': {
            'beta0': 1,  # Un componente conectado
            'beta1': 1,  # Un agujero
            'euler': 0   # χ = β₀ - β₁ = 0
        },
        'blob_with_three_holes': {
            'beta0': 1,  # Un componente conectado
            'beta1': 3,  # Tres agujeros
            'euler': -2  # χ = β₀ - β₁ = -2
        },
        'two_blobs': {
            'beta0': 2,  # Dos componentes conectados
            'beta1': 0,  # Sin agujeros
            'euler': 2   # χ = β₀ - β₁ = 2
        },
        'two_blobs_one_hole': {
            'beta0': 2,  # Dos componentes conectados
            'beta1': 1,  # Un agujero
            'euler': 1   # χ = β₀ - β₁ = 1
        },
        'complex_topology': {
            'beta0': 3,  # Tres componentes conectados
            'beta1': 2,  # Dos agujeros
            'euler': 1   # χ = β₀ - β₁ = 1
        },
        'irregular_star': {
            'beta0': 1,  # Un componente conectado
            'beta1': 5,  # Cinco agujeros
            'euler': -4  # χ = β₀ - β₁ = -4
        },
        'irregular_chain': {
            'beta0': 1,  # Un componente conectado
            'beta1': 3,  # Tres agujeros
            'euler': -2  # χ = β₀ - β₁ = -2
        },
        'irregular_mesh': {
            'beta0': 1,  # Un componente conectado
            'beta1': 4,  # Cuatro agujeros
            'euler': -3  # χ = β₀ - β₁ = -3
        },
        'irregular_clusters': {
            'beta0': 4,  # Cuatro componentes conectados
            'beta1': 2,  # Dos agujeros
            'euler': 2   # χ = β₀ - β₁ = 2
        },
        'spiral_holes': {
            'beta0': 1,  # Un componente conectado
            'beta1': 3,  # Tres agujeros en espiral
            'euler': -2  # χ = β₀ - β₁ = -2
        },
        'horizontal_dominant': {
            'beta0': 1,  # Un componente conectado
            'beta1': 2,  # Dos agujeros
            'euler': -1  # χ = β₀ - β₁ = -1
        },
        'vertical_dominant': {
            'beta0': 1,  # Un componente conectado
            'beta1': 2,  # Dos agujeros
            'euler': -1  # χ = β₀ - β₁ = -1
        },
        'asymmetric_mesh': {
            'beta0': 1,  # Un componente conectado
            'beta1': 3,  # Tres agujeros
            'euler': -2  # χ = β₀ - β₁ = -2
        },
        'asymmetric_spiral': {
            'beta0': 1,  # Un componente conectado
            'beta1': 2,  # Dos agujeros
            'euler': -1  # χ = β₀ - β₁ = -1
        },
        'asymmetric_branches': {
            'beta0': 1,  # Un componente conectado
            'beta1': 3,  # Tres agujeros
            'euler': -2  # χ = β₀ - β₁ = -2
        }
    }

def validate_case_topology(case_name, metrics, tolerance=1e-10):
    """
    Valida que las métricas de un caso coincidan con los valores esperados
    
    Args:
        case_name: Nombre del caso a validar
        metrics: Diccionario con las métricas calculadas
        tolerance: Tolerancia permitida en comparaciones numéricas
        
    Returns:
        bool: True si las métricas coinciden con lo esperado
    """
    # Obtener casos predefinidos
    cases = get_topology_cases()
    
    # Si el caso no está definido, no se puede validar
    if case_name not in cases:
        return False
    
    # Obtener valores esperados
    expected = cases[case_name]
    
    # Validar cada métrica
    beta0_valid = metrics['beta0'] == expected['beta0']
    beta1_valid = metrics['beta1'] == expected['beta1']
    euler_valid = abs(metrics['euler_poincare'] - expected['euler']) <= tolerance
    
    # Todas las métricas deben ser válidas
    return beta0_valid and beta1_valid and euler_valid 