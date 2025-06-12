# Módulo generador de campos topológicos y análisis

from .field_generator import (
    generate_topology_case,
    generate_vector_field,
    create_single_blob,
    create_single_blob_with_holes,
    create_multiple_blobs,
    create_complex_topology,
    create_blob,
    create_hole,
    get_safe_positions,
    create_horizontal_dominant,
    create_vertical_dominant,
    create_asymmetric_mesh,
    create_asymmetric_spiral,
    create_asymmetric_branches,
    add_noise_to_field
)

from .topology_metrics import (
    count_vertices_edges_faces_corrected,
    euler_characteristic_2d,
    euler_poincare_2d,
    validate_euler_formulas,
    compute_all_metrics,
    compute_perimeter,
    analyze_connectivity
)

from .topology_codes_extended import (
    get_f8_code,
    f8_to_f4,
    compute_vcc,
    compute_3ot
)

from .visualizer import (
    plot_topology_analysis,
    create_comparison_plot,
    plot_vector_field_enhanced,
    create_individual_case_visualization,
    save_metrics_to_csv,
    create_summary_report,
    plot_topology_codes,
    plot_topology_patterns
)

from .case_definitions import (
    get_topology_cases,
    validate_case_topology
)

from .image_reader import (
    read_binary_image,
    validate_binary_image,
    preprocess_binary_image
)

__all__ = [
    # Field generation
    'generate_topology_case',
    'generate_vector_field',
    'create_single_blob',
    'create_single_blob_with_holes',
    'create_multiple_blobs',
    'create_complex_topology',
    'create_horizontal_dominant',
    'create_vertical_dominant',
    'create_asymmetric_mesh',
    'create_asymmetric_spiral',
    'create_asymmetric_branches',
    'add_noise_to_field',
    
    # Topology metrics
    'count_vertices_edges_faces_corrected',
    'euler_characteristic_2d',
    'euler_poincare_2d',
    'validate_euler_formulas',
    'compute_all_metrics',
    'compute_perimeter',
    'analyze_connectivity',
    
    # Topology codes
    'get_f8_code',
    'f8_to_f4',
    'compute_vcc',
    'compute_3ot',
    
    # Visualization
    'plot_topology_analysis',
    'create_comparison_plot',
    'plot_vector_field_enhanced',
    'create_individual_case_visualization',
    'save_metrics_to_csv',
    'create_summary_report',
    'plot_topology_codes',
    'plot_topology_patterns',
    
    # Case definitions
    'get_topology_cases',
    'validate_case_topology',
    'create_blob',
    'create_hole',
    'get_safe_positions',
    
    # Image reader
    'read_binary_image',
    'validate_binary_image',
    'preprocess_binary_image'
]