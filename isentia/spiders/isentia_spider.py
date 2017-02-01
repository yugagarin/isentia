## response.xpath('//meta[@name="author"]').xpath('@content').extract() authot in the guardian 

import logging
import traceback

import scrapy
import urlparse 
from scrapy.http import Request 
from scrapy.selector import Selector 
from scrapy.spiders import Spider 
from scrapy.linkextractors import LinkExtractor
from scrapy.item import Item, Field
from scrapy.contrib.spiders import CrawlSpider, Rule

#various web page parsing tools 
from readability import Document
import html2text
import lxml.etree
import lxml.html

class MyItem(Item):
	""" Fields extracted from the web page """
	text_body=scrapy.Field()
	url=scrapy.Field()
	author=scrapy.Field()
	headline=scrapy.Field()

class QuotesSpider(CrawlSpider):
    name = "isentia"
	
    allowed_domains= ['theguardian.com','bbc.com']
    start_urls = ['https://www.theguardian.com/au','http://www.bbc.com/']

    rules = (Rule(LinkExtractor(allow=()), callback='parse_item', follow=True),)
 
    def parse_item(self, response):
		try:
			#html2text parsing option
			#h = html2text.HTML2Text()
			#Ignore converting links from HTML
			#h.ignore_links = True
		
			#lxml parsing option
			#root = lxml.html.fromstring(response.body.decode('utf8'))
			# optionally remove tags that are not usually rendered in browsers
			# javascript, HTML/HEAD, comments, add the tag names you dont want at the end
			#lxml.etree.strip_elements(root, lxml.etree.Comment, "script", "head")
		
			doc = Document(response.body.decode('utf8'))
			item = MyItem()
			item['text_body'] = doc.summary() 
			#item['text_body'] = lxml.html.tostring(root, method="text", encoding=response.encoding)		
			#item['text_body'] = h.handle(response.body.decode(response.encoding))
			item['url'] = response.url
			item['author']='' 
			item['headline']=doc.title()
			return item
		except:
			logging.log(logging.CRITICAL,"Error while parsing item in spider:\n" + traceback.print_exc())


