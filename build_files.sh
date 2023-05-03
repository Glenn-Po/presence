# build_files.sh
source ./bin/activate
pip install -r requirements.txt
python3.9 manage.py collectstatic