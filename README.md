# Casebook
Backend for our team's EECS 341 Final Project at Case Western Reserve University.

## Running the Backend
To run the backend first install all requirements:

`pip install -r requirements.txt`

Then run the gunicorn server:
`gunicorn --bind 0.0.0.0:8000 wsgi`

## Frontend
Frontend located here: https://github.com/BriungRi/casebook-web
