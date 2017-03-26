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

## How to use the admin panel
On the admin panel, you will see 5 tables available to modify with Add/Change options:
- Club Attendance
- Matches
- Players
- Slides
- Updates

### Club Attendance
To keep track of attendance for a practice, use the Club Attendance table. Simply ask members to enter their first and last name. At 3:30 UTC, a script will automatically run to go through the Club Attendance and store them in an attendance_history table to be displayed on the Attendance page (admin only).

### Matches
To record ranked matches, enter the winner and loser names and the score (best of 3 match). The same script for the Club Attendance will collect the match results and update the ladder page as well as individual match history pages.

### Players
To manually add a new player to the database, have members enter their first and last name and class standing. Note: New members who sign in on the Club Attendance form will automatically have a Player entry created for them.

### Slides
To add a new slideshow to the photos page, you need to add a date, title, and a slides ID.
- Date: Needed to organize slides to ascending order
- Title: Used to label a slideshow
- Slides ID: The ID of the slideshow (see below)

##### How to get the Slides ID
- In your browser, open up the Google Slides you want to share on the photos page
- Make sure the slideshow is published (File -> Publish to the web -> Publish)
- Look for the slides ID in the URL.

For example, if the URL is:

      https://docs.google.com/presentation/d/1152Jzvxr-hDXlGE1zaT4_NuZf8sl-GAIvCUhhzMA800/edit#slide=id.g1b0ebe7be8_0_0
the Slides ID is:

      1152Jzvxr-hDXlGE1zaT4_NuZf8sl-GAIvCUhhzMA800

### Updates
To post an update on the front page, simply enter the date and the message you want to display.

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
