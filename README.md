# Bidnow 🔨 
A Blockchain powered charity auction for micromobility devices.

[Presentation link](https://www.canva.com/design/DAFZ0C5fHko/RoesW9ONoY4EHaFwKnIrpw/view?utm_content=DAFZ0C5fHko&utm_campaign=designshare&utm_medium=link&utm_source=publishsharelink)

[Site link with 2 minute auction time for try](http://35.157.207.149:8000)
## Idea 💡
The idea is to provide a auction site with the win
report saved on the blockchain. 

## Functionality and technology ⚙️

### Technologies :
- Django 
- Redis
- Web3
- Celery

The main functionality is a fast way to register the
bids aside of the main database in this case Sqlite
with Redis. Then with celery that control the schedule
of the auction and the end actions such as:
- update the model on sqlite with the winner
- serialize the model in json and register to the blockchain 
- delete the redis ended auction section to free space

## Installation 🔧

 - Make your virtual enviroment
 
 - Activate
 
 - Install pakages with requirements.txt
 
   ```js
   pip install -r requirements.txt
   ```
 - Make sure to insert your data in secret.py
 - Launch your redis server
 
 - Migrate
 
    ```js
   python manage.py migrate
   ```
 - Create super user only admin can make new auctions
 
   ```js
   python manage.py createsuperuser
   ```
 - Create superuser profile
 
    ```js
   python manage.py shell
   ```
   ```py
   from micromobility.models import Profile
   from django.contrib.auth.models import User
   s = User.objects.all()
   Profile.create(user=s[0])
   ``` 
 - Launch celery 
 
   ```js
   celery -A auction_house worker --loglevel=INFO
   ```
