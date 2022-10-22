# neect-rally-tascas

Rally Tascas Web App made by **NEECT - Núcleo de Estudantes de Engenharia de Computadores e Telemática**

## Setup
- Setup MySQL database
```
$ chmod +x setup_mysql.sh
$ ./setup_mysql.sh
```
Use ```./setup_mysql.sh -h``` to see usage options.

- Create and enter a python virtual environment 
```
$ python3 -m venv venv
$ source venv/bin/activate
```

- Install necessary packages
```
$ pip install -r requirements.txt
```

- Run API server
```
$ python3 manage.py migrate &&
    python3 manage.py runserver
```

- Kill port 8000 if occupied (in case runserver fails)
```
$ sudo fuser -n tcp -k 8000
```

## API Docs
Swagger documentation for the API:  
[http://127.0.0.1:8000/api/docs](http://127.0.0.1:8000/api/docs) *(to be improved)*

Markdown documentation for the API:
[docs/README.md](docs/README.md)