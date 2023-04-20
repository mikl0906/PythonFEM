Write-Output "# FEM analysis started"

$model_path = $PSScriptRoot

# Generate mesh
py ./src/mesher.py $model_path

# Create matrices
if ($LASTEXITCODE -eq 0) {
    py ./src/matrix-assembler.py $model_path
}
else {
    Exit
}

# Solve the system
if ($LASTEXITCODE -eq 0) {
    py ./src/solver.py $model_path
}
else {
    Exit
}

Write-Output "# FEM analysis finished"

