from models import session, Reminder
import time
import requests


while True:

    for reminder in session.query(Reminder).filter(Reminder.time <= time.time()):

        print('Reminder going')

        requests.post(reminder.webhook, {'content': reminder.message, 'name': 'Reminders', 'avatar_url': 'https://raw.githubusercontent.com/reminder-bot/logos/master/Remind_Me_Bot_Logo_PPic.jpg'})
        session.query(Reminder).filter(Reminder.id == reminder.id).delete(synchronize_session='fetch')

    time.sleep(2.5)
