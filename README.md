# mutual-credit-server
A mutual credit system implemented as an API

## Getting started
```
# Clone repo
git clone https://github.com/NamesJ/mutual-credit-server
cd mutual-credit-server

# Setup virtual environment
python -m venv venv

## Activate virtual environment
## Linux
source <venv>/bin/activate

## Windows
### Command Prompt
<venv>\Scripts\activate.bat

### Powershell
<venv>\Scripts\activate.ps1

## Install requirements
python -m pip install -r requirements.txt

# Start the API server
python main.py

# Seed the database via API client
python test/seed_db.py
```
