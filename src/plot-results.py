import json
import numpy as np
import matplotlib.pyplot as plt

fig = plt.figure()
ax = fig.add_subplot(projection="3d")

with open("./mesh/mesh.json") as mesh_file:
    mesh = json.load(mesh_file)

nodes = mesh["nodes"]
elements_1D = mesh["elements-1D"]

with open("./results/results.json") as results_file:
    results = json.load(results_file)

displacements = np.array(results["displacements"])

with open("./input/materials.json") as materials_file:
    materials = json.load(materials_file)["definitions"]

with open("./input/cross-sections.json") as cross_sections_file:
    cross_sections = json.load(cross_sections_file)["linear-profiles"]


xis = np.linspace(0, 1, 10)
N_1 = lambda xi: 1 - xi
N_2 = lambda xi: xi
H_v1 = lambda xi, ay, by: by*(2*xi**3 - 3*xi**2 + ay*xi + 1 - ay)
H_v2 = lambda xi, ay, by: by*(-2*xi**3 + 3*xi**2 - ay*xi)
H_w1 = lambda xi, az, bz: bz*(2*xi**3 - 3*xi**2 + az*xi + 1 - az)
H_w2 = lambda xi, az, bz: bz*(-2*xi**3 + 3*xi**2 - az*xi)
H_t1 = lambda xi, ay, by, L: L*by*(xi**3 + (0.5*ay - 2)*xi**2 + (1 - 0.5*ay)*xi)
H_t2 = lambda xi, ay, by, L: L*by*(xi**3 - (1 + 0.5*ay)*xi**2 + 0.5*ay*xi)
H_p1 = lambda xi, az, bz, L: L*bz*(xi**3 + (0.5*az - 2)*xi**2 + (1 - 0.5*az)*xi)
H_p2 = lambda xi, az, bz, L: L*bz*(xi**3 - (1 + 0.5*az)*xi**2 + 0.5*az*xi)
G_v1 = lambda xi, by, L: 6*by/L*(xi**2 - xi)
G_v2 = lambda xi, by, L: 6*by/L*(-xi**2 + xi)
G_w1 = lambda xi, bz, L: 6*bz/L*(xi**2 - xi)
G_w2 = lambda xi, bz, L: 6*bz/L*(-xi**2 + xi)
G_t1 = lambda xi, ay, by: by*(3*xi**2 + (ay - 4)*xi + 1 - ay)
G_t2 = lambda xi, ay, by: by*(3*xi**2 - (ay + 2)*xi)
G_p1 = lambda xi, az, bz: bz*(3*xi**2 + (az - 4)*xi + 1 - az)
G_p2 = lambda xi, az, bz: bz*(3*xi**2 - (az + 2)*xi)


for element_1D in elements_1D:
    node_ids = np.array(element_1D["node-ids"])
    element_nodes = [node for node in nodes if node["id"] in node_ids]
    node1_pos = [element_nodes[0][i] for i in ("x", "y", "z")]
    node2_pos = [element_nodes[-1][i] for i in ("x", "y", "z")]
    L = np.sqrt(sum((element_nodes[0][i] - element_nodes[-1][i])**2 for i in ("x", "y", "z")))

    dofs = np.concatenate([np.arange(6) + 6 * (node_ids[0] - 1),np.arange(6) + 6 * (node_ids[1] - 1)])

    material = next(material for material in materials if material["id"] == element_1D["material-id"])
    E = material["E"]
    G = material["G"]

    cross_section = next(cs for cs in cross_sections if cs["id"] == element_1D["cross-section-id"])
    A = cross_section["A"]
    Iy = cross_section["Iy"]
    Iz = cross_section["Iz"]
    k = cross_section["k"]

    ay = 12*E*Iy/(k*G*A*L**2)
    by = 1/(1-ay)
    az = 12*E*Iz/(k*G*A*L**2)
    bz = 1/(1-az)

    el_disp = displacements[dofs]
    el_disp[0:3] += node1_pos
    el_disp[6:9] += node2_pos

    xs = []
    ys = []
    zs = []

    for xi in xis:
        u =     N_1(xi)*el_disp[0] + N_2(xi)*el_disp[6]
        v =     H_v1(xi, ay, by)*el_disp[1] + H_t1(xi, ay, by, L)*el_disp[5] + H_v2(xi, ay, by)*el_disp[7] + H_t2(xi, ay, by, L)*el_disp[11]
        w =     H_w1(xi, az, bz)*el_disp[2] + H_p1(xi, az, bz, L)*el_disp[4] + H_w2(xi, az, bz)*el_disp[8] + H_p2(xi, az, bz, L)*el_disp[10]
        phi =   N_1(xi)*el_disp[3] + N_2(xi)*el_disp[9]
        theta = G_v1(xi, ay, by)*el_disp[1] +    G_t1(xi, ay, by)*el_disp[5] + G_v2(xi, ay, by)*el_disp[7] +    G_t2(xi, ay, by)*el_disp[11]
        psi =   G_w1(xi, az, bz)*el_disp[2] +    G_p1(xi, az, bz)*el_disp[4] + G_w2(xi, az, bz)*el_disp[8] +    G_p2(xi, az, bz)*el_disp[10]

        xs.append(u)
        ys.append(v)
        zs.append(w)
    
    ax.plot(xs,ys,zs)

plt.show()