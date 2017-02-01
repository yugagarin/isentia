import pymongo
import traceback
from scrapy.conf import settings
from scrapy.exceptions import DropItem
import logging

class MongoDBPipeline(object):
	""" Part of scrapy pipeline to write into mongodb database """
    def __init__(self):
        connection = pymongo.MongoClient(settings['MONGODB_URI'],ssl_ca_certs=settings['MONGODB_CERT'])
        db = connection[settings['MONGODB_DB']]
        self.collection = db[settings['MONGODB_COLLECTION']]

    def process_item(self, item, spider):
		try:
			valid = True
			for data in item:
				if not data:
					valid = False
					raise DropItem("Missing {0}!".format(data))
			if valid:
				self.collection.insert(dict(item))
				logging.log(logging.DEBUG,"News article added to MongoDb database")
			return item
		except:
			logging.log(logging.CRITICAL,"Error while writing to MongDb:\n" + traceback.print_exc())
			
