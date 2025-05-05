# Lost & Found

## Team Members
- **Azat Gainolla** – 220103291  
- **Alikhan Nassikhov** – 220103368  
- **Alikhan Galymzhan** – 220103203  
- **Berik Rakhmetov** – 220103146  

---

## About the Project

**Lost & Found** is a community-driven platform to help people report and find lost items. Whether you've lost your belongings or found someone else’s, our system makes it fast and secure to connect and resolve the issue.

---

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
##Access the App

Django App: http://localhost:8000/

Admin Panel: http://localhost:8000/admin/

PgAdmin: http://localhost:5050/

MinIO Console: http://localhost:9001/
