# KitchenService

KitchenService is a web application designed to manage restaurant operations efficiently. It allows users to manage dishes, cooks, and dish types.

## Live Demo

The project is deployed on Render. You can access it here:  
[KitchenService Live](https://kitchenservice-7.onrender.com/accounts/login/?next=/)


## Test Credentials

To help you explore the functionality, you can log in using the following test user credentials:

- **Login:** admin123
- **Password:** admin123

## Features

- View, add, update, and delete dishes
- Manage cooks and assign them to dishes
- Filter dishes and cooks using search forms
- User authentication and authorization
- Secure storage of sensitive data

## Installation

Follow these steps to run the project locally:

1.Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

2.Install dependencies
pip install -r requirements.txt

3.Set up environment variables
Create a .env file in the root directory and add the required environment variables:
SECRET_KEY=your_secret_key
DEBUG=True
DATABASE_URL=sqlite:///db.sqlite3  # Change this if 
using PostgreSQL or another databas

4.Apply migrations
python manage.py migrate

5.Create a superuser (optional, for admin access)
python manage.py createsuperuser

6.Run the development server
python manage.py runserver

Now, open http://127.0.0.1:8000/ in your browser to access the app.e
### 1. Clone the repository

```bash
git clone https://github.com/Julia15031988/KitchenService.git
cd KitchenService
