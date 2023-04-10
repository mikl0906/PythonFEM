import json
import matplotlib.pyplot as plt

with open("./mesh/mesh.json") as mesh_file:
    mesh = json.load(mesh_file)

nodes = mesh["nodes"]
elements_1d = mesh["elements-1d"]

fig = plt.figure()
ax = fig.add_subplot(projection="3d")

for element in elements_1d.values():
    node_ids = element["node-ids"]

    element_nodes = [nodes[str(node_id)] for node_id in node_ids]

    ax.plot([node["x"] for node in element_nodes],[node["y"] for node in element_nodes],[node["z"] for node in element_nodes])

plt.show()