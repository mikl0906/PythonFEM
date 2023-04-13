import json
import time
import numpy as np
from core import solve_gaussian
from core import solve_lu

print("\n# Solver started")
start_time = time.time()

with open("./fem_data/matrices.json") as matrices_file:
    matrices = json.load(matrices_file)

stiffness_matrix = np.array(matrices["stiffness-matrix"])
force_vector = np.array(matrices["force-vector"])
zero_dofs = matrices["zero-dofs"]

solution = solve_gaussian(stiffness_matrix, force_vector)

displacements = np.copy(solution)
for zero_dof in zero_dofs:
    displacements = np.insert(displacements, zero_dof, 0)

result_file_content = {
    "displacements": displacements.tolist()
}

with open("./results/results.json", "w") as results_file:
    json.dump(result_file_content, results_file, indent=2)

print(f"# Solver finished. Time elapsed: {round(time.time() - start_time, 8)}")