# Lost & Found

## Team Members
- **Azat Gainolla** – 220103291  19-p
- **Alikhan Nassikhov** – 220103368  19-p
- **Alikhan Galymzhan** – 220103203  14-p
- **Berik Rakhmetov** – 220103146  13-p

---

## About the Project

**Lost & Found** is a community-driven platform to help people report and find lost items. Whether you've lost your belongings or found someone else’s, our system makes it fast and secure to connect and resolve the issue.

---

## Objectives
Provide a simple way to report and claim lost items

Improve item recovery rates through search and filters

Enable secure communication between finders and owners



## Features

- Search for lost items  
- Filter items by categories  
- View all reported items  
- Report found items  
- Claim lost items via request system  

---

## Tech Stack

- **Backend:** Python, Django  
- **Database:** PostgreSQL  
- **Admin Tool:** PgAdmin  
- **Storage:** MinIO for media files  
- **Containerization:** Docker & Docker Compose  

---

## How to Run the Project


```bash
git clone https://github.com/azatgainolla026/Lost-And-Found.git
cd lostandfound
docker-compose up --build
docker-compose exec web python manage.py makemigrations
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
```
## Access the App

Django App: http://localhost:8000/

Admin Panel: http://localhost:8000/admin/

PgAdmin: http://localhost:5050/

MinIO Console: http://localhost:9001/


## References

Django documentation: https://docs.djangoproject.com/

MinIO: https://min.io/docs/minio

Docker Compose: https://docs.docker.com/compose/

PostgreSQL: https://www.postgresql.org/docs/

## Requirements 

Docker Desktop installed
