import urllib
import urllib2
import time
headers = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'} 
#url='http://3.raspberrypiserver.sinaapp.com/trainer/android/'
url='http://127.0.0.1:8000/update/'
#values={"no":2,"devices":'00:00:00:00:00:00',"devices":'00:00:00:00:00:01'}
values={"no":2,"ssi":-100,"mac":"10:00:00:00:00:00","time":time.time()*1000}
data=urllib.urlencode(values)
req=urllib2.Request(url,data,headers)
response=urllib2.urlopen(req)
#the_page=response.read()
#print the_page
