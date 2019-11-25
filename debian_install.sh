#!/usr/bin/bash

# Install virtualenv
sudo apt install python3-virtualenv
sudo apt install python3-pip
virtualenv venv
source venv/bin/activate

# Install requirements
pip3 install -r requirements.txt

echo "Done! Now run the project with debian_run.sh"
