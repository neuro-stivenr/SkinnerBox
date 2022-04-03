# SkinnerBox

## System Dependencies

1. python3
2. python3-venv
3. make

## Install & Run

On a Unix-like system:

```bash
cd SkinnerBox
make # to install
make run # to run
```

I haven't tested the installation on Windows, but it probably goes something like this in PowerShell:

```powershell
cd SkinnerBox
# to install
python -m venv env
.\env\Scripts\activate.ps1
pip install -r requirements.txt
# to run
python game.py
```
