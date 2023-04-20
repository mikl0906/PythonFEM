import json
import time
import numpy as np
import sys
from core import solve_gaussian, solve_lu

solve_function = {
    "gaussian": solve_gaussian,
    "lu": solve_lu
}

# Time tracker
print("\n# Solver started")
start_time = time.time()

try:
    model_path = sys.argv[1]
except:
    print("No model folder name provided")
    exit(1)

# Open settings file
with open(f"{model_path}/settings.json") as settings_file:
    analysis_settings = json.load(settings_file)["analysis-settings"]
solver = analysis_settings["solver"]
print(f"Solver: {solver}")

# Open matrices file and import data
with open(f"{model_path}/fem_data/matrices.json") as matrices_file:
    matrices = json.load(matrices_file)

stiffness_matrix = np.array(matrices["stiffness-matrix"])
force_vector = np.array(matrices["force-vector"])
zero_dofs = matrices["zero-dofs"]

# Remove zero rows and dofs
for i, row in enumerate(stiffness_matrix):
    if np.dot(row, row) < 0.001:
        zero_dofs.append(i)
zero_dofs = list(map(int, set(zero_dofs)))
stiffness_matrix_reduced = np.delete(np.delete(stiffness_matrix, zero_dofs, axis=0), zero_dofs, axis=1)
force_vector_reduced = np.delete(force_vector, zero_dofs)

# Find the solution of the system
displacements = solve_function[solver](stiffness_matrix_reduced, force_vector_reduced)

# Insert zero dofs
for zero_dof in zero_dofs:
    displacements = np.insert(displacements, zero_dof, 0)
# Output maximum translation
print(f"Maximum translation: {round(np.max(displacements),3)} mm")

# Find the reaction forces
reactions = np.matmul(stiffness_matrix, displacements) - force_vector

# Write result file
result_file_content = {
    "displacements": np.round(displacements,5).tolist(),
    "reaction-forces": np.round(reactions,5).tolist()
}
with open(f"{model_path}/fem_data/results.json", "w") as results_file:
    json.dump(result_file_content, results_file, indent=2)

# Time tracker
print(f"# Solver finished. Time elapsed: {round(time.time() - start_time, 8)}\n")