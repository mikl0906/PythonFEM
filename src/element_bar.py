import numpy as np

def element_bar_global_k_matrix(node1, node2, material, cross_section):
    E = material["E"]
    A = cross_section["A"]

    [x1, y1, z1] = [node1[key] for key in ("x", "y", "z")]
    [x2, y2, z2] = [node2[key] for key in ("x", "y", "z")]

    dx = x2 - x1
    dy = y2 - y1
    dz = z2 - z1

    L = np.sqrt(dx**2 + dy**2 + dz**2)

    if L == 0:
        return None

    # Tait-Bryan angles alpha - yaw, beta - pitch, gamma - roll
    alpha = np.arctan2(dy, dx)
    beta = np.arctan2(dz, np.sqrt(dx**2 + dy**2))
    gamma = 0

    sin_a, sin_b, sin_g = np.sin([alpha, beta, gamma])
    cos_a, cos_b, cos_g = np.cos([alpha, beta, gamma])
    # Rotation matrix
    R = np.array([[cos_a*cos_b, cos_a*sin_b*sin_g - sin_a*cos_g, cos_a*sin_b*cos_g + sin_a*sin_g],
                  [sin_a*cos_b, sin_a*sin_b*sin_g + cos_a*cos_g, sin_a*sin_b*cos_g - cos_a*sin_g],
                  [-sin_b     , cos_b*sin_g                    , cos_b*cos_g]])
    
    # Element rotation matrix
    T = np.vstack((np.hstack((R, np.zeros_like(R))), np.hstack((np.zeros_like(R), R))))

    # Stiffness matrix in local coordinate system (x aligned with bar)
    k_lcs = E*A/L*np.array([[ 1., 0., 0., -1., 0., 0.],
                            [ 0., 0., 0.,  0., 0., 0.],
                            [ 0., 0., 0.,  0., 0., 0.],
                            [-1., 0., 0.,  1., 0., 0.],
                            [ 0., 0., 0.,  0., 0., 0.],
                            [ 0., 0., 0.,  0., 0., 0.]])
    
    # Stiffness matrix in global coordinate system
    k_gcs = np.matmul(T.T, np.matmul(k_lcs, T))

    return k_gcs

def element_bar_global_k_matrix_2(node1, node2, material, cross_section):
    E = material["E"]
    A = cross_section["A"]
    
    [x1, y1, z1] = [node1[key] for key in ("x", "y", "z")]
    [x2, y2, z2] = [node2[key] for key in ("x", "y", "z")]

    dx = x2 - x1
    dy = y2 - y1
    dz = z2 - z1

    L = np.sqrt(dx**2 + dy**2 + dz**2)

    if L == 0:
        return None

    # Tait-Bryan angles alpha - yaw, beta - pitch, gamma - roll
    alpha = np.arctan2(dy, dx)
    beta = np.arctan2(dz, np.sqrt(dx**2 + dy**2))
    gamma = 0

    sin_a, sin_b, sin_g = np.sin([alpha, beta, gamma])
    cos_a, cos_b, cos_g = np.cos([alpha, beta, gamma])

    sig4 = cos_g*sin_a - cos_a*sin_b*sin_g
    sig5 = sin_a*sin_g + cos_a*cos_g*sin_b
    sig1 = cos_a**2*cos_b**2
    sig2 = cos_a*cos_b*sig4
    sig3 = cos_a*cos_b*sig5

    quarter = E*A/L*np.array([[ sig1,      -sig2,       sig3],
                              [-sig2,    sig4**2, -sig4*sig5],
                              [ sig3, -sig4*sig5,    sig5**2]])

    return np.vstack((np.hstack((quarter, -quarter)), np.hstack((-quarter, quarter))))

def element_bar_global_k_matrix_3(node1, node2, material, cross_section):
    E = material["E"]
    A = cross_section["A"]

    [x1, y1, z1] = [node1[key] for key in ("x", "y", "z")]
    [x2, y2, z2] = [node2[key] for key in ("x", "y", "z")]

    dx = x2 - x1
    dy = y2 - y1
    dz = z2 - z1

    L = np.sqrt(dx**2 + dy**2 + dz**2)

    if L == 0:
        return None

    # Tait-Bryan angles alpha - yaw, beta - pitch, gamma - roll
    alpha = np.arctan2(dy, dx)
    beta = np.arctan2(dz, np.sqrt(dx**2 + dy**2))
    gamma = 0

    sin_a, sin_b, sin_g = np.sin([alpha, beta, gamma])
    cos_a, cos_b, cos_g = np.cos([alpha, beta, gamma])

    sig4 = cos_g*sin_a - cos_a*sin_b*sin_g
    sig5 = sin_a*sin_g + cos_a*cos_g*sin_b
    sig1 = cos_a**2*cos_b**2
    sig2 = cos_a*cos_b*sig4
    sig3 = cos_a*cos_b*sig5

    return E*A/L*np.array([[ sig1,      -sig2,       sig3, -sig1,       sig2,      -sig3],
                           [-sig2,    sig4**2, -sig4*sig5,  sig2,   -sig4**2,  sig4*sig5],
                           [ sig3, -sig4*sig5,    sig5**2, -sig3,  sig4*sig5,   -sig5**2],
                           [-sig1,       sig2,      -sig3,  sig1,      -sig2,       sig3],
                           [ sig2,   -sig4**2,  sig4*sig5, -sig2,    sig4**2, -sig4*sig5],
                           [-sig3,  sig4*sig5,   -sig5**2,  sig3, -sig4*sig5,    sig5**2]])

def element_bar_local_k_matrix(L, E, A):
    return E*A/L*np.array([[1., -1.],
                           [-1., 1.]])

def element_bar_t_matrix(node1, node2):
    [x1, y1, z1] = [node1[key] for key in ("x", "y", "z")]
    [x2, y2, z2] = [node2[key] for key in ("x", "y", "z")]

    dx = x2 - x1
    dy = y2 - y1
    dz = z2 - z1

    L = np.sqrt(dx**2 + dy**2 + dz**2)

    # Tait-Bryan angles alpha - yaw, beta - pitch, gamma - roll
    alpha = np.arctan2(dy, dx)
    beta = np.arctan2(dz, np.sqrt(dx**2 + dy**2))
    gamma = 0

    sin_a, sin_b, sin_g = np.sin([alpha, beta, gamma])
    cos_a, cos_b, cos_g = np.cos([alpha, beta, gamma])
    # Rotation matrix
    R = np.array([[cos_a*cos_b, cos_a*sin_b*sin_g - sin_a*cos_g, cos_a*sin_b*cos_g + sin_a*sin_g],
                  [sin_a*cos_b, sin_a*sin_b*sin_g + cos_a*cos_g, sin_a*sin_b*cos_g - cos_a*sin_g],
                  [-sin_b     , cos_b*sin_g                    , cos_b*cos_g]])

    return np.vstack((np.hstack((R, np.zeros_like(R))), np.hstack((np.zeros_like(R), R))))