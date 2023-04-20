import numpy as np

def element_bar_global_k_matrix(node1, node2, material, cross_section):
    E = material["E"]
    A = cross_section["A"]

    vector = np.array([node2[key] - node1[key] for key in "xyz"])
    L = np.linalg.norm(vector)

    cos_a, cos_b, cos_g = vector / L

    return E*A/L*np.array([
        [cos_a**2, cos_a*cos_b, cos_a*cos_g, -cos_a**2, -cos_a*cos_b, -cos_a*cos_g],
        [cos_a*cos_b, cos_b**2, cos_b*cos_g, -cos_a*cos_b, -cos_b**2, -cos_b*cos_g],
        [cos_a*cos_g, cos_b*cos_g, cos_g**2, -cos_a*cos_g, -cos_b*cos_g, -cos_g**2],
        [-cos_a**2, -cos_a*cos_b, -cos_a*cos_g, cos_a**2, cos_a*cos_b, cos_a*cos_g],
        [-cos_a*cos_b, -cos_b**2, -cos_b*cos_g, cos_a*cos_b, cos_b**2, cos_b*cos_g],
        [-cos_a*cos_g, -cos_b*cos_g, -cos_g**2, cos_a*cos_g, cos_b*cos_g, cos_g**2]])
