####ENVIROMENT:
- python 2.7
- django 1.4
- mysql 5.6

####INSTALLATION COMMAND：
$sudo apt install python  
$wget https://bootstrap.pypa.io/get-pip.py  
$sudo python get-pip.py  
$sudo apt install mysql-server  
DEFAULT PASSWORD FOR root: admin  
$sudo pip install django==1.4  
$sudo apt install python-mysqldb    

$mysql -u root -p  
mysql> create database raspberry;  
[Ctrl-d]  

enter the root of the project  
$python manage.py syncdb  
create super account  

$crontab -e
[edit mode]  
(insert)  
*/3 * * * * curl http://localhost:8000/corn  

$python manage.py runserver [your ip:port]  

