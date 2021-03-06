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

# Make calls to API
## GET request in web browser
http://127.0.0.1:5000/api/v1...

## Requests in curl
### GET request
curl http://127.0.0.1:5000/api/v1/accounts/all

### POST request
curl -X POST -H "Content-Type: application/json" http://127.0.0.1:5000/api/v1/accounts -d "{\"id\":123456789,\"allowance\":100}"

### PUT request
curl -X PUT -H "Content-Type: application/json" http://127.0.0.1:5000/api/v1/transactions -d "{\"id\":\"d703253dcc934644b4070af64e69b495\",\"action\":\"approve\"}"
```
