import requests
import json
import time
import datetime
from bs4 import BeautifulSoup

timetamp = int(datetime.datetime.now().timestamp())

root = "C:\\360Downloads\\spider"

print(timetamp)


url = "http://vs26.thisav.com/dash/4kcdLQqn2AxzVuSjX9OobA,1514470339/140853.mpd"

headers = {
    'accept': "*/*",
    'accept-encoding': "gzip, deflate",
    'accept-language': "zh-CN,zh;q=0.9",
    'host': "vs26.thisav.com",
    'origin': "http://www.thisav.com",
    'proxy-connection': "keep-alive",
    'referer': "http://www.thisav.com/video/140853/undress-deep-desire-%E2%80%90jealousy%E2%80%90.html",
    'user-agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36",
    'cache-control': "no-cache",
    'postman-token': "38598f67-46c8-628f-eaea-dc4771fc22c7"
    }

response = requests.request("GET", url, headers=headers)



soup = BeautifulSoup(response.text,'xml')

ret = []

initRange = soup.find('Initialization').get('range')
ret.append(initRange)

ranges = soup.find_all('SegmentURL')
for range in ranges:
    ret.append(range.get('mediaRange'))

print(ret)




url = 'http://vs26.thisav.com/dash/4kcdLQqn2AxzVuSjX9OobA,1514470339/140853_dashinit.mp4'

headers = {
    'accept': "*/*",
    'accept-encoding': "gzip, deflate",
    'accept-language': "zh-CN,zh;q=0.9",
    'host': "vs26.thisav.com",
    'origin': "http://www.thisav.com",
    'proxy-connection': "keep-alive",
    #'Access-Control-Request-Headers':'range',
    #'Access-Control-Request-Method':'GET',
    #'range': "bytes=341945-834335",
    #'referer': "http://www.thisav.com/video/244761/%E7%9C%9F%E6%AD%A3%E5%BC%B7%E5%A7%A6%E6%98%AF%E5%90%88%E6%B3%95%E7%9A%84%E5%A4%A7%E5%A4%A7%E5%8A%9B%E5%81%9A%E6%84%9B%E5%AD%B8%E7%94%9F.html",
    'user-agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36",
    'cache-control': "no-cache",
    }





def fun(start,end):
    start_byte = start
    end_byte = end
    print(start,end)
    headers['range']= 'bytes=%d-%d'%(start_byte,end_byte)
    print(headers)

    response = requests.request("GET", url, headers=headers)
    #large = response.headers['Content-Range'].split('/')[-1]
    #print(response.text)

    print(response.status_code)
    with open('%s/test.mp4'%(root),'ab') as f:
        f.write(response.content)
        f.close()

for range in ret:
    start = range.split('-')[0]
    end = range.split('-')[1]
    fun(int(start),int(end))


