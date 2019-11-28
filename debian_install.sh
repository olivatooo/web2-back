#!/usr/bin/bash

# Install virtualenv
sudo apt install python3-virtualenv
sudo apt install python3-pip
virtualenv venv
source venv/bin/activate

# Install requirements
pip3 install -r requirements.txt

# Create database
python3 manage.py migrate
python3 manage.py makemigrations
python3 manage.py migrate tresvago

# Creating super user
python3 manage.py createsuperuser

echo "Done! Now run the project with debian_run.sh"
