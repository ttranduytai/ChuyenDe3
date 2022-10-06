import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from nhandan.items import NhandanItem
import re
from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods.posts import GetPosts, NewPost
from wordpress_xmlrpc.methods.users import GetUserInfo
from wordpress_xmlrpc.methods import media, posts
from wordpress_xmlrpc.compat import xmlrpc_client
import collections
collections.Iterable = collections.abc.Iterable
import urllib
import os
import requests
import shutil
from PIL import Image
from os.path import splitext
#wp = Client('http://localhost/wordpress/xmlrpc.php', 'tranduytai', 'BB9u koSA raeJ Es0D pijt OUWO')
wp = Client('http://nhandanqb.cf/xmlrpc.php', 'tranduytai', 'XTRW CLXS Pjpq sxgb u4Or Md4q')
wp.call(GetPosts())
wp.call(GetUserInfo())

def listToString(s):
    str1 = ""
    for ele in s:
        str1 += ele
    return str1

def strip_value(value):
    m = re.search("http[^\s]+(\s)*h?(http[^\s>]+)(\s)*", value)
    if m:
        return m.group(2)
    else:
        return value

class NhandanSpider(CrawlSpider):
    name = "nhandan"
    allowed_domains = ['nhandan.vn']
    start_urls = [
            'https://nhandan.vn/chinhtri/',
            'https://nhandan.vn/kinhte/',
            'https://nhandan.vn/vanhoa/',
            'https://nhandan.vn/xahoi/',
            'https://nhandan.vn/phapluat/',
            'https://nhandan.vn/du-lich/',
            'https://nhandan.vn/thegioi/',
            'https://nhandan.vn/thethao/',
            'https://nhandan.vn/giaoduc/',
            'https://nhandan.vn/y-te/',
            'https://nhandan.vn/khoahoc-congnghe/',
            'https://nhandan.vn/moi-truong/',
    ]       
    rules = (
        Rule(LinkExtractor(allow='',
                           deny=['/abc/'],
                           process_value=strip_value,
                           restrict_xpaths=["//button[@class='text control__loadmore']"]), follow=True, process_links=None),
        Rule(LinkExtractor(allow='',
                           deny=['/abc/'],
                           process_value=strip_value,
                           restrict_xpaths=["//a[@class='cms-link']"]), follow=False, callback='parse_item', process_links=None)
    )

    def parse_item(self, response):
        item = NhandanItem()
        item['title'] = response.xpath("//h1[@class='article__title cms-title']/text()").get().strip()
        list_p = response.xpath("//div[@class='article__sapo cms-desc'] | //div[@class='article__body cms-body']//p").getall()
        item['content'] = listToString(list_p)
        item['category'] = response.xpath("//div[@class='breadcrumbs']/a[@class='wrap-text']/h3[@class='text']/text()").get().strip()
        item['image'] = response.xpath("//img[@class='cms-photo']/@src").get()
        item['url'] = response.request.url

        post = WordPressPost()
        post.title = item['title']
        post.content = item['content']
        post.post_status = 'publish'
        post.terms_names = {
            'post_tag': ['nhandan'],
            'category': [item['category']]
        }

        r = requests.get(item['image'])
        with open(f"{item['title']}.png",'wb') as f:
             f.write(r.content)
        filename = f"C:\\Users\\trant\\Desktop\\nhandan\\nhandan\\{item['title']}.png"
        data = {    
            'name': f'{item["title"]}.jpg',
            'type': 'image/jpeg',
        }
        with open(filename, 'rb') as img:
            data['bits'] = xmlrpc_client.Binary(img.read())
        response = wp.call(media.UploadFile(data))
        attachment_id = response['id']
        post.thumbnail = attachment_id
        os.remove(f"{item['title']}.png")

        wp.call(NewPost(post))
        return item