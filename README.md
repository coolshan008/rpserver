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


####USAGE
1. Gather data
2. trainer/re to get tuple
3. trainer/train to train model
4. Gather testing data
6. trainer/testing to get training acc
7. classify/ to classify all devices' position and update the devices num in each classroom
8. cron/ to refresh state of classroom every 5 min
9. inquiry/ quiry the devices num in certain room

- train will sample part of the tuple to train for each classroom  
- **index of classroom should start from 0**
- time is count in seconds


