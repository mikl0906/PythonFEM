import json
from jsonschema import validate
import numpy as np

def validate_schema(geometry):
    print("🧪 Validating geometry file...")

    schema_file_path = "json-schema/geometry.testschema.json"
    schema = json.load(open(schema_file_path))
    try: validate(geometry, schema)
    except Exception as e:
        print(f"❌ Error occured\n{e}")
        exit(1)

    print("✅ Geometry file is valid\n")

def check_point_distances(points):
    print("🧪 Checking point distances...")
    
    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            point_1 = points[f"point-{i}"]
            point_2 = points[f"point-{j}"]
            l = np.sqrt(sum([(point_1[key] - point_2[key])**2 for key in "xyz"]))
            if l < 0.001:
                print(f"❌Points {i} and {j} are too close")
                exit(1)

    print("✅ Point distances are valid\n")

def check_if_lines_have_valid_points(geometry):
    print("🧪 Checking if lines have valid point references...")

    for line in geometry["lines"]:
        for point_id in line["point-ids"]:
            if point_id not in geometry["points"]:
                print(f"❌ Point {point_id} does not exist")
                exit(1)

    print("✅ Line point references are valid\n")

def check_if_lines_refer_to_unique_points(geometry):
    print("🧪 Checking if lines refer to unique points...")

    for line in geometry["lines"]:
        if line["point-ids"][0] == line["point-ids"][1]:
            print(f"❌ Line {line} refers to the same point twice")
            exit(1)

    print("✅ Lines refer to unique points\n")

def check_if_lines_are_unique(geometry):
    print("🧪 Checking if lines are unique...")

    for i in range(len(geometry["lines"])):
        for j in range(i + 1, len(geometry["lines"])):
            line_1 = geometry["lines"][i]
            line_2 = geometry["lines"][j]

            if line_1["point-ids"][0] == line_2["point-ids"][1] and line_1["point-ids"][1] == line_2["point-ids"][0]:
                print(f"❌ Lines {i} and {j} connect the same points")
                exit(1)

    print("✅ Lines are unique\n")

def check_if_lines_overlap(geometry):
    print("🧪 Checking if lines overlap...")

    for i in range(len(geometry["lines"])):
        for j in range(i + 1, len(geometry["lines"])):
            line_1 = geometry["lines"][i]
            line_2 = geometry["lines"][j]

            if line_1["point-ids"][0] == line_2["point-ids"][0] and line_1["point-ids"][1] == line_2["point-ids"][1]:
                print(f"❌ Lines {i} and {j} overlap")
                exit(1)

    print("✅ Lines do not overlap\n")