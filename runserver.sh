sudo nginx -s stop
sudo nginx -c /etc/nginx/nginx.conf
python manage.py runserver 

# the http server runs on 8000 port and is redirected from 8080 port
# so the server can be accessed through localhost:8000 or address:8080
