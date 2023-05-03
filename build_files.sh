# build_files.sh
ls -l
echo $VIRTUAL_ENV
source bin/activate
pip install -r requirements.txt
python3.9 manage.py collectstatic