import urllib
import urllib2
url="http://127.0.0.1:8000"
req=urllib2.Request(url)
print req
res_data=urllib2.urlopen(req)
res=res_data.read()
print res
