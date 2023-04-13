import numpy as np

def element_bar_local_k_matrix(L, E, A):
    return E*A/L*np.array([[1., -1.],
                           [-1., 1.]])

def element_bar_t_matrix(node1, node2):
    x1 = node1["x"]
    y1 = node1["y"]
    x2 = node2["x"]
    y2 = node2["y"]

    dx = x2 - x1
    dy = y2 - y1

    theta = 0

    if dx > 0 and dy == 0:
        theta = 0
    if dx < 0 and dy == 0:
        theta = np.pi
    if dx == 0 and dy == 0:
        theta = 0
    if dx == 0 and dy == 0:
        theta = 0
    

    return 1