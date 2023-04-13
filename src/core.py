import numpy as np
import sys
import matplotlib.pyplot as plt

def element_bar_k_matrix(L, E, A):
    return E*A/L*np.array([[1., -1.],
                           [-1., 1.]])

def element_bar_t_matrix(node1, node2):
    return 1

def element_k_matrix(L, E, G, A, Iy, Iz, k):
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

# Direct solvers
def solve_gaussian(A_matrix,b_vector):
    A = np.array(A_matrix, dtype=float)
    b = np.array(b_vector, dtype=float)
    n = np.size(b)
    x = np.zeros(n)

    # Iterate for each row i
    for i in range(n):
        if A[i,i] == 0.0:
            sys.exit(f"Error while solving. Main diagonal element is zero. DOF: {i}")
        # Iterate for each following row j
        for j in range(i+1, n):
            if A[j,i] == 0:
                continue
            # From every element of the j's row subtract the corresponding 
            # element of the i's row multiplied by the ratio
            ratio = A[j,i] / A[i,i]
            for k in range(n):
                A[j,k] -= ratio*A[i,k]
            b[j] -= ratio*b[i]

    # Solve the equations from the last to the first
    for i in range(n-1,-1,-1):
        x[i] = b[i]
        for j in range(i+1, n):
            x[i] -= A[i,j]*x[j]
        x[i] /= A[i,i]

    return x

def solve_lu(A,b):
    n = np.size(b)
    LU = np.zeros((n, n))
    for i in range(n):
        for j in range(i, n):
            sum = 0
            for k in range(0,i):
                sum += LU[i,k] * LU[k,j]
            LU[i,j] = A[i,j] - sum

        for j in range(i+1,n):
            sum = 0
            for k in range(0,i):
                sum += LU[j,k] * LU[k,i]
            LU[j,i] = (A[j,i] - sum) / LU[i,i]

    y = np.zeros(n)
    for i in range(n):
        sum = 0
        for k in range(i):
            sum += LU[i,k] * y[k]
        y[i] = b[i] - sum

    x = np.zeros(n)
    for i in range(n-1,-1,-1):
        sum = 0
        for k in range(i+1,n):
            sum += LU[i,k] * x[k]
        x[i] = (y[i] - sum) / LU[i,i]

    return x

# Iterative solvers
def solve_jacobi(A,b):
    n = np.size(b)
    x = np.zeros(n)
    D = np.diag(A)
    LU = A - np.eye(n)*D
    for _ in range(100):
        x_old = x
        x = (b - np.matmul(LU, x))/ D
        if np.dot(x-x_old,x-x_old) < 0.00001:
            return x
    return None