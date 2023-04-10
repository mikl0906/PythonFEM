import json
from core import element_bar_k_matrix, element_k_matrix
import numpy as np

print("Matrix assembler started\n")

# Import mesh
with open("./mesh/mesh.json") as matrices_file:
    mesh = json.load(matrices_file)

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

number_of_nodes = len(nodes)
number_of_dofs = number_of_nodes * 6
number_of_elements_1d = len(elements_1d)

stiffness_matrix = np.zeros((number_of_dofs, number_of_dofs))
force_vector = np.zeros(number_of_dofs)
zero_dofs = []

for element_1d in elements_1d.values():
    material = materials[str(element_1d["material-id"])]
    cross_section = cross_sections[str(element_1d["cross-section-id"])]
    node_ids = np.array(element_1d["node-ids"])
    element_nodes = [nodes[str(node_id)] for node_id in node_ids]
    L = np.sqrt(sum((element_nodes[0][i] - element_nodes[-1][i])**2 for i in ("x", "y", "z")))

    fem_type = element_1d["fem-type"]
    element_matrix = None
    dofs = None

    if fem_type == "bar":
        E = material["E"]
        A = cross_section["A"]

        P = np.array([[1,0,0,0,0,0],[0,0,0,1,0,0]])
        element_matrix = np.matmul(P.T,np.matmul(element_bar_k_matrix(L, E, A),P))
        dofs = np.tile((np.tile(np.arange(3), (2, 1)).T + 3 * (node_ids - 1)).ravel(order="F"), (6,1))

    if fem_type == "beam":
        E = material["E"]
        G = material["G"]
        A = cross_section["A"]
        Iy = cross_section["Iy"]
        Iz = cross_section["Iz"]
        k = cross_section["k"]

        element_matrix = element_k_matrix(L, E, G, A, Iy, Iz, k)
        dofs = np.tile(np.tile(np.arange(6), (2, 1)).T + 6 * (node_ids - 1).ravel(order="F"), (12,1))

    if element_matrix is not None and dofs is not None:
        stiffness_matrix[dofs.T, dofs] += element_matrix

for nodal_force in nodal_forces.values():
    dofs = np.arange(6) + 6 * (int(nodal_force["node-id"]) - 1)
    force_vector[dofs] += [nodal_force[key] for key in ("fx", "fy", "fz", "mx", "my", "mz")]

for nodal_dips in nodal_displacements.values():
    dofs = np.arange(6) + 6 * (int(nodal_dips["node-id"]) - 1)
    values = [nodal_dips[key] for key in ("x", "y", "z", "rx", "ry", "rz")]

    zero_node_dofs = [dof for i, dof in enumerate(dofs) if values[i] == 0]
    zero_dofs += zero_node_dofs
    stiffness_matrix = np.delete(np.delete(stiffness_matrix, zero_node_dofs, axis=0), zero_node_dofs, axis=1)
    force_vector = np.delete(force_vector, zero_node_dofs)

zero_row_ids = []
for i, row in enumerate(stiffness_matrix):
    if np.dot(row, row) < 0.001:
        zero_row_ids.append(i)
stiffness_matrix = np.delete(np.delete(stiffness_matrix, zero_row_ids, axis=0), zero_row_ids, axis=1)
force_vector = np.delete(force_vector, zero_row_ids)

matrices_file_content = {
    "stiffness-matrix": stiffness_matrix.tolist(),
    "force-vector": force_vector.tolist(),
    "zero-dofs": list(map(int, zero_dofs))
}
# Create/Open mesh file and overwrite the content
with open("./fem_data/matrices.json", "w") as matrices_file:
    json.dump(matrices_file_content, matrices_file, indent=2)

print(f"Number of dofs: {number_of_dofs}")
print("Matrix assembler finished\n")