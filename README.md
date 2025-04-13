# Learning Management System

A web-based Learning Management System built with Flask.

## Features
- User Authentication (Student/Teacher)
- Email Verification
- Course Management
- Assignment Handling
- User Profiles

## Setup
1. Clone the repository
2. Create a virtual environment: `python -m venv venv`
3. Activate virtual environment: `venv\Scripts\activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Set up environment variables in `.env` file
6. Run the application: `python run.py`

## Environment Variables
Create a `.env` file with:
- SECRET_KEY
- DATABASE_URL
- MAIL_USERNAME
- MAIL_PASSWORD

## Technologies Used
- Flask
- SQLAlchemy
- Flask-Mail
- MySQL