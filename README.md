# Binghamton University Table Tennis Club Website
Our website provides the following information to all users:
- A ladder that organizes users based on the USATT rating system
- Player information (wins, losses, match history)
- Club photos at past tournaments
- About us page
- The ITTF rules for table tennis
- Contact page
- Home page with club info, updates, and links to other social media

For admins only:
- Track attendances at each practice (including late members)
- Add new players to the database
- Add matches to the database
- View summary statistics (Average players per practice, total front page visits, and more)
- Display messages/updates on the front page
- Add new Google Slides to the photos page

## Website URL
https://binghamtontabletennis.herokuapp.com/

## To run locally on Cloud9
First, create a new Python workspace. Then, enter the following commands in bash:

    $ git clone https://github.com/BinghamtonTableTennis/rating-system
    $ cd rating-system/
    $ sudo apt-get update
    $ sudo apt install libpq-dev python-dev
    $ sudo pip install -r requirements.txt
    $ sudo service postgresql start
    $ export DATABASE_URL=postgres:///"$(whoami)"
    $ export SECRET_KEY="$(cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 32 | head -n 1)"
    $ touch .env
    $ python manage.py migrate
    $ python manage.py collectstatic
    $ heroku local

## To create a local admin
    $ python manage.py createsuperuser

## To access the admin panel
Go to /admin and enter admin credentials

## Deploying to Heroku from Cloud9
Make sure you have a local copy working as explained above. Next, create a Heroku account at https://www.heroku.com/. Then, run the following command (enter credentials when prompted):

    $ heroku create

Now, go to the Heroku site for your new app, go to Settings, click Reveal Config Vars, and create a key called SECRET_KEY. Enter anything you would like for the value. Then, run the following two commands:

    $ git push heroku master
    $ heroku run python manage.py migrate

You can now navigate to your brand new URL hosted on Heroku.

## To create an admin on Heroku
    $ heroku run python manage.py createsuperuser
