from flask_mail import Mail

mail = Mail()

class EmailConfig:
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'hibahrosary@gmail.com'
    MAIL_PASSWORD = 'borr ptps ornc oxdq'
    MAIL_DEFAULT_SENDER = 'hibahrosary@gmail.com'