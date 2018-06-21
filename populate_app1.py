import os
os.environ.setdefault(
  'DJANGO_SETTINGS_MODULE',
  'courseproj.settings'
)

import django
django.setup()

## FAKE POP SCRIPT
import random
from app1.models import AccessRecord, Webpage, Topic, User
from faker import Faker

fakegen = Faker()
topics = ['Search', 'Social', 'Marketplace', 'News', 'Games']

def add_topic():
  t = Topic.objects.get_or_create(top_name=random.choice(topics))[0]
  t.save()
  return t

def populate(N=5):
  for entry in range(N):
    # Get the topics for the entry
    top = add_topic()

    # Create the fake data for that entry
    fake_url = fakegen.url()
    fake_date = fakegen.date()
    fake_name = fakegen.company()
    fake_email = fakegen.email()
    fake_fn = fakegen.first_name()
    fake_ln = fakegen.last_name()

    # Create the new webpage entry
    webpg = Webpage.objects.get_or_create(topic=top, url=fake_url, name=fake_name)[0]

    # Create fake access record for that webpage
    acc_rec = AccessRecord.objects.get_or_create(name=webpg, date=fake_date)[0]

    # Create fake users
    users = User.objects.get_or_create(email=fake_email, first_name=fake_fn, last_name=fake_ln)


if __name__ == '__main__':
  print("Populating script!")
  populate(20)
  print("Populating complete!")
