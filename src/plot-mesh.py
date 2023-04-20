import json
import matplotlib.pyplot as plt
import sys
import time

print("\n# Plot mesh started")
start_time = time.time()

try:
    model_path = sys.argv[1]
except:
    print("No model folder name provided")
    exit(1)

with open(f"{model_path}/fem_data/mesh.json") as mesh_file:
    mesh = json.load(mesh_file)
nodes = mesh["nodes"]
elements_1d = mesh["elements-1d"]

fig = plt.figure()
ax = fig.add_subplot(projection="3d")

for element in elements_1d.values():
    node_ids = element["node-ids"]

    element_nodes = [nodes[str(node_id)] for node_id in node_ids]

    ax.plot([node["x"] for node in element_nodes],[node["y"] for node in element_nodes],[node["z"] for node in element_nodes])

print(f"# Plot mesh finished. Time elapsed: {round(time.time() - start_time,8)}")
plt.show()