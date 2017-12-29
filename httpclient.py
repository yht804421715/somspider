import http.client

conn = http.client.HTTPConnection("vs27.thisav.com")

headers = {
    'accept': "*/*",
    'accept-encoding': "gzip, deflate",
    'accept-language': "zh-CN,zh;q=0.9",
    'host': "vs27.thisav.com",
    'if-range': "\"59f444d9-285e7679\"",
    'origin': "http://www.thisav.com",
    'proxy-connection': "keep-alive",
    'range': "bytes=341945-834335",
    'referer': "http://www.thisav.com/video/244761/%E7%9C%9F%E6%AD%A3%E5%BC%B7%E5%A7%A6%E6%98%AF%E5%90%88%E6%B3%95%E7%9A%84%E5%A4%A7%E5%A4%A7%E5%8A%9B%E5%81%9A%E6%84%9B%E5%AD%B8%E7%94%9F.html",
    'user-agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36",
    'cache-control': "no-cache",
    'postman-token': "417c5653-c299-a983-50c1-c8588c613a26"
    }

conn.request("GET", "/dash/kn5uF0fhGHVwOAyOGD39-Q,1514465253/244761_dashinit.mp4", headers=headers)

res = conn.getresponse()

print(res.headers)