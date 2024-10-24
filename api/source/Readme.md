### Rough API Setup Steps

### SQL DB Setup

- Make sure you have Sql Server Mangement Studio installed if on windows

### Env Setup

1. Copy `.env.empty` into the same directory and rename the copy as `.env`
2. Fill in vars that are needed

### Python Setup

### Required Python 3.11 and PIP 23.1.2 (PIP 23.1.2 is installed with Python 3.11)

1. Install Python
2. Run `python -m pip install --user virtualenv`
3. Go to `/api/`
4. Run `python -m venv venv`
5. Run `./venv/scripts/activate`
   NOTE: May need to run powershell script: Set-ExecutionPolicy -ExecutionPolicy Bypass
6. Run `pip install -r ./source/requirements.txt`
7. Start Api by `cd ./source` and running `flask run --reload`
