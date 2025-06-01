### Project Description  
Foodgram is an educational project from Yandex.Practicum.  

The goal of this website is to allow users to create and store recipes on an online platform. Additionally, users can:  
- Download a shopping list of ingredients needed for a dish.  
- Browse recipes from friends.  
- Save favorite recipes to a personal collection.  

### Technologies  
- Python 3.9  
- Django 3.2.3  
- Django REST framework 3.12.4  

### Local Deployment  

1. Install `docker` and `docker-compose` on your server.  
2. Create an `/infra/.env` file (use `/infra/.env.example` as a template).  
3. Run `docker-compose up -d --build`.  
4. Apply migrations:  
   ```bash  
   docker-compose exec backend python manage.py migrate  

### Author 

Shchegll ;)

