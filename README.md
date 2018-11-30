# Casebook
Backend for our team's EECS 341 (Databases) final project at Case Western Reserve University.

## Running the Backend
### Clone the repository

`git clone https://github.com/marklalor/casebook.git && cd casebook`

### Install Python requirements

`Casebook` requires `python 3.7.0` or higher.

After installing `python 3.7.0` or higher, install all requirements:

`pip install -r requirements.txt`

### Install and setup MySQL
Install the `MySQL` database.

Modify the `casebook/db/database.ini` file with the host, username,
and password corresponding to your own `MySQL` installation.

### Initialize the database

Then you must initialize the database (optionally with test data)

The following command will delete any existing database, initialize a new 
one with the proper schema, and then fill in some test data:

`python casebook/db/db.py delete init fill`

To initialize without the test data, the following will suffice:

`python casebook/db/db.py delete init`

### Running the server

Then run the `gunicorn` server (`gunicorn` should be on your path after the previous `pip install`):

`gunicorn --bind 0.0.0.0:8000 wsgi`

## Running and using the frontend

Frontend code and instructions located here: `https://github.com/BriungRi/casebook-web`
