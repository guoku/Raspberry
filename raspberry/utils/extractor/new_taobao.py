#encoding=utf8

import urllib2
import cookielib
from bs4 import BeautifulSoup
import re
from urlparse import parse_qs, urlparse
from urllib import unquote
from django.utils.log import getLogger


IMG_POSTFIX = "_\d+x\d+.*\.jpg|_b\.jpg"
log = getLogger('django')



class TaoBao():
    cookie = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
    urllib2.install_opener(opener)
    opener.addheaders.append(('Cookie','cna=I2H3CtFnDlgCAbRP3eN/4Ujy; t=2609558ec16b631c4a25eae0aad3e2dc; w_sec_step=step_login; x=e%3D1%26p%3D*%26s%3D0%26c%3D0%26f%3D0%26g%3D0%26t%3D0%26__ll%3D-1%26_ato%3D0; lzstat_uv=26261492702291067296|2341454@2511607@2938535@2581747@3284827@2581759@2938538@2817407@2879138@3010391; tg=0; _cc_=URm48syIZQ%3D%3D; tracknick=; uc3=nk2=&id2=&lg2=; __utma=6906807.613088467.1388062461.1388062461.1388062461.1; __utmz=6906807.1388062461.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); mt=ci=0_0&cyk=0_0; _m_h5_tk=6457881dd2bbeba22fc0b9d54ec0f4d9_1389601777274; _m_h5_tk_enc=3c432a80ff4e2f677c6e7b8ee62bdb48; _tb_token_=uHyzMrqWeUaM; cookie2=3f01e7e62c8f3a311a6f83fb1b3456ee; wud=wud; lzstat_ss=2446520129_1_1389711010_2581747|2258142779_0_1389706922_2938535|1182737663_4_1389706953_3284827|942709971_0_1389706966_2938538|2696785043_0_1389707052_2817407|50754089_2_1389707124_2879138|2574845227_1_1389707111_3010391|377674404_1_1389711010_2581759; linezing_session=3lJ2NagSIjQvEYbpCk5o8clc_1389693042774lS4I_5; swfstore=254259; whl=-1%260%260%261389692419141; ck1=; uc1=cookie14=UoLU4ni6x8i9JA%3D%3D; v=0'))

    # images = list()

    def __init__(self, item_id):
        self.item_id = item_id
        self.html = self.fetch_html()
        self.soup = BeautifulSoup(self.html, from_encoding="gb18030")
        if len(self.soup.findAll("body")) == 0:
            # print "OKOKOKO"
            self.html = self.fetch_html_ny()
            print self.html
            self.soup = BeautifulSoup(self.html)
            # print self.soup



    @property
    def headers(self):
        return self._headers

    @property
    def nick(self):

        self._nick = self._headers.get('at_nick')
        if not self._nick:
            return ""
        return unquote(self._nick)

    @property
    def cid(self):
        cat = self.headers.get('X-Category')
        try:
            _cid = cat.split('/')
            return _cid[-1]
        except AttributeError, e:
            log.error("Error: %s", e.message)
        return 0


    @property
    def desc(self):
        return self.soup.title.string[0:-4]


    @property
    def price(self):
        ptag = self.get_ptag()

        if ptag:
            pr = ptag[0].string
            ps = re.findall("\d+\.\d+",pr)
            return float(ps[0])


    @property
    def images(self):
        _images = list()
        fimg = self.soup.select("#J_ImgBooth")

        fjpg = fimg[0].attrs.get('data-src')
        if not fjpg:
            fjpg = fimg[0].attrs.get('src')

        fjpg = re.sub(IMG_POSTFIX, "", fjpg)

        _images.append(fjpg)

        optimgs = self.soup.select("ul#J_UlThumb li a img")

        for op in optimgs:
            try:
                optimg = re.sub(IMG_POSTFIX, "", op.attrs.get('src'))
            except TypeError, e:
                optimg = re.sub(IMG_POSTFIX, "", op.attrs.get('data-src'))
            if optimg in _images:
                continue
            _images.append(optimg)

        return _images

    @property
    def shoplink(self):
        shopidtag = re.findall('shopId:"(\d+)', self.html)

        if len(shopidtag) > 0:
            shoplink = "http://shop"+shopidtag[0]+".taobao.com"
            return shoplink
        return "http://chaoshi.tmall.com/"

    def get_ptag(self):
        ptag = self.soup.select("div.tb-wrap ul li strong em.tb-rmb-num")
        if len(ptag) > 0:
            return ptag
        ptag = self.soup.select("span.originPrice")
        if len(ptag) > 0:
            return ptag

        return None

    def fetch_html(self):
        try:
            f = self.opener.open('http://item.taobao.com/item.htm?id=%s' % self.item_id)
        except Exception, e:
            raise

        self._headers = f.headers
        return f.read()

    def fetch_html_ny(self):
        try:
            f= self.opener.open("http://item.ny.taobao.com/item.htm?id=%s" % self.item_id)
        except Exception, e:
            log.error(e.message)
            raise
        self._headers = f.headers
        return f.read()

    def res(self):
        result = {
			"desc": self.desc,
			"cid": self.cid,
			"promprice" : self.price,
            "price": self.price,
			"category" : "",
			"imgs": self.images,
			"count": 0,
			"reviews": 0,
			"nick": self.nick,
			"shop_link": self.shoplink,
			"location": "",
        }
        return result



if __name__=="__main__":
    # t = TaoBao("9960937204")
    # t = TaoBao("39523724233")
    # print t.soup.select("img#J_ImgBooth")
    t = TaoBao("40869142654")
    # print t.soup.findAll('body')
    print t.res()
    # print t.nick
    # print t.cid
    # print t.price
    # print t.desc
    # print t.images
    # print t.shoplink











