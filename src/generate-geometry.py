import numpy as np
import json


N_OF_POINTS = 10
X_LENGTH = 1000
Y_LENGTH = 1000
Z_LENGTH = 1000
points = {}
point_index = 0
for point in np.random.rand(N_OF_POINTS, 3):
    points[f"point-{point_index}"] = {
        "x": point[0] * X_LENGTH,
        "y": point[1] * Y_LENGTH,
        "z": point[2] * Z_LENGTH
    }
    point_index += 1

N_OF_LINES = 10
lines = {}
line_index = 0
for line in np.random.randint(0, N_OF_POINTS, size=(N_OF_LINES, 2)):
    lines[f"line-{line_index}"] = {
        "point-ids": [f"point-{line[0]}", f"point-{line[1]}"]
    }
    line_index += 1


file_content = {
    "units": "mm",
    "points": points,
    "lines": lines
}

with open("test-geometry.json", "w") as f:
    json.dump(file_content, f, indent=2)