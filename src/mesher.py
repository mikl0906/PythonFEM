import json
import numpy as np
import time

print("\n# Mesh generation started")
start_time = time.time()

# Read mesh-settings.json
with open("./mesh/mesh-settings.json") as settings_file:
    settings = json.load(settings_file)
N_OF_1D_ELEMENTS = settings["number-of-1D-element-divisions"]
NODE_DISTANCE_TOLERANCE = settings["node-distance-tolerance"]

# Read geometry.json
with open("./input/geometry.json") as geometry_file:
    geometry = json.load(geometry_file)
points = geometry["points"]
lines = geometry["lines"]
surfaces = geometry["surfaces"]
members_1d = geometry["members-1d"]
members_2d = geometry["members-2d"]
members_3d = geometry["members-3d"]


# Read boundary conditions
with open("./input/boundary-conditions.json") as bc_file:
    bc = json.load(bc_file)
# Point displacements
point_displacements = bc["point-displacements"]
# Point forces
point_forces = bc["point-forces"]

# Check node collision
node_collision = lambda n1, n2 : np.sqrt(sum((n1[k]-n2[k])**2 for k in ("x", "y", "z"))) < NODE_DISTANCE_TOLERANCE

# mesh file content
nodes = {}
nodes_index = 1
elements_1d = {}
elements_1d_index = 1
elements_2d = {}
elements_2d_index = 1
elements_3d = {}
elements_3d_index = 1
nodal_displacements = {}
nodal_displacements_index = 1
nodal_forces = {}
nodal_forces_index = 1


# Iterate throw the list of beams in the geometry definition
for member_1d in members_1d.values():
    # Get material, cross section and line definition
    material_id = member_1d["material-id"]
    cross_section_id = member_1d["cross-section-id"]
    fem_type = member_1d["fem-type"]
    member_line = lines[str(member_1d["line-id"])]
    # Get the line definition points
    member_points = [points[str(point_id)] for point_id in member_line["point-ids"]]
    
    # Generate "N_OF_1D_ELEMENTS" + 1 number of node coordinates
    xs = np.linspace(member_points[0]["x"], member_points[1]["x"], N_OF_1D_ELEMENTS + 1)
    ys = np.linspace(member_points[0]["y"], member_points[1]["y"], N_OF_1D_ELEMENTS + 1)
    zs = np.linspace(member_points[0]["z"], member_points[1]["z"], N_OF_1D_ELEMENTS + 1)
    
    # Create nodes and elements. If there is an existing node at the position, use it
    member_node_list = []
    for i in range(len(xs)):
        current_node_position = {
            "x": xs[i],
            "y": ys[i],
            "z": zs[i]
        }
        # Search if there is a node that is near
        near_node_id = next((key for key, node in nodes.items() if node_collision(current_node_position,node)), None)
            
        if near_node_id:
            member_node_list.append(near_node_id)
        else:
            member_node_list.append(nodes_index)
            nodes[str(nodes_index)] = current_node_position
            nodes_index += 1

        if i > 0:
            elements_1d[str(elements_1d_index)] = {
                "node-ids": [member_node_list[i - 1], member_node_list[i]],
                "material-id": material_id,
                "cross-section-id": cross_section_id,
                "fem-type": fem_type
            }
            elements_1d_index += 1

# Create nodal displacements
for disp in point_displacements.values():
    disp_point = points[str(disp["point-id"])]
    disp_node_id = next(key for key, node in nodes.items() if node_collision(disp_point, node))

    nodal_displacements[str(nodal_displacements_index)] = {
        "node-id": disp_node_id,
        "x": disp["x"],
        "y": disp["y"],
        "z": disp["z"],
        "rx": disp["rx"],
        "ry": disp["ry"],
        "rz": disp["rz"]
    }
    nodal_displacements_index += 1

# Create nodal forces
for force in point_forces.values():
    force_point = points[str(force["point-id"])]
    force_node_id = next(key for key, node in nodes.items() if node_collision(force_point, node))

    nodal_forces[str(nodal_forces_index)] = {
        "node-id": force_node_id,
        "fx": force["fx"],
        "fy": force["fy"],
        "fz": force["fz"],
        "mx": force["mx"],
        "my": force["my"],
        "mz": force["mz"]
    }
    nodal_forces_index += 1

# Assemble mesh file content
mesh_file_content = {
    "nodes": nodes,
    "elements-1d": elements_1d,
    "elements-2d": elements_2d,
    "elements-3d": elements_3d,
    "nodal-displacements": nodal_displacements,
    "nodal-forces": nodal_forces
}
# Create/Open mesh file and overwrite the content
with open("./mesh/mesh.json", "w") as mesh_file:
    json.dump(mesh_file_content, mesh_file, indent=2)

print(f"Number of nodes:                 {len(nodes)}\n"+
      f"Number of 1D elements:           {len(elements_1d)}\n"+
      f"Number of 2D elements:           {len(elements_2d)}\n"+
      f"Number of 3D elements:           {len(elements_3d)}\n"+
      f"Number of nodal displacement bc: {len(nodal_displacements)}\n"+
      f"Number of nodal force bc:        {len(nodal_forces)}\n"+
      f"# Mesh generation finished. Time elapsed: {round(time.time() - start_time, 8)}")