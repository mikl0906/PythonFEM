import sys
sys.path.append('./src')
from element_bar import element_bar_global_k_matrix_4

node1 = {
    "x": 1,
    "y": 1,
    "z": 1
}
node2 = {
    "x": 1,
    "y": 1,
    "z": 2
}
material = {
    "E": 1
}
cross_section = {
    "A": 1
}

k = element_bar_global_k_matrix_4(node1, node2, material, cross_section)

print(k)