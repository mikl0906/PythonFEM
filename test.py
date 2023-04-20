import numpy as np
import json

with open("./bar-truss-benchmark-model/fem_data/matrices.json") as matrices_file:
    matrices = json.load(matrices_file)

stiffness_matrix = np.array(matrices["stiffness-matrix"])
force_vector = np.array(matrices["force-vector"])
zero_dofs = matrices["zero-dofs"]

with open("./bar-truss-benchmark-model/fem_data/results.json") as results_file:
    results = json.load(results_file)
displacements = results["displacements"]

calc_force = np.matmul(stiffness_matrix, displacements)
print(force_vector)
print(np.round(calc_force,3))
print(np.round(calc_force - force_vector,3))
print(f"Error: {np.dot(calc_force - force_vector,calc_force - force_vector)}")