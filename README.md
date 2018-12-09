# PoetToneWeb
Poetry Website
## Setup
>Install requirements

>Install PostgreSql

>Remember your sql username and password from setup

>Create database and call it PoetTone

> Navigate to config.py and change line:
SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:shuttle@localhost:5432/PoetTone'
by replacing 'postgresql://YOURSQLUSERNAME:YOURSQLPASSWORD@localhost:5432/PoetTone'

>Go to dbUpdater.py and follow directions in comments on first line. Run dbUpdater.py

>In routes.py uncomment first function (lines 10-24) of the file (this function will be
called as soon as you start the app. The function uses nlp to find poems that are similar.
It then adds these similar poems to a table in the db.)

>
>cd to app root folder

>In terminal type FLASK_APP=PoetTone.py and hit enter

> type flask run to run the app on localhost

>Try to connect to app's localhost in a browser. It will not work right away. The recommender
function you uncommented is doing its magic.

>look at your terminal for progress updates on the recommender. It should take about 10 mins.

>Once its done you should be able to load the webpage. Comment out the function you 
uncommented in routes.py. You don't have to rerun the recommender calculations unless you change
the poems in the database.
