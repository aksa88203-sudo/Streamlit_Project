Set-Location "C:\Users\ABU HURERA NOOR\Desktop\StreamLit_project"

if (Test-Path ".\venv\Scripts\Activate.ps1") {
    . .\venv\Scripts\Activate.ps1
}

python -m streamlit run app.py --server.port 8501
