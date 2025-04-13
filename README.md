# Learning Management System

A web-based Learning Management System built with Flask.

## Features
- User Authentication (Student/Teacher)
- Email Verification
- Course Management
- Assignment Handling
- User Profiles

## Prerequisites
- Python 3.8 or higher
- MySQL Server
- Git

## Setup Instructions
1. Clone the repository: git clone https://github.com/ArkanRiyasath/LMS-Project.git cd LMS-Project
2. Create a virtual environment: `python -m venv venv`
3. Activate virtual environment: 
    - Windows: `venv\Scripts\activate`
    - Linux/Mac: `source venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Set up MySQL database:
    - Install MySQL Server
    - Create a new database named 'lms'
    - Update DATABASE_URL in .env file with your credentials
6. Create a .env file with the following:
    SECRET_KEY=your-secret-key-here
    DATABASE_URL=mysql+pymysql://username:password@localhost/lms
    MAIL_USERNAME= your-email@gmail.com MAIL_PASSWORD=your-app-password
7. Initialize the database: flask db upgrade
8. Run the application: python run.py
9. Access the application:
    - Open your web browser
    - Go to: http://localhost:5000

## Email Setup
For Gmail users:
1. Enable 2-Step Verification in your Google Account
2. Generate an App Password:
    - Go to Google Account Settings
    - Security → App Passwords
    - Generate a password for your app
    - Use this password in your .env file

## Common Issues & Solutions
1. Database Connection Error:
    - Verify MySQL is running
    - Check database credentials
    - Ensure database 'lms' exists

2. Email Verification Issues:
    - Confirm Gmail App Password is correct
    - Check spam folder for verification emails
    - Verify MAIL_USERNAME and MAIL_PASSWORD in .env

3. Dependencies Issues:
    - Make sure virtual environment is activated
    - Run: pip install -r requirements.txt

## Technologies Used
- Flask (Web Framework)
- SQLAlchemy (Database ORM)
- Flask-Mail (Email Service)
- MySQL (Database)
- Flask-Login (Authentication)

## Project Structure
    LMS/
    ├── routes/          # Route handlers
    ├── models/          # Database models
    ├── templates/       # HTML templates
    ├── static/          # Static files (CSS, JS)
    ├── config/         # Configuration files
    ├── migrations/     # Database migrations
    └── requirements.txt # Project dependencies

## Support
For issues and questions, please open an issue in the GitHub repository.