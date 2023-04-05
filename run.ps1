Write-Output "FEM analysis started"

py ./src/mesher.py
py ./src/plot-mesh.py
py ./src/matrix-assembler.py
py ./src/solver.py
py ./src/plot-results.py