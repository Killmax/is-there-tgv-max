# is-there-tgv-max
Simple script to get an email with all the TGV Max Train available on a specific day.

To get these information, I'm using here the request from the official website of SNCF (oui.sncf).

## Installation

The mail delivery system used here is SendGrid. You will need to go on their website and get an API key.

Moreover, you will need Python3 and two modules called SendGrid-Python and Requests.

```bash
pip install sendgrid-python
pip install requests
``` 

You will also need to set three environments variables

```bash
EMAIL_FROM="john.doe@example.com" # The address from which the email will be sent
EMAIL_TO="john.doe@example.com" # The address which will receive the email
SENDGRID_API_KEY="SG..." # The API key coming from your account on Send Grid.
```

## Usage

The script must be executed like this:
```bash 
.\script.py <RRCODE CITY FROM (FRPAR, FRLIL, etc.)> <RRCODE CITY TO> <DATE (YYYY-mm-DD)>
```


