#encoding=utf8

import urllib2 
from bs4 import BeautifulSoup
import re 
import json
class JD:
    def fetch_item(self, itemid):
        link = ""
        self.itemid = itemid
        if type(itemid) == int:
            link = "http://item.jd.com/%d.html"%itemid
        else:
            link = "http://item.jd.com/%s.html"%itemid
        resp = urllib2.urlopen(link)
        
        html = resp.read()
        html = html.decode("gbk").encode("utf8")

        return self.parser(html,itemid)

    def parser(self, html, itemid):
        soup = BeautifulSoup(html)

        title = soup.title.string
        title = title[:-18]
        
        imgtags = soup.select("html body div.w div#product-intro \
                div#preview div#spec-list div.spec-items ul li img")
        imgs = []

        for tag in imgtags:
            src = tag['src']
            src = src.replace('com/n5','com/n1')
            imgs.append(src)
        
        cattag = soup.select("html body div.w div.breadcrumb span a")[1]
        catlink = cattag.attrs['href']
        catstr = re.findall(r'\d+',catlink)
        category = [int(x) for x in catstr]

        tmp = re.findall(r'店铺.*>(.+)</a>',html)
        nick = ""
        shop_link = ""
        if len(tmp)>0:
            nick = tmp[0]
            link = re.findall(r'店铺.* href="(.+)">',html)[0]
            shop_link = link[:-16]
        else:
            nick="京东"
            shop_link = "http://jd.com"
        itemid = int(itemid)
        price_link = "http://p.3.cn/prices/get?skuid=J_%d&type=1&area=1_72_4137&callback=cnp"%itemid
        resp = urllib2.urlopen(price_link)
        data = resp.read()
        data = data[5:-4]
        pj = json.loads(data)
        price = float(pj['p'])

        result = {
            "desc":title,
            "price":price,
            "category":category,
            "imgs":imgs,
            "nick":nick,
            "shop_link":shop_link
        }

        return result


if __name__ == '__main__':
    jd = JD()
    result = jd.fetch_item(1069437177)
    print result
