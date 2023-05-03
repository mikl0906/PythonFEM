# Simple FEM implimented in Python.

## Definitions

Project folder - root folder. Project specific.
Model folder - wraps the files of a specific simulation inside the project folder

## Proposed workflow

- Create Project folder
- Create a Model folder inside the Project folder
- Run the model. The results are going to appear under the model folder
- Postprocess the results

## Project folder

Root folder. for the project simulations

### Content

- library folder (optional) - material and cross-sections common for all models
- Model folders - contains all the data for the specific simulation
- README.md - description of the project

## Model folder

Contains all the data for the simulation

### Content

- geometry.json - defines the geometry
- boundary-conditions.json - defines the boundary conditions
- fem_data folder - contains simulation intermediate files and results
  - mesh.json - contains generated mesh and boundary conditions
  - matrices.json - contains assembled matrices of the system
  - reuslts.json - contains results at degrees of freedom
- settings.json - simulation settings
- materials.json (optional) - material data
- cross-section.json (optional) - cross-section data

## Library folder

Contains material and cross-sections common for all models

### Content

- materials.json (optional) - material data
- cross-section.json (optional) - cross-section data
