#encoding=utf8


import urllib2 
from bs4 import BeautifulSoup 
import re 
import json 

class AmazonExtractor:

    @staticmethod
    def fetch_item(item_link):

        resp = urllib2.urlopen(item_link)

        html = resp.read()
        
        return AmazonExtractor.parser(html)


    @staticmethod
    def parser( html):
        try:
            soup = BeautifulSoup(html)
            title = soup.select("span#productTitle")[0].string
            p = soup.select("#priceblock_ourprice")
            ptag = p[0]
            ptag = ptag.string
            price = re.findall(r'\d+\.\d+',ptag)[0]

            price = float(price)

            imgtags = soup.select('li span span.a-button-text img')
            imgs = []

            for tag in imgtags:
                src = tag.attrs['src']
                imgs.append(src)
            brand = soup.select("a#brand")[0].string
            merchanID = soup.select("input#merchantID")[0].attrs['value']
            nick = "亚马逊"
            shop_link = "http://amazon.com"

            cats = soup.select("span.zg_hrsr_ladder")
            if len(cats) == 0:
                category = []
            else:
                cats = cats.select('a')
                category = []
                for c in cats:
                    category.append(c.string)

            result = {
                "desc":title,
                "price":price,
                "category":category,
                "imgs":imgs,
                "nick":nick,
                "shop_link":shop_link,
                "brand":brand
            }
            return result
        except:
            return AmazonExtractor.cparser(html) 

    @staticmethod
    def cparser( html):
        #合约机页面解析
        soup = BeautifulSoup(html)
        title = soup.select("span#btAsinTitle")[0].string
        pricetag = soup.select("span#current-price")[0].string
        price = float(re.findall("\d+\.+\d+", pricetag)[-1])
        brand = soup.select("span#amsPopoverTrigger a")[0].string
        imgs = [soup.select("img#prodImage")[0]['src']]
        category = []
        result = {
            "desc":title,
            "price" : price,
            "category" : category,
            "imgs" : imgs,
            "nick":"亚马逊",
            "shop_link":"http://amazon.com",
            "brand" : brand
        }
        return result

if __name__=="__main__":
    a = AmazonExtractor()
    r = a.fetch_item("http://www.amazon.com/HTC-One-M7-Silver-32GB/dp/B00E6FII18/ref=pd_sim_cps_2?ie=UTF8&refRID=018T0RQ3SW73ABKJDCNV")
    print r['desc']
    print r['price']
    print r['category']
    print r['nick']
    print r['shop_link']
    print r['brand']
    print r['imgs']

