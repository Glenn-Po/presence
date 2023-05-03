# build_files.sh
apt update
apt install python3-venv
python3.9 -m venv .
source bin/activate
pip install --upgrade pip
pip install -r requirements.txt
python3.9 manage.py collectstatic