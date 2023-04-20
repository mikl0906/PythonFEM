import json
import time
import numpy as np
from element_bar import element_bar_global_k_matrix
from element_beam import element_beam_local_k_matrix
import sys

print("\n# Matrix assembler started")
start_time = time.time()

try:
    model_path = sys.argv[1]
except:
    print("No model folder name provided")
    exit(1)

# Import mesh
with open(f"{model_path}/fem_data/mesh.json") as matrices_file:
    mesh = json.load(matrices_file)
number_of_dofs = mesh["number-of-dofs"]
number_of_nodes = mesh["number-of-nodes"]
number_of_elements_1d = mesh["number-of-elements-1d"]
nodes = mesh["nodes"]
elements_1d = mesh["elements-1d"]
nodal_displacements = mesh["nodal-displacements"]
nodal_forces = mesh["nodal-forces"]

# Import materials
with open("./library/materials.json") as materials_file:
    materials = json.load(materials_file)["materials"]

# Import cross sections
with open("./library/cross-sections.json") as cross_sections_file:
    cross_sections = json.load(cross_sections_file)["linear-profiles"]

# Initialize empty stiffness matrix and force vector
stiffness_matrix = np.zeros((number_of_dofs, number_of_dofs))
force_vector = np.zeros(number_of_dofs)

for element_1d in elements_1d.values():
    material = materials[element_1d["material-id"]]
    cross_section = cross_sections[element_1d["cross-section-id"]]

    element_nodes = [nodes[node_id] for node_id in element_1d["node-ids"]]
    dof_ids = [dof_ids for node in element_nodes for dof_ids in node["dof-ids"]]

    element_type = element_1d["element-type"]
    element_matrix = None
    dof_ids_grid = np.tile(dof_ids, (len(dof_ids), 1))

    if element_type == "bar":
        element_matrix = element_bar_global_k_matrix(element_nodes[0], element_nodes[-1], material, cross_section)

    if element_type == "beam":
        element_matrix = element_beam_local_k_matrix(element_nodes[0], element_nodes[-1], material, cross_section)

    if element_matrix is not None and dof_ids_grid is not None:
        stiffness_matrix[dof_ids_grid.T, dof_ids_grid] += np.round(element_matrix,5)

force_dofs = {
    "ux": "fx",
    "uy": "fy",
    "uz": "fz",
    "rx": "mx",
    "ry": "my",
    "rz": "mz"
}
# Force boundary conditions
for nodal_force in nodal_forces.values():
    node = nodes[nodal_force["node-id"]]
    dof_names = node["dof-names"]
    dof_ids = node["dof-ids"]
    dof_values = nodal_force["dof-values"]

    for i, dof in enumerate(dof_names):
        force_dof = force_dofs[dof]
        if dof_values.get(force_dof) is None:
            continue
        force_vector[dof_ids[i]] += dof_values[force_dof]

# Displacement boundary conditions
zero_dofs = []
for nodal_disp in nodal_displacements.values():
    node = nodes[nodal_disp["node-id"]]
    dof_names = node["dof-names"]
    dof_ids = node["dof-ids"]
    dof_values = nodal_disp["dof-values"]

    applied_dofs = []
    applied_values = []
    for i, dof in enumerate(dof_names):
        if dof_values.get(dof) is None:
            continue
        
        applied_dofs.append(dof_ids[i])
        applied_values.append(dof_values[dof])

    zero_node_dofs = [applied_dofs[i] for i, value in enumerate(applied_values) if value == 0]
    zero_dofs += zero_node_dofs

# Delete zero equations
# zero_row_ids = []
# for i, row in enumerate(stiffness_matrix):
#     if np.dot(row, row) < 0.001:
#         zero_dofs.append(i)

# zero_dofs = list(map(int, set(zero_dofs)))
# Delete zero dofs
# stiffness_matrix = np.delete(np.delete(stiffness_matrix, zero_dofs, axis=0), zero_dofs, axis=1)
# force_vector = np.delete(force_vector, zero_dofs)

# Create/Open mesh file and overwrite the content
matrices_file_content = {
    "stiffness-matrix": stiffness_matrix.tolist(),
    "force-vector": force_vector.tolist(),
    "zero-dofs": zero_dofs
}
with open(f"{model_path}/fem_data/matrices.json", "w") as matrices_file:
    json.dump(matrices_file_content, matrices_file, indent=2)

print(f"Number of dofs: {number_of_dofs}\n" +
      f"Size of the system: {len(force_vector)}\n" +
      f"Number of zero dofs: {len(zero_dofs)}\n" + 
      f"# Matrix assembler finished. Time elapsed: {round(time.time() - start_time, 8)}")