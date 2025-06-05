# Módulo generador de campos topológicos y análisis

from .field_generator import (
    generate_topology_case,
    generate_vector_field,
    create_single_blob,
    create_single_blob_with_holes,
    create_multiple_blobs,
    create_complex_topology
)

from .topology_metrics import (
    compute_betti_numbers_2d,
    euler_characteristic_2d,
    euler_poincare_2d,
    validate_euler_formulas,
    compute_all_metrics,
    analyze_connectivity
)

from .visualizer import (
    plot_topology_analysis,
    create_comparison_plot,
    plot_vector_field_enhanced,
    create_individual_case_visualization,
    save_metrics_to_csv,
    create_summary_report
)

from .case_definitions import (
    get_topology_cases,
    validate_case_topology,
    create_blob,
    create_hole,
    get_safe_positions
)

__all__ = [
    # Field generation
    'generate_topology_case',
    'generate_vector_field',
    'create_single_blob',
    'create_single_blob_with_holes',
    'create_multiple_blobs',
    'create_complex_topology',
    
    # Topology metrics
    'compute_betti_numbers_2d',
    'euler_characteristic_2d',
    'euler_poincare_2d',
    'validate_euler_formulas',
    'compute_all_metrics',
    'analyze_connectivity',
    
    # Visualization
    'plot_topology_analysis',
    'create_comparison_plot',
    'plot_vector_field_enhanced',
    'create_individual_case_visualization',
    'save_metrics_to_csv',
    'create_summary_report',
    
    # Case definitions
    'get_topology_cases',
    'validate_case_topology',
    'create_blob',
    'create_hole',
    'get_safe_positions'
]