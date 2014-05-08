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
        
        response = urllib2.urlopen('http://a.m.taobao.com/i' + itemid + '.htm')
        rurl = response.url
        if rurl.find("cloud-jump") > -1 or rurl.find("h5.m"):
            return TaobaoExtractor.fetch_redirect(itemid)
        shoptype = "taobao.com"
        if response.url.find("tmall") >= 0:
            shoptype = "tmall.com"


        html = response.read()

        soup = BeautifulSoup(html)
        linktag = soup.select("html body div.bd div.left-margin-5 p strong a")
        shoplink = ""
        if len(linktag) > 0:
            shoplink = linktag[0]["href"]
            shoplink = shoplink.replace(".m.t", ".t")

        
        imgs = soup.select("html body img")
        
        desc = soup.title.string[0 : -9]

        cattag = soup.p
        if cattag == None:
            #print "已经下架"
            return None
        
        atag = cattag.findChildren('a')
        cidtag = atag[-1]
        cidurl = cidtag.attrs['href']
        cid = int(re.findall(r'\d+$', cidurl)[0])
        firstcat = atag[1].text
        secondcat = cidtag.text

        category = [firstcat, secondcat]

        details = soup.find_all('div', { 'class' : 'detail' })
            
        imgurls = []      
        imgtag = details[0]
        src = imgtag.img['src']
        src = re.sub('_\d+x\d+\.jpg|_b.jpg', '', src)
        imgurls.append(src)
             
            
        tables = soup.find_all('table')
        imgtable = tables[1]
        imgtags = imgtable.findChildren('img')
        for tag in imgtags:
            imgurl = tag['src']
            #imgurl = imgurl.replace('_70x70.jpg','')
            imgurl = re.sub(TaobaoExtractor.IMG_POSTFIX, '', imgurl)
            imgurls.append(imgurl)

                
        detail = details[1]
        judge = re.findall(ur'格：', detail.p.text)
        hasprom = True #默认都有促销
        secondhand = False #二手商品情况处理
        if len(judge) > 0:
            hasprom = False
        else:
            judge = re.findall(ur'价', detail.p.text)
            if len(judge) > 0:
                secondhand = True
        
        promprice = 0
        if hasprom:
            prom = detail.p.strong
            if prom != None:
                tmp = re.findall("\d+.\d+", prom.text)
                if len(tmp) > 0:
                    promprice = float(tmp[0])
                

        p = detail.findChildren('p')
        startindex = 1
        
        if hasprom == False:
            startindex = 0
        pricetag = p[startindex].text
        price = 0
        if pricetag != None:
            price = re.findall(r'\d+\.\d+', pricetag)
            if len(price) > 0:
                price = float(price[0])

        counttag = p[startindex+2].text
        tmp = re.findall(r'\d+', counttag)
        salecount = 0
        if len(tmp) > 0:
            salecount = int(tmp[0])


        loctag = p[startindex + 3].text
        location = ''
        if loctag.find(u'地') > 0:
            location = loctag.split(u'：')[1]


        #reviewtag = soup.findChildren('td', 'link_btn fix_btn')[1]
        #reviews = 0
        #if secondhand:
        #    rew = re.findall(r'\d+', reviewtag.a.text)
        #    if len(rew) > 0:
        #        reviews = int(rew[0])
        #else:
        #    rew = re.findall(r'\d+', reviewtag.a.span.text)
        #    if len(rew) > 0:
        #        reviews = int(rew[0])
        nick = '' 
        for nametag in soup.select('body div.bd div.box div.detail p a img'):
            try:
                nameurl = nametag['src']
                o = urlparse(nameurl)
                nick = parse_qs(str(o.query))['nick'][0]
                break
            except:
                pass
        if promprice > 0:
            price = promprice
        result = {
            "desc" : desc,
            "cid" : cid,
            "promprice" : promprice, #促销价格
            "price" : price ,
            "category" : category,
            "imgs" : imgurls,
            "count" : salecount,
            "location" : location,
            "nick" : nick,
            "shop_link" : shoplink
            #"sellerid":sellerid,
            #"shoptype":shoptype
        } 
        return result


    @staticmethod
    def fetch_shop(shoplink):
        if shoplink.find(".m.") >= 0:
            shoplink = shoplink.replace(".m.", ".", 1)
        resp = urllib2.urlopen(shoplink)
        if resp.code != 200:
            return None
        fontpage = resp.read()
        sellerid = 0
        sells = re.findall("(userId|userid|sellerid|sellerId)=(\d+)", fontpage)
        if len(sells)>0:
            sellerid = sells[0][1]
        else:
            sells = re.findall("userId:('|\")(\d+)('|\")",fontpage)
            if len(sells)>0:
                sellerid = sells[0][2]
        shoptype = "taobao.com"
        print sellerid
        if shoplink.find("tmall") >= 0:
            shoptype = "tmall.com"

        soup = BeautifulSoup(fontpage)
        title = soup.select("a.J_TGoldlog")[0].text[:-4]
        nick = soup.select("a.seller-name")[0].text[3:]
        shopidtag = soup.select("a.J_TCollectShop")[1].attrs['data-init']
        o = urlparse(shopidtag)
        shopid = parse_qs(str(o.query))['shopId'][0]
        '''
        #读取wap店铺首页获取店名和
        shoplink = shoplink.replace(".t",".m.t",1)
        resp = urllib2.urlopen(shoplink)
        if resp.code != 200:
            return None
        html = resp.read()
        shopids = re.findall("shop_id=(\d+)", html)
        shopid = 0
        if len(shopids) > 0:
            shopid = int(shopids[0])
        soup = BeautifulSoup(html)
        title = soup.title.getText()
        i = title.find(" - ")
        title = title[0:i]
        img = soup.findChild("td", attrs = { "class" : "pic" }).img 
        if img == None:
            return None
        shoppic = img.attrs["src"]
        shoppic = re.sub(TaobaoExtractor.IMG_POSTFIX, "", shoppic, 1)
        nicktag = soup.select("html body div.bd div.box div.detail a img")[-1]
        src = nicktag.attrs["src"]
        o = urlparse(src)
        nick = parse_qs(str(o.query))['nick'][0]
        '''
        result = {
            "type" : shoptype,
            "seller_id" : sellerid,
            "shop_id" : shopid,
            "title" : title,
            "pic" : '',
            "nick" : nick
        }
        return result


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
        nick = unquote(f.headers.get('At_Nick'))
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
        fimg = soup.select("img#J_ImgBooth")
        if len(fimg) == 0:
            #print 'pic is none'
            return None 
        fjpg = fimg[0].attrs['data-src']
        fjpg = re.sub(TaobaoExtractor.IMG_POSTFIX,"",fjpg)
        #print fjpg
        imgs.append(fjpg)
        
        optimgs = soup.select("ul#J_UlThumb li div a img")
        for op in optimgs:
            op = re.sub(TaobaoExtractor.IMG_POSTFIX,"",op.attrs["data-src"])
            #print op
            if op in imgs:
                continue
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
            #print 'pic is none'
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
            #print 'shopid is none'
            return None
        sl = soup.select("span.slogo a")
        shoplink = "http://shop"+shopidtag[0]+".taobao.com"
        if len(sl) > 0 :
            shoplink = sl[0].attrs['href']
        pricetag = soup.select("strong.J_originalPrice")
        if len(pricetag) == 0:
            #print 'no price'
            return None
        pr = pricetag[0].string
        ps = re.findall("\d+\.\d+",pr)
        if len(ps) == 0:
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
    print TaobaoExtractor.fetch_item("25558776712")
    print TaobaoExtractor.fetch_shop("http://shop110165889.taobao.com/?spm=2013.1.0.0.uSTb9g")

