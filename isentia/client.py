import pymongo

from scrapy.conf import settings
from scrapy.exceptions import DropItem
from scrapy import log
import pprint

class MongoDBClient(object):

    def __init__(self):
        connection = pymongo.MongoClient("mongodb://isentia:isentia@sl-aus-syd-1-portal.2.dblayer.com:15428,sl-aus-syd-1-portal.1.dblayer.com:15428/isentia?ssl=true",
            ssl_ca_certs="./cert.crt"
        )
        db = connection['isentia']
        self.collection = db['media']

    def query(self, term):
        #pprint.pprint(self.collection.index_information())
        #pprint.pprint(self.collection.create_index([('text_body', 'text')], default_language='english')) # 
        qry={ '$text': { '$search': term}}
        cur=self.collection.find(qry)
        for doc in cur:
            pprint.pprint(doc)


client=MongoDBClient()
client.query('coal')