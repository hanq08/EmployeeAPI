# EmployeeAPI
## Overview
This api is a http-based api built by django rest framework.Below is the ER diagram of the database schema.
![alt text](https://s3.amazonaws.com/luluwondering/er.jpg)
## Prerequisites
- Python 2.7
- Django==1.11.4
- djangorestframework==3.6.3
- pytz==2017.2
## Quickstart
- Create virtual environment with python2.7
`virtualenv -p /usr/local/bin/python27 venv `
- Install dependencies
`pip install -r requirements.txt`
- Load initial data for the role table which represents the organization hierarchy: CEO --> VP --> Director --> Manager --> Individual contributor
`python manage.py loaddata role.json`
- Run django development server
`python manage.py runserver`
## Reference
### Employee
- Read
`GET /employee`
`GET /employee/{employee-id}`
- Create
`POST /employee`
When creating a new employee, supervisor_id must be provided. Endpoint `/supervisors` can be used to add more supervisor to the employee (see below). 
Fields
  - first_name: String
  - last_name: String
  - phone(optional): String
  - salary: Integer
  - role_id: Integer
  - performance_review: Integer
  - supervisor_id: Integer
- Update
`PUT /employee/{employee-id}`
`PATCH /employee/{employee-id}`
Role can't be changed once created. Employee can be promoted with the `/promote/{employee-id}` endpoint (see below). Employee can't be demoted.
Fields
  - first_name: String
  - last_name: String
  - phone(optional): String
  - salary: Integer
  - performance_review: Integer
- Deleting
`DELETE /employee/{employee-id}
### EmployeeSupervisor
This table represents the many to many report relationship between employees.
- Read
`GET /supervisors`
- Create
`POST /supervisors`
When creating a new report relation, supervisor rank must be equal or higher than employee's rank.
Fields
  - employee: Integer
  - supervisor: Integer
### Role
- Read
`GET /role`
`GET /role/{role-id}`
- Update
`PUT /employee/{role-id}`
Rank can't be changed. 
Fields
  - name: String
- Deleting
`DELETE /role/{role-id}
#### Promotion
Promote a employee one rank higher. Employee's supervisor will be changed to the employee first supervisor's supervisor
`PUT /promote/{employee-id}`
