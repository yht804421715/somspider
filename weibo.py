import  requests
from bs4 import  BeautifulSoup
import re
import os
import  time
import  json
from multiprocessing.pool import  Pool



class weibo:
    rootPath = 'C:/weibo/'
    header = {
    'Host':'m.weibo.cn',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:53.0) Gecko/20100101 Firefox/53.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0'
    }

    uid = 0
    count = 1
    #uid = 3150828683#微博用户标识
    containerid = None
    onlyself = False

    @classmethod
    def start(cls,uid):
        cls.uid = uid
        page = 1
        containerid = cls.setContainerId()
        if not os.path.exists(cls.rootPath+'list'):
            f = open(cls.rootPath + 'list', 'w+')
        max_page = cls.setMaxPage(cls.uid,containerid)
        mp = Pool(processes=8)

        data = []
        for i in range(1,max_page):
            data.append([uid,containerid,cls.rootPath,i])
        mp.map(cls.parserPage,data)




    @classmethod
    def setContainerId(cls):
        start_url = 'https://m.weibo.cn/api/container/getIndex?type=uid&value=' + str(cls.uid)
        start_r = requests.get(start_url, headers=cls.header)
        print(start_url)
        js = json.loads(start_r.text)['data']
        name = js['userInfo']['screen_name']  # 获取微博名称
        cls.rootPath = cls.rootPath + name + '/'  # 切换目录
        if not os.path.exists(cls.rootPath[:-1]):
            os.makedirs(cls.rootPath[:-1])
        weibo_tab = js['tabsInfo']['tabs'][1]
        cls.containerid = weibo_tab['containerid']
        return cls.containerid

    @classmethod
    def setMaxPage(cls,uid,containerid):
        weibo_url = 'https://m.weibo.cn/api/container/getIndex?' \
                    'uid=' + str(uid) + \
                    '&luicode=10000011' \
                    '&lfid=100505' + str(uid) + '&type=uid&value=' + str(uid) + '&containerid=' + str(
            containerid) + '&page=' + str(1)
        weibo_r = requests.get(weibo_url, headers=cls.header, timeout=10)
        js = json.loads((weibo_r.text))['data']
        max_page = int(js['cardlistInfo']['total'] / 10) + 1
        return max_page

    @classmethod
    def isSpidered(cls,rootPath,url):

        f = open(rootPath+'list','r')
        f.seek(0)
        for  read in f.readlines():
            if read == url +'\n':
                f.close()
                return  True
        f.close()
        return False

    @classmethod
    def Download(cls,rootPath,urls = [],count = 0):
        pic_header = {
    'authority':'ww4.sinaimg.cn',
    'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'accept-encoding':'gzip, deflate, sdch, br'
    }

        if len(urls) == 0:
            return
        for url in urls:
            print(url)
            name = url[-13:]
            if not os.path.exists(cls.rootPath+name):
                #hpath = re.search(r'https://ww2.sinaimg.cn(.*)',url).groups()[0]
                #pic_header[':path']= hpath
                pic_r = requests.get(url,headers = pic_header)
                f = open(rootPath+name,'ab+')
                f.write(pic_r.content)
                count  = count + 1
                f.close()
                print('图片'+str(count-1))

    @classmethod
    def parserPage(cls,data):
        uid = data[0]
        containerid = data[1]
        rootPath = data[2]
        page = data[-1]
        weibo_url = 'https://m.weibo.cn/api/container/getIndex?' \
                    'uid=' + str(uid) + \
                    '&luicode=10000011' \
                    '&lfid=100505' + str(uid) + '&type=uid&value=' + str(uid) + '&containerid=' + str(
            containerid) + '&page=' + str(page)

        if cls.isSpidered(rootPath,weibo_url):
            print('爬取过该页')
            return

        weibo_r = requests.get(weibo_url, headers=cls.header, timeout=10)
        js = json.loads((weibo_r.text))['data']
        pic_url = []
        weibo_cards = js['cards']

        for card in weibo_cards:
            if 'mblog' not in card:
                continue
            blog = card['mblog']
            pics = blog.get('pics', None)
            retwteeted = blog.get('retweeted_status', None)
            if cls.onlyself and retwteeted is None:
                continue
            if pics is not None:
                for pic in pics:
                    pic_url.append(pic['large']['url'])
        # 下载图片
        # print(pic_url)

        cls.Download(rootPath,pic_url, cls.count)

        f = open(rootPath + 'list', 'a+')
        f.write(weibo_url + '\n')
        f.close()

        print('page =%d' % page)






if __name__ == '__main__':
    uid = input('input uid: ')
    weibo.start(uid)