# build_files.sh
# pip install python3-venv
# python3.9 -m venv .
# source bin/activate
# apt-get install mysql-client
# pip3 install --upgrade venv
# python3.9 -m venv .
# source ./bin/activate
pip3 install --upgrade pip
python3.9 -m pip install -r requirements.txt
python3.9 manage.py collectstatic