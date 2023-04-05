import json
import numpy as np

print("Solver started\n")

with open("./fem_data/matrices.json") as matrices_file:
    matrices = json.load(matrices_file)

stiffness_matrix = matrices["stiffness-matrix"]
force_vector = matrices["force-vector"]
zero_dofs = matrices["zero-dofs"]

n_of_dofs = np.size(force_vector)
solution = np.zeros(n_of_dofs)

# Augmented matrix
a = np.array([np.append(row, force_vector[i]) for i, row in enumerate(stiffness_matrix)])

for i in range(n_of_dofs - 1):
    if a[i][i] == 0:
        print("Error")
        break
    for j in range(i + 1, n_of_dofs):
        ratio = a[j][i] / a[i][i]

        for k in range(n_of_dofs + 1):
            a[j][k] = a[j][k] - ratio*a[i][k]

solution[n_of_dofs - 1] = a[n_of_dofs - 1][n_of_dofs] / a[n_of_dofs - 1][n_of_dofs - 1]

for i in range(n_of_dofs - 2, -1, -1):
    solution[i] = a[i][n_of_dofs]
    for j in range(i + 1, n_of_dofs):
        solution[i] -= a[i][j]*solution[j]

    solution[i] /= a[i][i]

displacements = np.copy(solution)
for zero_dof in zero_dofs:
    displacements = np.insert(displacements, zero_dof, 0)

result_file_content = {
    "displacements": displacements.tolist()
}

with open("./results/results.json", "w") as results_file:
    json.dump(result_file_content, results_file, indent=2)

print("Solver finished\n")