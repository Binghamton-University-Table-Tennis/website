# rating-system
Web application displaying the ratings for Binghamton Table Tennis Club members

## Website URL
https://binghamtontabletennis.herokuapp.com/

## To run locally on Cloud9
First, create a new Python workspace. Then, enter the following commands in bash:
- $ git clone https://github.com/BinghamtonTableTennis/rating-system
- $ cd rating-system/
- $ sudo pip install -r requirements.txt
- $ sudo service postgresql start
- $ export DATABASE_URL=postgres:///"$(whoami)"
- $ export SECRET_KEY="$(cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 32 | head -n 1)"
- $ touch .env
- $ python manage.py migrate
- $ python manage.py collectstatic
- $ heroku local

## To create a local admin
- $ python manage.py createsuperuser
