# rally-tascas-api

Rally Tascas API made by **NEECT - Núcleo de Estudantes de Engenharia de Computadores e Telemática**  
This application was created using **Python** and **Django**.

## Setup
- Setup MySQL database
```bash
$ chmod +x setup_mysql.sh
$ ./setup_mysql.sh
```
Use ```./setup_mysql.sh -h``` to see usage options.

- Create and enter a python virtual environment 
```bash
$ python3 -m venv venv
$ source venv/bin/activate
```

- Install necessary packages
```bash
$ pip3 install -r requirements.txt
```

- Run API server
```bash
$ python3 manage.py migrate &&
    python3 manage.py runserver
```

- Kill port 8000 if occupied (in case runserver fails)
```bash
$ sudo fuser -n tcp -k 8000
```

- (Optional) Create superuser
```bash
$ python3 manage.py createsuperuser
```

## API Docs
Swagger documentation for the API:  
[http://127.0.0.1:8000/api/docs](http://127.0.0.1:8000/api/docs) *(to be improved)*

Markdown documentation for the API:  
[docs/README.md](docs/README.md)