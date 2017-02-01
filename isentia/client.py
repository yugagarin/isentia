#!/usr/bin/python

import pymongo
import traceback
import logging
import pprint
import sys

class MongoDBClient(object):
	
	def __init__(self):
		connection = pymongo.MongoClient("mongodb://isentia:isentia@sl-aus-syd-1-portal.2.dblayer.com:15428,sl-aus-syd-1-portal.1.dblayer.com:15428/isentia?ssl=true",ssl_ca_certs="./cert.crt")
		db = connection['isentia']
		self.collection = db['media']
	
	def ix_information(self):
		""" Get list of indices """
		pprint.pprint(self.collection.index_information()) #get list of indexes
	
	def create_ft_index(self):
		"""Create full text index on collection""" 
		pprint.pprint(self.collection.create_index([('text_body', 'text')], default_language='english')) 
	
	def query(self, term): 
		""" Queries the collection for a term in html body """
		qry={ '$text': { '$search': term}}
		cur=self.collection.find(qry)
		for doc in cur:
			pprint.pprint(doc)

def main():
	try:
		if (len(sys.argv)==1):
			return
		else:
			client=MongoDBClient()
			query=sys.argv[1]
			client.query(query)
	except:
		logging.log(logging.CRITICAL,"Error in main:\n" + traceback.print_exc())

if __name__ == "__main__":
    main()