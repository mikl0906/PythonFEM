import numpy as np
import sys
import matplotlib.pyplot as plt

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