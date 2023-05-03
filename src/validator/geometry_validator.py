import json
from jsonschema import validate
import sys
import os
import validator.geometry_validator_functions as gvf

if len(sys.argv) < 2:
    print("No geometry file provided")
    exit(1)

geometry_file_path = sys.argv[1]

if not os.path.isfile(geometry_file_path):
    print("Geometry file does not exist")
    exit(1)

with open(geometry_file_path) as geometry_file:
    geometry = json.load(geometry_file)

    gvf.validate_schema(geometry)
    gvf.check_point_distances(geometry["points"])
    gvf.check_if_lines_have_valid_points(geometry)
    gvf.check_if_lines_refer_to_unique_points(geometry)
    gvf.check_if_lines_are_unique(geometry)
    gvf.check_if_lines_overlap(geometry)