
# Mlegal



## Installation

Clone the project and install the dependencies 

```bash
  pip install requirements.txt
```

Migrate 

```bash
  python manage.py migrate
```
    
Create superuser and run the server

```bash
  python manage.py createsuperuser
  python manage.py runserver
```
    


## Sending Emails

Using the admin panel add a few subscribers and a campaign
after starting the server


Export the environment variables DJANGO_SECRET_KEY, SMTP_USERNAME, SMTP_PASSWORD (use your mailgun domain credentials)

run the command to start sending emails

```bash
  python manage.py send_latest_campaign
```

