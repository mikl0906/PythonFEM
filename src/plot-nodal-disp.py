import json
import numpy as np
import matplotlib.pyplot as plt

fig = plt.figure()
ax = fig.add_subplot(projection="3d")

with open("./mesh/mesh.json") as mesh_file:
    mesh = json.load(mesh_file)

nodes = mesh["nodes"]
elements_1d = mesh["elements-1d"]

with open("./results/results.json") as results_file:
    results = json.load(results_file)

displacements = np.array(results["displacements"])

for element_1D in elements_1d.values():
    node_ids = np.array(element_1D["node-ids"])
    element_nodes = [nodes[str(node_id)] for node_id in node_ids]
    element_pos = (np.array([[element_nodes[0][i], element_nodes[-1][i]] for i in ("x", "y", "z")])).ravel(order="F")

    dofs = np.concatenate([np.arange(3) + 6 * (node_ids[0] - 1),np.arange(3) + 6 * (node_ids[1] - 1)])

    element_disp = displacements[dofs]

    element_new_pos = element_pos + element_disp

    ax.plot(element_new_pos[np.array([0,3])],element_new_pos[np.array([1,4])],element_new_pos[np.array([2,5])])

plt.show()

