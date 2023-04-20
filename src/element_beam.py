import numpy as np

def element_beam_local_k_matrix(node1, node2, material, cross_section):
    E = material["E"]
    G = material["G"]
    A = cross_section["A"]
    Iy = cross_section["Iy"]
    Iz = cross_section["Iz"]
    k = cross_section["k"]

    L = np.sqrt(sum((node1[i] - node2[i])**2 for i in ("x", "y", "z")))

    if L == 0:
        return None
    
    EIy = E*Iy
    EIz = E*Iz
    kGA = k*G*A

    k_1_1   =  E*A/L
    k_1_7   = -k_1_1
    k_2_2   =  12*kGA*EIy*(12*EIy + kGA*L**2) / (L*(12*EIy - kGA*L**2)**2)
    k_2_6   =   6*kGA*EIy*(12*EIy + kGA*L**2) /    (12*EIy - kGA*L**2)**2
    k_2_8   = -k_2_2
    k_2_12  =  k_2_6
    k_3_3   =  12*kGA*EIz*(12*EIz + kGA*L**2) / (L*(12*EIz - kGA*L**2)**2)
    k_3_5   =  -6*kGA*EIz*(12*EIz + kGA*L**2) /    (12*EIz - kGA*L**2)**2
    k_3_9   =  k_3_3
    k_3_11  =  k_3_5
    k_4_4   =  G*(Iy + Iz)/L
    k_4_10  = -k_4_4
    k_5_5   =  4*EIz*(kGA**2*L**4 + 3*kGA*L**2*EIz + 36*EIz**2) / (L*(12*EIz - kGA*L**2)**2)
    k_5_9   =  -k_3_5
    k_5_11  = -2*EIz*(72*(EIz)**2 - (kGA)**2*L**4 - 30*kGA*L**2*EIz) / (L*(12*EIz - kGA*L**2))
    k_6_6   =  4*EIy*(kGA**2*L**4 + 3*kGA*L**2*EIy + 36*EIy**2) / (L*(12*EIy - kGA*L**2)**2)
    k_6_8   = -k_2_6
    k_6_12  = -2*EIy*(-kGA**2*L**4 - 30*kGA*L**2*EIy + 72*EIy**2) / (L*(12*EIy - kGA*L**2)**2)
    k_7_7   = k_1_1
    k_8_8   = k_2_2
    k_8_12  = -k_2_6
    k_9_9   = k_3_3
    k_9_11  = -k_3_5
    k_10_10 = k_4_4
    k_11_11 = k_5_5
    k_12_12 = k_6_6

    return np.array([
        [  k_1_1,      0,      0,      0,      0,      0,   k_1_7,      0,      0,      0,      0,      0],
        [      0,  k_2_2,      0,      0,      0,  k_2_6,       0,  k_2_8,      0,      0,      0, k_2_12],
        [      0,      0,  k_3_3,      0,  k_3_5,      0,       0,      0,  k_3_9,      0, k_3_11,      0],
        [      0,      0,      0,  k_4_4,      0,      0,       0,      0,      0, k_4_10,      0,      0],
        [      0,      0,  k_3_5,      0,  k_5_5,      0,       0,      0,  k_5_9,      0, k_5_11,      0],
        [      0,  k_2_6,      0,      0,      0,  k_6_6,       0,  k_6_8,      0,      0,      0, k_6_12],
        [  k_1_7,      0,      0,      0,      0,      0,   k_7_7,      0,      0,      0,      0,      0],
        [      0,  k_2_8,      0,      0,      0,  k_6_8,       0,  k_8_8,      0,      0,      0, k_8_12],
        [      0,      0,  k_3_9,      0,  k_5_9,      0,       0,      0,  k_9_9,      0, k_9_11,      0],
        [      0,      0,      0, k_4_10,      0,      0,       0,      0,      0,k_10_10,      0,      0],
        [      0,      0, k_3_11,      0, k_5_11,      0,       0,      0, k_9_11,      0,k_11_11,      0],
        [      0, k_2_12,      0,      0,      0, k_6_12,       0, k_8_12,      0,      0,      0,k_12_12]
    ])