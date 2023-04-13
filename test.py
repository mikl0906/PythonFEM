import sys
sys.path.append("./src")

import time
import numpy as np
import os
import json
from pathlib import Path
from core import solve_jacobi
from core import solve_gaussian
from core import solve_lu


# A = np.array([[1, 1, 1], [2, -3, 4], [3, 4, 5]])
# b = np.array([9, 13, 40])
with open("./fem_data/matrices.json") as matrices_file:
    matrices = json.load(matrices_file)

A = np.array(matrices["stiffness-matrix"])
b = np.array(matrices["force-vector"])

print("Solve gaussian")
start_time = time.time()
# for _ in range(1000):
x = solve_gaussian(A,b)
print(x)
print(f"Time elapsed: {time.time() - start_time}")

print("Solve LU")
start_time = time.time()
# for _ in range(1000):
x = solve_lu(A,b)
print(x)
print(f"Time elapsed: {time.time() - start_time}")

print("Solve jacobi")
start_time = time.time()
# for _ in range(1000):
x = solve_jacobi(A,b)
print(x)
print(f"Time elapsed: {time.time() - start_time}")



# w = np.linalg.eigvals(A)
# print(w)
# ro = np.max(np.abs(w))
# print(ro)

# x = solve_gaussian(A, b)
# print(x)

# points_dict = {}
# points_list = []

# for i in range(10000):
#     points_dict[str(i)] = {"x": 1, "y": 1, "z": 1}
#     points_list.append({"id": i, "x": 1, "y": 1, "z": 1})

# line_points = np.random.randint(10000, size=5000)

# print("Dictionary")
# start_time = time.time()
# points = [points_dict[str(point_id)] for point_id in line_points]
# print(f"Number of points: {len(points)}")
# print(f"Time elapsed: {round(time.time() - start_time,8)}")
# print("List")
# start_time = time.time()
# points = [point for point in points_list if point["id"] in line_points]
# print(f"Number of points: {len(points)}")
# print(f"Time elapsed: {round(time.time() - start_time,8)}")
