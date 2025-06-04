from generator.field_generator import generate_field_with_holes, generate_vector_field
from generator.visualizer import plot_vector_field_with_mask
from generator.topology_metrics import compute_betti_numbers
import os

os.makedirs("output", exist_ok=True)

cases = [
    "one_blob_three_holes",
    "two_blobs",
    "two_blobs_one_with_hole"
]

for i, case in enumerate(cases):
    # Primero generamos el campo base con agujeros
    field = generate_field_with_holes(size=(100, 100))
    # Luego generamos el campo vectorial
    u, v = generate_vector_field(field)
    beta0, beta1 = compute_betti_numbers(field)
    chi = beta0 - beta1
    print(f"[{case}] β0 = {beta0}, β1 = {beta1}, χ = {chi}")
    plot_vector_field_with_mask(u, v, field, f"output/frame_{i:03}.png")

