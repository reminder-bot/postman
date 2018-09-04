from models import session, Reminder, Deletes
import time
import requests
from datetime import datetime
import configparser


config = configparser.SafeConfigParser()
config.read('config.ini')

while True:

    rems = []
    for reminder in session.query(Reminder).filter(Reminder.time <= time.time()).filter(Reminder.webhook != ''):

        url_w = reminder.webhook + '?wait=true'
        url = reminder.webhook

        rems.append(reminder.id)
        print('Looping for reminder {}'.format(reminder))

        if reminder.interval is not None and reminder.interval < 8:
            continue

        try:
            if reminder.interval is None:
                requests.post(url, {'content': reminder.message, 'username': 'Reminders', 'avatar_url': 'https://raw.githubusercontent.com/reminder-bot/logos/master/Remind_Me_Bot_Logo_PPic.jpg'})

                print('{}: Administered reminder to {}'.format(datetime.utcnow().strftime('%H:%M:%S'), reminder.webhook))

            else:
                rems.remove(reminder.id)

                if reminder.message.startswith('-del_after_'):

                    chars = ''

                    for char in reminder.message[len('-del_after_'):]:
                        if char in '0123456789':
                            chars += char
                        else:
                            break

                    wait_time = int(chars)

                    t = requests.post(url_w, {'content': reminder.message[len('-del_after_' + chars):], 'username': 'Reminders', 'avatar_url': 'https://raw.githubusercontent.com/reminder-bot/logos/master/Remind_Me_Bot_Logo_PPic.jpg'})

                    d = Deletes(time=time.time() + wait_time, channel=reminder.channel, message=t.json()['id'])

                    session.add(d)

                else:
                    requests.post(url, {'content': reminder.message, 'username': 'Reminders', 'avatar_url': 'https://raw.githubusercontent.com/reminder-bot/logos/master/Remind_Me_Bot_Logo_PPic.jpg'})

                print('{}: Administered interval to {} (Reset for {} seconds)'.format(datetime.utcnow().strftime('%H:%M:%S'), reminder.webhook, reminder.interval))

                while reminder.time <= time.time():
                    reminder.time += reminder.interval ## change the time for the next interval

        except Exception as e:
            print('Ln 1033: {}'.format(e))

    if len(rems) > 0:
        session.query(Reminder).filter(Reminder.id.in_(rems)).delete(synchronize_session='fetch')

    time.sleep(2.5)
    session.commit()
