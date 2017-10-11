from django.db import models

import MySQLdb

class FilterResult():
	"""docstring for FilterResult"""
	def __init__(self,item):
		self.query_item = {i:[_d.split("_") for _d in d] for i,d in item.items() if d}
		self.table = {
			'1':{
				"hmacwt":{
					'H3K4ac vs H3':'0',
					'H3K9ac vs H3 [YPD]':'1',
					'H3K14ac vs H3 [YPD]':'2',
					'H4ac vs H3 [YPD]':'5'
				},
				'hmacmut':{
					'H3K4ac [set1D] vs [WT]':'0',
					'H3K4ac vs H3 [set1D]':'1'
				}
			},
			'2':{
				'hmmewt':{
					'H3K4me3 vs H3 [WCE]':'0',
					'H3K36me3 vs H3':'2',
					'H3K79me2 vs H3':'3',
					'H3K79me3 vs H3':'4',
					'H3K4me1 vs H3':'5',
					'H3K4me2 vs H3':'6',
					'H3R2me2a vs H3':'8'
				},
				'hmmemut':{
					'H3K4me3 vs H3 [ubp8D]':'0',
					'H3K36me3 vs H3 [ubp8D]':'1',
					'H3K79me3 vs H3 [ubp8D]':'2',
					'H3K4me3 vs H3 [ubp10D]':'3',
					'H3K79me3 vs H3 [ubp10D]':'4'
				}
			},
			'3':{
				'h2az':{
					'H2A.Z vs H2B':'0',
					'H2A vs H2B':'1'
				},
				'h2ubimut':{
					'H2BK123ub vs H2':'0'
				},
				'h2ubimut':{
					'H2BK123ub vs H2 [ubp8D]':'0',
					'H2BK123ub vs H2 [ubp10D]':'1'
				}
			}
		}

	def getResult(self):
		return self.query_item
		# try:
		# 	db = MySQLdb.connect('localhost', 'haoping', 'a012345', 'yna_database')

		# except Exception as e:
		# 	raise e