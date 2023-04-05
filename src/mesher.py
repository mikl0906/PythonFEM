import json
import numpy as np
import time

start_time = time.time()
print("\nMesh generation started")

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
beams = geometry["beams"]


# Read boundary conditions
with open("./input/boundary-conditions.json") as bc_file:
    bc = json.load(bc_file)
# Point displacements
point_displacements = bc["point-displacements"]
# nodal_displacements_point_ids = [disp["point-id"] for disp in point_displacements]
# Point forces
point_forces = bc["point-forces"]
# nodal_forces_point_ids = [force["point-id"] for force in point_forces]

# Check node collision
node_collision = lambda n1, n2 : np.sqrt(sum((n1[k]-n2[k])**2 for k in ("x", "y", "z"))) < NODE_DISTANCE_TOLERANCE

# mesh file content
nodes = []
nodes_index = 1
elements_1D = []
elements_1D_index = 1
nodal_displacements = []
nodal_displacements_index = 1
nodal_forces = []
nodal_forces_index = 1


# Iterate throw the list of beams in the geometry definition
for beam in beams:
    # Get material, cross section and line definition
    material_id = beam["material-id"]
    cross_section_id = beam["cross-section-id"]
    beam_line = next(line for line in lines if line["id"] == beam["line-id"])
    # Get the line definition points
    beam_points = [point for point in points if point["id"] in beam_line["point-ids"]]
    
    # Generate "N_OF_1D_ELEMENTS" + 1 number of node coordinates
    xs = np.linspace(beam_points[0]["x"], beam_points[1]["x"], N_OF_1D_ELEMENTS + 1)
    ys = np.linspace(beam_points[0]["y"], beam_points[1]["y"], N_OF_1D_ELEMENTS + 1)
    zs = np.linspace(beam_points[0]["z"], beam_points[1]["z"], N_OF_1D_ELEMENTS + 1)
    
    # Create nodes and elements. If there is an existing node at the position, use it
    local_node_ids = []
    for i in range(len(xs)):
        current_node_position = {
            "x": xs[i],
            "y": ys[i],
            "z": zs[i]
        }
        # Search if there is a node that is near
        near_node_id = next((node["id"] for node in nodes if node_collision(current_node_position,node)), None)
            
        if near_node_id:
            local_node_ids.append(near_node_id)
        else:
            local_node_ids.append(nodes_index)
            nodes.append({"id": nodes_index, **current_node_position})
            nodes_index += 1

        if i > 0:
            elements_1D.append({
                "id": elements_1D_index,
                "node-ids": [local_node_ids[i - 1], local_node_ids[i]],
                "material-id": material_id,
                "cross-section-id": cross_section_id
            })
            elements_1D_index += 1

# Create nodal displacements
for disp in point_displacements:
    disp_point = next(point for point in points if point["id"] == disp["point-id"])
    disp_node_id = next(node["id"] for node in nodes if node_collision(disp_point, node))

    nodal_displacements.append({
        "id": nodal_displacements_index,
        "node-id": disp_node_id,
        "x": disp["x"],
        "y": disp["y"],
        "z": disp["z"],
        "rx": disp["rx"],
        "ry": disp["ry"],
        "rz": disp["rz"]
    })
    nodal_displacements_index += 1

# Create nodal forces
for force in point_forces:
    force_point = next(point for point in points if point["id"] == force["point-id"])
    force_node_id = next(node["id"] for node in nodes if node_collision(force_point, node))

    nodal_forces.append({
        "id": nodal_forces_index,
        "node-id": force_node_id,
        "fx": force["fx"],
        "fy": force["fy"],
        "fz": force["fz"],
        "mx": force["mx"],
        "my": force["my"],
        "mz": force["mz"]
    })
    nodal_forces_index += 1

# Assemble mesh file content
mesh_file_content = {
    "nodes": nodes,
    "elements-1D": elements_1D,
    "nodal-displacements": nodal_displacements,
    "nodal-forces": nodal_forces
}
# Create/Open mesh file and overwrite the content
with open("./mesh/mesh.json", "w") as mesh_file:
    json.dump(mesh_file_content, mesh_file, indent=2)

print("\nMesh generated successfully\n"+
      f"Number of nodes:                 {len(nodes)}\n"+
      f"Number of 1D elements:           {len(elements_1D)}\n"+
      f"Number of nodal displacement bc: {len(nodal_displacements)}\n"+
      f"Number of nodal force bc:        {len(nodal_forces)}\n"+
      f"Time elapsed:                    {round(time.time() - start_time, 8)} seconds\n")
