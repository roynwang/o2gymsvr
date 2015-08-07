mysql -uroot -p435393055 -e'drop database o2gym;CREATE DATABASE o2gym DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci'
python manage.py migrate
python manage.py runserver 0.0.0.0:8000
