import json
from core import element_k_matrix
import numpy as np

with open("./mesh/mesh.json") as matrices_file:
    mesh = json.load(matrices_file)

nodes = mesh["nodes"]
elements_1D = mesh["elements-1D"]
nodal_displacements = mesh["nodal-displacements"]
nodal_forces = mesh["nodal-forces"]

with open("./input/materials.json") as materials_file:
    materials = json.load(materials_file)["definitions"]

with open("./input/cross-sections.json") as cross_sections_file:
    cross_sections = json.load(cross_sections_file)["linear-profiles"]

number_of_nodes = len(nodes)
number_of_dof = number_of_nodes * 6
number_of_elements_1D = len(elements_1D)

stiffness_matrix = np.zeros((number_of_dof, number_of_dof))
force_vector = np.zeros(number_of_dof)
zero_dofs = []

for element in elements_1D:
    node_ids = np.array(element["node-ids"])
    element_nodes = [node for node in nodes if node["id"] in node_ids]
    L = np.sqrt(sum((element_nodes[0][i] - element_nodes[-1][i])**2 for i in ("x", "y", "z")))
    
    dofs = np.tile(np.arange(6), (2, 1)).T + 6 * (node_ids - 1)
    dofs = np.tile(dofs.ravel(order="F"), (12, 1))

    material = next(material for material in materials if material["id"] == element["material-id"])
    E = material["E"]
    G = material["G"]

    cross_section = next(cs for cs in cross_sections if cs["id"] == element["cross-section-id"])
    A = cross_section["A"]
    Iy = cross_section["Iy"]
    Iz = cross_section["Iz"]
    J = cross_section["J"]
    k = cross_section["k"]

    element_k_matrix_lcs = element_k_matrix(L, E, G, A, Iy, Iz, k)

    stiffness_matrix[dofs.T, dofs] += element_k_matrix_lcs

for nodal_force in nodal_forces:
    dofs = np.arange(6) + 6 * (nodal_force["node-id"] - 1)
    force_vector[dofs] += [nodal_force[key] for key in ("fx", "fy", "fz", "mx", "my", "mz")]

for nodal_dips in nodal_displacements:
    dofs = np.arange(6) + 6 * (nodal_dips["node-id"] - 1)
    values = [nodal_dips[key] for key in ("x", "y", "z", "rx", "ry", "rz")]

    zero_node_dofs = [dof for i, dof in enumerate(dofs) if values[i] == 0]
    zero_dofs += zero_node_dofs
    stiffness_matrix = np.delete(np.delete(stiffness_matrix, zero_node_dofs, axis=0), zero_node_dofs, axis=1)
    force_vector = np.delete(force_vector, zero_node_dofs)


matrices_file_content = {
    "stiffness-matrix": stiffness_matrix.tolist(),
    "force-vector": force_vector.tolist(),
    "zero-dofs": list(map(int, zero_dofs))
}
# Create/Open mesh file and overwrite the content
with open("./fem_data/matrices.json", "w") as matrices_file:
    json.dump(matrices_file_content, matrices_file, indent=2)