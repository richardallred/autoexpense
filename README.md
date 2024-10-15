# Automate expense reports for monthly cell phone bill

The `download_verizon_bill.py` script can be used to automate the download of the PDF of your cell phone bill from Verizon and submission of the expense to Concur

## Setup

### Install pre-requisites

1. Create a virtual environment and activate it and update pip (optional)
```
python -m venv autoExpenseVenv
```
```
[richardallred@fedora autoexpense]$ python -m venv autoExpenseVenv
[richardallred@fedora autoexpense]$ source autoExpenseVenv/bin/activate
(autoExpenseVenv) [richardallred@fedora autoexpense]$ pip install --upgrade pip
Requirement already satisfied: pip in ./testVenv/lib64/python3.12/site-packages (23.3.2)
Collecting pip
  Downloading pip-24.2-py3-none-any.whl.metadata (3.6 kB)
...
Successfully installed pip-24.2
```

2. Install dependencies with pip
```
pip install -r requirements.txt
```
```
(autoExpenseVenv) [richardallred@fedora autoexpense]$ pip install -r requirements.txt
Collecting selenium (from -r requirements.txt (line 1))
  Using cached selenium-4.25.0-py3-none-any.whl.metadata (7.1 kB)
...
Installing collected packages: sortedcontainers, websocket-client, urllib3, typing_extensions, sniffio, python-dotenv, pysocks, PyPDF2, packaging, idna, h11, charset-normalizer, certifi, attrs, wsproto, requests, outcome, webdriver-manager, trio, trio-websocket, selenium
Successfully installed PyPDF2-3.0.1 attrs-24.2.0 certifi-2024.8.30 charset-normalizer-3.4.0 h11-0.14.0 idna-3.10 outcome-1.3.0.post0 packaging-24.1 pysocks-1.7.1 python-dotenv-1.0.1 requests-2.32.3 selenium-4.25.0 sniffio-1.3.1 sortedcontainers-2.4.0 trio-0.26.2 trio-websocket-0.11.1 typing_extensions-4.12.2 urllib3-2.2.3 webdriver-manager-4.0.2 websocket-client-1.8.0 wsproto-1.2.0
```


### Configure Environment Variables for your Verizon Username and Password

```
export AUTOEXPENSE_VERIZON_USERNAME="8888675309"
export AUTOEXPENSE_VERIZON_PASSWORD="SuperS3cur3Pa55w0rd!"
export AUTOEXPENSE_RH_SSO_USER="rallred"
export AUTOEXPENSE_RH_EMAIL="rallred@redhat.com"
export AUTOEXPENSE_FIRST_NAME="Richard"
export AUTOEXPENSE_CITY="Chapel Hill, North Carolina"
export AUTOEXPENSE_DEVICE_AMT="38.88"
```

### Run Script

Run with `python autoexpense.py`, you will be prompted to enter your PIN + Token when the RH SSO Login begins, please input that and press `Enter`

```
(venv) [richardallred@fedora autoexpense]$ python autoexpense.py
Hello, Richard!
Deleted: /home/richardallred/devprojects/autoexpense/downloads/MyBill_09.20.2024.pdf
Download started successfully.
Extracted dollar amount: 118.45
Device Payment dollar amount: 38.88
Total expensable amount is: 79.57
Please input your PIN + Token for RH SSO:
Found /home/richardallred/devprojects/autoexpense/downloads/MyBill_09.20.2024.pdf

```


Use `--help` to see the available options for CLI overrides

```
(venv) [richardallred@fedora autoexpense]$ python autoexpense.py --help
usage: autoexpense.py [-h] [--name NAME] [--city CITY] [--downloadto DOWNLOADTO] [--deviceamt DEVICEAMT] [--headless] [--chrome-debug-port CHROME_DEBUG_PORT]

A simple python script for automation of expense reports

options:
  -h, --help            show this help message and exit
  --name NAME           Your first name on your verizon bill in case you have more than one line
  --city CITY           The city your transaction should be listed in fully spelled out seperated with a comma (ex. Chapel Hill, North Carolina)
  --downloadto DOWNLOADTO
                        Location of the directory to download the PDF to
  --deviceamt DEVICEAMT
                        Amount to subtract for your monthly device payment which is not reimbursable
  --headless            Should the browser run in a headless mode?
  --chrome-debug-port CHROME_DEBUG_PORT
                        Which port to run the chrome debugger on

```