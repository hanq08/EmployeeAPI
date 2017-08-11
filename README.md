# EmployeeAPI
## Overview
This api is a http-based api built by django rest framework. Below is the ER diagram of the database schema.
![alt text](https://s3.amazonaws.com/luluwondering/er.jpg) 
## Prerequisites
- Python 2.7
- Django==1.11.4
- djangorestframework==3.6.3
- pytz==2017.2
## Quickstart
- Create virtual environment with python2.7 <br>
`virtualenv -p /usr/local/bin/python27 venv `
- Install dependencies <br>
`pip install -r requirements.txt`
- Load initial data for the role table which represents the organization hierarchy: CEO --> VP --> Director --> Manager --> Individual contributor <br>
`python manage.py loaddata role.json`
- Run django development server <br>
`python manage.py runserver`
- Tests <br>
`python manage.py test`
## Reference
### Employee
- Read <br>
`GET /employee` <br>
`GET /employee/{employee-id}` 
- Create <br>
`POST /employee` 
When creating a new employee, supervisor_id must be provided. Endpoint `/supervisors` can be used to add more supervisor to the employee (see below). <br>
Fields
  - first_name: String
  - last_name: String
  - phone(optional): String
  - salary: Integer
  - role_id: Integer
  - performance_review: Integer
  - supervisor_id: Integer
- Update <br>
`PUT /employee/{employee-id}` <br>
`PATCH /employee/{employee-id}` <br>
Role can't be changed once created. Employee can be promoted with the `/promote/{employee-id}` endpoint (see below). Employee can't be demoted. <br>
Fields
  - first_name: String
  - last_name: String
  - phone(optional): String
  - salary: Integer
  - performance_review: Integer
- Deleting <br>
`DELETE /employee/{employee-id}`
### EmployeeSupervisor
This table represents the many to many report relationship between employees.
- Read <br>
`GET /supervisors`
- Create <br>
`POST /supervisors` <br>
When creating a new report relation, supervisor rank must be equal or higher than employee's rank. <br>
Fields
  - employee: Integer
  - supervisor: Integer
- Update <br>
`PUT /supervisors/{id}` <br>
- Deleting <br>
`DELETE /supervisors/{id}`
### Role
Role can't be created by the api. <br>
- Read <br>
`GET /role` <br>
`GET /role/{role-id}` 
- Update <br>
`PUT /employee/{role-id}` <br>
Rank can't be changed. <br>
Fields 
  - name: String
- Deleting <br>
`DELETE /role/{role-id}`
#### Promotion
Promote a employee one rank higher. Employee's supervisor will be changed to the employee first supervisor's supervisor <br>
`PUT /promote/{employee-id}`
### Issues
- Implement more unit tests.
