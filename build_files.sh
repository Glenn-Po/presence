# build_files.sh
# pip install python3-venv
# python3.9 -m venv .
# source bin/activate
pip install venv
python3.9 -m venv .
source ./bin/activate
pip install --upgrade pip
pip install wheel
pip install -r requirements.txt
python3.9 manage.py collectstatic