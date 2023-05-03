# build_files.sh
sudo apt update
sudo apt install python3-venv
python3.9 -m venv .
source bin/activate
pip install --upgrade pip
pip install -r requirements.txt
python3.9 manage.py collectstatic