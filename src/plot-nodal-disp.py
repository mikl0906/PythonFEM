import json
import numpy as np
import matplotlib.pyplot as plt
import sys
import time

print("\n# Plot nodal results started")
start_time = time.time()

try:
    model_path = sys.argv[1]
except:
    print("No model folder name provided")
    exit(1)

scale = 1
try:
    scale = float(sys.argv[2])
    print(f"Provided scale: {scale}")
except:
    print("Default scale of 1 is used")

fig = plt.figure()
ax = fig.add_subplot(projection="3d")

# Load mesh
with open(f"{model_path}/fem_data/mesh.json") as mesh_file:
    mesh = json.load(mesh_file)
nodes = mesh["nodes"]
elements_1d = mesh["elements-1d"]

with open(f"{model_path}/fem_data/results.json") as results_file:
    results = json.load(results_file)

displacements = np.array(results["displacements"])

for element_1D in elements_1d.values():
    node_ids = np.array(element_1D["node-ids"])
    element_nodes = [nodes[str(node_id)] for node_id in node_ids]
    element_pos = (np.array([[element_nodes[0][i], element_nodes[-1][i]] for i in ("x", "y", "z")])).ravel(order="F")

    dof_ids = [dof_ids for node in element_nodes for dof_ids in node["dof-ids"]]

    element_disp = displacements[dof_ids]

    element_new_pos = element_pos + element_disp * scale

    ax.plot(element_new_pos[np.array([0,3])],element_new_pos[np.array([1,4])],element_new_pos[np.array([2,5])])

print(f"# Plot nodal results finished. Time elapsed: {round(time.time() - start_time,8)}")
plt.show()