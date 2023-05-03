# build_files.sh
# pip install python3-venv
# python3.9 -m venv .
# source bin/activate
wget https://dev.mysql.com/get/mysql-apt-config_0.8.15-1_all.deb
sudo dpkg -i mysql-apt-config_0.8.15-1_all.deb
sudo apt-get update
sudo apt-get install mysql-client
pip install --upgrade pip
pip install wheel
pip install -r requirements.txt
python3.9 manage.py collectstatic