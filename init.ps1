$ErrorActionPreference = "Stop"

Write-Host "Creating virtual environment..."
python -m venv venv

Write-Host "Upgrading pip..."
.\venv\Scripts\python.exe -m pip install --upgrade pip

Write-Host "Installing project in editable mode..."
.\venv\Scripts\pip.exe install -e .

Write-Host "Creating directories..."
$directories = @(
    "./data/raw/benign",
    "./data/raw/malicious/coap-amplificator",
    "./data/raw/malicious/network-scanning",
    "./data/raw/malicious/merlin",
    "./data/raw/malicious/mirai-dos",
    "./data/raw/malicious/mirai-infection",
    "./data/extracted_features/benign",
    "./data/extracted_features/malicious/coap-amplificator",
    "./data/extracted_features/malicious/network-scanning",
    "./data/extracted_features/malicious/merlin",
    "./data/extracted_features/malicious/mirai-dos",
    "./data/extracted_features/malicious/mirai-infection",
    "./data/labelled/benign",
    "./data/labelled/malicious/coap-amplificator",
    "./data/labelled/malicious/network-scanning",
    "./data/labelled/malicious/merlin",
    "./data/labelled/malicious/mirai-dos",
    "./data/labelled/malicious/mirai-infection",
    "./data/processed"
)

foreach ($dir in $directories) {
    if (-not (Test-Path $dir)) {
        New-Item -ItemType Directory -Force -Path $dir | Out-Null
    }
}

Write-Host "Initialization completed."
