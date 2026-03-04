param(
    [switch]$Docker
)

Set-Location "C:\Users\ABU HURERA NOOR\Desktop\StreamLit_project"

if ($Docker) {
    Set-Location ".\fastapi_backend"
    docker compose up --build -d
    docker compose logs -f api
    exit $LASTEXITCODE
}

if (Test-Path ".\venv\Scripts\Activate.ps1") {
    . .\venv\Scripts\Activate.ps1
}

Set-Location ".\fastapi_backend"
python -m uvicorn app.main:app --host 127.0.0.1 --port 8001 --reload
