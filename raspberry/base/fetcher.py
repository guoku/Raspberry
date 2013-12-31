#encoding=utf-8

import urllib2
from bs4 import BeautifulSoup
import re
from urlparse import parse_qs
from urlparse import urlparse


def fetch(itemid):
    
    response = urllib2.urlopen('http://a.m.taobao.com/i'+itemid+'.htm')
    html = response.read()

    soup = BeautifulSoup(html)
    
    desc = soup.title.string[0:-9]

    cattag = soup.p
    if cattag==None:
        print "已经下架"
        return None
    atag = cattag.findChildren('a')
    cidtag = atag[-1]
    cidurl = cidtag.attrs['href']
    cid = int(re.findall(r'\d+$',cidurl)[0])
    firstcat = atag[1].text
    secondcat = cidtag.text

    category = [firstcat,secondcat]

    details = soup.find_all('div', { 'class' : 'detail' })
        
    imgurls = []      
    imgtag = details[0]
    src = imgtag.img['src']
    src = re.sub('_\d+x\d+\.jpg','',src)
    imgurls.append(src)
         
        
    tables = soup.find_all('table')
    imgtable = tables[1]
    imgtags = imgtable.findChildren('img')
    for tag in imgtags:
        imgurl = tag['src']
        #imgurl = imgurl.replace('_70x70.jpg','')
        imgurl = re.sub('_\d+x\d+\.jpg|_b.jpg','',imgurl)
        imgurls.append(imgurl)

            
    detail = details[1]
    judge = re.findall(ur'格：',detail.p.text)
    hasprom = True #默认都有促销
    secondhand = False #二手商品情况处理
    if len(judge)>0:
        hasprom = False
    else:
        judge = re.findall(ur'价',detail.p.text)
        if len(judge)>0:
            secondhand = True
    promprice = 0
    if hasprom:
        prom = detail.p.strong
        if prom != None:
            tmp = re.findall("\d+.\d+",prom.text)
            if len(tmp)>0:
                promprice = float(tmp[0])
            

    p = detail.findChildren('p')
    startindex = 1
    
    if hasprom==False:
        startindex = 0
    pricetag = p[startindex].text
    price = 0
    if pricetag!=None:
        price =re.findall(r'\d+\.\d+',pricetag)
        if len(price)>0:
            price = float(price[0])

    counttag = p[startindex+2].text
    tmp = re.findall(r'\d+',counttag)
    salecount = 0
    if len(tmp)>0:
        salecount = int(tmp[0])


    loctag = p[startindex+3].text
    location = ''
    if loctag.find(u'地')>0:
        location = loctag.split(u'：')[1]

    reviewtag = soup.findChildren('td','link_btn fix_btn')[1]
    reviews = 0
    if secondhand:
        rew = re.findall(r'\d+',reviewtag.a.text)
        if len(rew)>0:
            reviews = int(rew[0])
    else:
        rew = re.findall(r'\d+',reviewtag.a.span.text)
        if len(rew)>0:
            reviews = int(rew[0])
    nick = '' 
    for nametag in soup.select('body div.bd div.box div.detail p a img'):
        try:
            nameurl = nametag['src']
            o = urlparse(nameurl)
            nick = parse_qs(o.query)['nick'][0]
            nick= nick
            break
        except:
            pass
    result = {
            "desc":desc,
            "cid":cid,
            "promprice":promprice , #促销价格
            "price":price ,
            "category":category,
            "imgs":imgurls,
            "count":salecount,
            "location":location,
            "reviews":reviews,
            "nick":nick
            } 
    return result

if __name__=='__main__':
    fetch("35593268923")


