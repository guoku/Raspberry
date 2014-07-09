#encoding=utf8

import urllib2
import cookielib
from bs4 import BeautifulSoup
import re
from urlparse import parse_qs, urlparse
from urllib import unquote

class TaobaoExtractor:
    
    IMG_POSTFIX = "_\d+x\d+.*\.jpg|_b\.jpg"

    @staticmethod
    def fetch_item(itemid):
        return TaobaoExtractor.fetch_redirect(itemid)

    @staticmethod
    def fetch_redirect(itemid):
        result = TaobaoExtractor.fetch_taobao_web(itemid)
        if result == None:
            return TaobaoExtractor.fetch_tmall_web(itemid)
        return result



    @staticmethod
    def fetch_taobao_web(itemid):

        #目前只针对普通淘宝店电脑版，天猫店暂时不能处理
        cookie = cookielib.CookieJar()
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
        urllib2.install_opener(opener)
        opener.addheaders.append(('Cookie','cna=I2H3CtFnDlgCAbRP3eN/4Ujy; t=2609558ec16b631c4a25eae0aad3e2dc; w_sec_step=step_login; x=e%3D1%26p%3D*%26s%3D0%26c%3D0%26f%3D0%26g%3D0%26t%3D0%26__ll%3D-1%26_ato%3D0; lzstat_uv=26261492702291067296|2341454@2511607@2938535@2581747@3284827@2581759@2938538@2817407@2879138@3010391; tg=0; _cc_=URm48syIZQ%3D%3D; tracknick=; uc3=nk2=&id2=&lg2=; __utma=6906807.613088467.1388062461.1388062461.1388062461.1; __utmz=6906807.1388062461.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); mt=ci=0_0&cyk=0_0; _m_h5_tk=6457881dd2bbeba22fc0b9d54ec0f4d9_1389601777274; _m_h5_tk_enc=3c432a80ff4e2f677c6e7b8ee62bdb48; _tb_token_=uHyzMrqWeUaM; cookie2=3f01e7e62c8f3a311a6f83fb1b3456ee; wud=wud; lzstat_ss=2446520129_1_1389711010_2581747|2258142779_0_1389706922_2938535|1182737663_4_1389706953_3284827|942709971_0_1389706966_2938538|2696785043_0_1389707052_2817407|50754089_2_1389707124_2879138|2574845227_1_1389707111_3010391|377674404_1_1389711010_2581759; linezing_session=3lJ2NagSIjQvEYbpCk5o8clc_1389693042774lS4I_5; swfstore=254259; whl=-1%260%260%261389692419141; ck1=; uc1=cookie14=UoLU4ni6x8i9JA%3D%3D; v=0'))

        f = opener.open('http://item.taobao.com/item.htm?id='+itemid)
        at_nick = f.headers.get('At_Nick')
        if at_nick is None:
            return None
        nick = unquote(at_nick)
        html = f.read()
        cidre = re.findall(" cid:'\d+'",html)
        if len(cidre)== 0:
            return None
        cidr = re.findall('\d+',cidre[0])
        cid = int(cidr[0])
        soup = BeautifulSoup(html)
        desc = soup.title.string[0:-4]
        ptag = soup.select("div.tb-wrap-newshop ul li strong em.tb-rmb-num")
        if len(ptag) == 0:
            #print 'pic is none'
            return None 
        pr = ptag[0].string
        ps = re.findall("\d+\.\d+",pr)
        if len(ps) == 0:
            return None

        price = float(ps[0])
        imgs = []
        optimgs = soup.select("ul#J_UlThumb li img")
        for op in optimgs:
            link = op.attrs['data-src']
            op = re.sub(TaobaoExtractor.IMG_POSTFIX,"",link)
            imgs.append(op)
        shopidtag = re.findall('shopId:"(\d+)',html)
        if len(shopidtag) == 0:
            #print 'shopid is none'
            return None
        shoplink = "http://shop"+shopidtag[0]+".taobao.com"
        result = {
            "desc" : desc,
            "cid" : cid,
            "promprice" : price,
            "price" : price,
            "category" : "",
            "imgs" : imgs,
            "count" : 0,
            "reviews" : 0,
            "nick" : nick,
            "shop_link" : shoplink,
            "location" : ""
            }
        return result



    @staticmethod
    def fetch_tmall_web(itemid):
        cookie=cookielib.CookieJar()
        opener=urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
        urllib2.install_opener(opener)
        opener.addheaders.append(('Cookie','cna=I2H3CtFnDlgCAbRP3eN/4Ujy; t=2609558ec16b631c4a25eae0aad3e2dc; w_sec_step=step_login; x=e%3D1%26p%3D*%26s%3D0%26c%3D0%26f%3D0%26g%3D0%26t%3D0%26__ll%3D-1%26_ato%3D0; lzstat_uv=26261492702291067296|2341454@2511607@2938535@2581747@3284827@2581759@2938538@2817407@2879138@3010391; tg=0; _cc_=URm48syIZQ%3D%3D; tracknick=; uc3=nk2=&id2=&lg2=; __utma=6906807.613088467.1388062461.1388062461.1388062461.1; __utmz=6906807.1388062461.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); mt=ci=0_0&cyk=0_0; _m_h5_tk=6457881dd2bbeba22fc0b9d54ec0f4d9_1389601777274; _m_h5_tk_enc=3c432a80ff4e2f677c6e7b8ee62bdb48; _tb_token_=uHyzMrqWeUaM; cookie2=3f01e7e62c8f3a311a6f83fb1b3456ee; wud=wud; lzstat_ss=2446520129_1_1389711010_2581747|2258142779_0_1389706922_2938535|1182737663_4_1389706953_3284827|942709971_0_1389706966_2938538|2696785043_0_1389707052_2817407|50754089_2_1389707124_2879138|2574845227_1_1389707111_3010391|377674404_1_1389711010_2581759; linezing_session=3lJ2NagSIjQvEYbpCk5o8clc_1389693042774lS4I_5; swfstore=254259; whl=-1%260%260%261389692419141; ck1=; uc1=cookie14=UoLU4ni6x8i9JA%3D%3D; v=0'))

        f = opener.open("http://detail.tmall.com/item.htm?id="+itemid)
        cat = f.headers.get('X-Category')
        cid = int(cat[5:])
        nick = unquote(f.headers.get('At_Nick'))
        nick = unquote(nick)
        html = f.read()
        soup = BeautifulSoup(html)
        desc = soup.title.string[0:-12]
        imgs = []
        fimg = soup.select("img#J_ImgBooth")
        if len(fimg) == 0:
            print 'pic is none'
            return None 
        fjpg = fimg[0].attrs['src']
        fjpg = re.sub(TaobaoExtractor.IMG_POSTFIX,"",fjpg)
        #print fjpg
        imgs.append(fjpg)
        optimgs = soup.select("ul#J_UlThumb li a img")
        for op in optimgs:
            op = re.sub(TaobaoExtractor.IMG_POSTFIX,"",op.attrs["src"])
            if op in imgs:
                continue
            imgs.append(op)
        shopidtag = re.findall('shopId:"(\d+)',html)
        if len(shopidtag) == 0:
            print 'shopid is none'
            return None
        sl = soup.select("span.slogo a")
        shoplink = "http://shop"+shopidtag[0]+".taobao.com"
        if len(sl) > 0 :
            shoplink = sl[0].attrs['href']
        pricetag = soup.select("span.originPrice")
        if len(pricetag) == 0:
            print 'no price'
            return None
        pr = pricetag[0].string
        ps = re.findall("\d+\.\d+",pr)
        if len(ps) == 0:
            print "pic len is 0"
            return None
        price = float(ps[0])
        result = {
            "desc" : desc,
            "cid" : cid,
            "promprice" : price,
            "price" : price,
            "category" : "",
            "imgs" : imgs,
            "count" : 0,
            "reviews" : 0,
            "nick" : nick,
            "shop_link" : shoplink,
            "location" : ""
                }
        return result


if __name__=="__main__":
    print TaobaoExtractor.fetch_item("39681973010")
    #print TaobaoExtractor.fetch_shop("http://shop110165889.taobao.com/?spm=2013.1.0.0.uSTb9g")

