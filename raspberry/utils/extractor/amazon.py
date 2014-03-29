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

        soup = BeautifulSoup(html)

        title = soup.title.string
        ti = title.rindex('-')
        title = title[:ti]

        p = soup.select("b.priceLarge")
        ptag = p[0]
        ptag = ptag.string
        price = re.findall(r'\d+\.\d+',ptag)[0]

        price = float(price)

        imgtags = soup.select('div#thumb-strip div.thumb img')
        imgs = []

        for tag in imgtags:
            src = tag.attrs['src']
            i = src.index("._")
            x = src.index("_.")
            link = src[:i]
            suffix = src[x+1:]
            imgs.append(link+suffix)
        brand = soup.select("form#handleBuy div.buying span a")[0].string
        merchanID = soup.select("input#merchantID")[0].attrs['value']
        nick = ''
        shop_link = ''
        if merchanID == 'A1AJ19PSB66TGU':
            nick = "亚马逊"
            shop_link = "http://z.cn"
        else:
            shop_link = "http://www.amazon.cn/gp/browse.html?ie=UTF8&me=%s"%merchanID
            nick = soup.select("div#BBAvailPlusMerchID b")[0].string

        cats = soup.select("span.zg_hrsr_ladder")[0]
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


if __name__=="__main__":
    a = AmazonExtractor()
    r = a.fetch_item("http://www.amazon.cn/%E9%9C%8D%E6%AF%94%E7%89%B9%E4%BA%BA-J-R-R%E2%80%A2%E6%89%98%E5%B0%94%E9%87%91/dp/B00AF3T0Y4/ref=sr_1_1?s=books&ie=UTF8&qid=1394016796&sr=1-1&keywords=%E9%9C%8D%E6%AF%94%E7%89%B9")
    print r['desc']
    print r['price']
    print r['category'][1]
    print r['nick']
    print r['shop_link']
    print r['brand']

