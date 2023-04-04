Write-Output "FEM analysis started"

py ./mesh/mesher.py
py ./fem_data/matrix-assembler.py
py solver.py