import json
import matplotlib.pyplot as plt

with open("./mesh/mesh.json") as mesh_file:
    mesh = json.load(mesh_file)


fig = plt.figure()
ax = fig.add_subplot(projection="3d")

for element in mesh["elements-1D"]:
    node_ids = element["node-ids"]

    nodes = [node for node in mesh["nodes"] if node["id"] in node_ids]

    ax.plot([node["x"] for node in nodes],[node["y"] for node in nodes],[node["z"] for node in nodes])

plt.show()