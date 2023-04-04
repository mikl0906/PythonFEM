import json

with open("./mesh/mesh.json") as mesh_file:
    mesh = json.load(mesh_file)

with open("./results/results.json") as results_file:
    results = json.load(results_file)

