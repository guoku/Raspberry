#encoding=utf8


import urllib2 
from bs4 import BeautifulSoup 
import re 
import json 

class AmazonCNExtractor:

    @staticmethod
    def fetch_item(item_link):

        resp = urllib2.urlopen(item_link)

        html = resp.read()
        
        return AmazonExtractor.parser(html)


    @staticmethod
    def parser( html):

        soup = BeautifulSoup(html)
        title = soup.select("#btAsinTitle span")[0].string
        title = title.strip()
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
    a = AmazonCNExtractor()
    r = a.fetch_item("http://www.amazon.cn/%E5%86%A0%E7%9B%8A%E5%90%8DGYM-%E6%96%B0%E5%9E%8B%E7%94%B5%E8%84%91%E6%A4%85-%E5%AE%B6%E7%94%A8%E7%94%B5%E8%84%91%E6%A4%85%E5%AD%90-%E4%B8%93%E5%88%A9%E5%8A%9E%E5%85%AC%E6%A4%85-%E9%BB%91%E8%89%B2-88333/dp/B00J7HTQWK/ref=sr_1_2?m=A1AJ19PSB66TGU&s=home-garden&ie=UTF8&qid=1397709461&sr=1-2")
    print r['desc']
    print r['price']
    print r['category'][1]
    print r['nick']
    print r['shop_link']
    print r['brand']

