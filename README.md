# rally-tascas-api

Rally Tascas API made by **NEECT - Núcleo de Estudantes de Engenharia de Computadores e Telemática**  
This application was created using **Python** and **Django**.

## Table of Contents

1. [Setup](#setup)
1. [API Docs](#api-docs)
1. [Generate Data](#generate-data)

## Setup
1. Setup MySQL database
```bash
$ chmod +x setup_mysql.sh
$ ./setup_mysql.sh
```
Use ```./setup_mysql.sh -h``` to see usage options.

2. Create and enter a python virtual environment 
```bash
$ python3 -m venv venv
$ source venv/bin/activate
```

3. Install necessary packages
```bash
$ pip3 install -r requirements.txt
```

4. Run API server
```bash
$ python3 manage.py migrate &&
    python3 manage.py runserver
```

5. Kill port 8000 if occupied (in case runserver fails)
```bash
$ sudo fuser -n tcp -k 8000
```

6. (Optional) Create superuser
```bash
$ python3 manage.py createsuperuser
```

## API Docs
Swagger documentation for the API:  
[http://127.0.0.1:8000/api/docs](http://127.0.0.1:8000/api/docs) *(to be improved)*

Markdown documentation for the API:  
[docs/README.md](docs/README.md)


## Generate Data

You can generate bulks of data, dummy or not, to the database with the following:

1. Make sure to have created a superuser (see above)

2. Put the data inside the json files in the folder /data

3. Make sure the server is running (see above)

4. Run the data generator:

```bash
cd data
$ python3 generator.py
```