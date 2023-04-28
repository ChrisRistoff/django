# !/bin/sh is the shebang line, which tells the shell what program to interpret the script with, in this case /bin/sh, the Bourne shell.

#!/bin/sh

# Exit on error
set -e

# wait for postgres to start
python manage.py wait_for_db

# collect static files and put them in the static folder
# --noinput tells Django not to ask the user any questions 
python manage.py collectstatic --noinput

# run migrations
python manage.py migrate

# run the server
# --socket :9000 tells uwsgi to listen on port 9000 for connections
# --workers 4 tells uwsgi to spawn 4 worker processes for handling requests
# --master tells uwsgi to start a master process that manages the worker processes
# --enable-threads tells uwsgi to enable threading within the worker processes
# --module app.wsgi tells uwsgi to use the wsgi.py file to serve the application
# app.wsgi is the wsgi.py file in the app folder
uwsgi --socket :9000 --workers 4 --master --enable-threads --module app.wsgi
