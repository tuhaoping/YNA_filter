from django.db import models

import MySQLdb

class FilterResult():
	"""docstring for FilterResult"""
	def __init__(self,item):
		self.query_item = {i:[_d.split("_") for _d in d] for i,d in item.items() if d}
		self.table = {
			'1':{
				"hmacwt":{
					'table':2,
					'per_table_data':5,
					'H3K4ac vs H3':'0',
					'H3K9ac vs H3 [YPD]':'1',
					'H3K14ac vs H3 [YPD]':'2',
					'H4ac vs H3 [YPD]':'5'
				},
				'hmacmut':{
					'table':1,
					'per_table_data':2,
					'H3K4ac [set1D] vs [WT]':'0',
					'H3K4ac vs H3 [set1D]':'1'
				}
			},
			'2':{
				'hmmewt':{
					'table':3,
					'per_table_data':5,
					'H3K4me3 vs H3 [WCE]':'0',
					'H3K36me3 vs H3':'2',
					'H3K79me2 vs H3':'3',
					'H3K79me3 vs H3':'4',
					'H3K4me1 vs H3':'5',
					'H3K4me2 vs H3':'6',
					'H3R2me2a vs H3':'8'
				},
				'hmmemut':{
					'table':1,
					'per_table_data':5,
					'H3K4me3 vs H3 [ubp8D]':'0',
					'H3K36me3 vs H3 [ubp8D]':'1',
					'H3K79me3 vs H3 [ubp8D]':'2',
					'H3K4me3 vs H3 [ubp10D]':'3',
					'H3K79me3 vs H3 [ubp10D]':'4'
				}
			},
			'3':{
				'h2az':{
					'table':1,
					'per_table_data':2,
					'H2A.Z vs H2B':'0',
					'H2A vs H2B':'1'
				},
				'h2ubiwt':{
					'table':1,
					'per_table_data':2,
					'H2BK123ub vs H2':'0'
				},
				'h2ubimut':{
					'table':1,
					'per_table_data':2,
					'H2BK123ub vs H2 [ubp8D]':'0',
					'H2BK123ub vs H2 [ubp10D]':'1'
				}
			}
		}

	def getResult(self, result_type = 'intersection'):
		# return self.query_item
		self.result_gene = set()
		for i, data in self.query_item.items():
			data_list = {k:[] for k in self.table[i].keys()}
			for f in data:
				for f_class, table in self.table[i].items():
					if f[0] in table:
						data_list[f_class].append("Data{}_{} {} {}".format(table[f[0]], f[1], f[2], f[3]))
			for table, data in data_list.items():
				if data:
					table_count = self.table[i][table]['table']
					if table_count == 1:	# 資料表只有一張
						sql_com = "SELECT Name_ORF FROM {} WHERE {}".format("yna_filter_"+table, " AND ".join(data))
					else:	# 資料表有一張以上
						table_list = ['yna_filter_{}_{}'.format(table, i) for i in range(table_count)]
						sql_com = "SELECT {} FROM {}".format(table_list[0]+'.Name_ORF', table_list[0])
						for _i, t in enumerate(table_list[1:]): #LEFT JOIN 起來
							sql_com = "{} LEFT JOIN {} ON {}={}".format(sql_com, t, table_list[_i]+'.Name_ORF', t+'.Name_ORF')

						
						if result_type == 'intersection':
							sql_com = "{} WHERE {}".format(sql_com, " AND ".join(data))
						else:
							sql_com = "{} WHERE {}".format(sql_com, " OR ".join(data))


						# print(sql_com)

				try:
					db = MySQLdb.connect('localhost', 'haoping', 'a012345', 'yna_database')
					cursor = db.cursor()
					cursor.execute(sql_com)
					if not self.result_gene:
						self.result_gene = {i[0] for i in cursor.fetchall()}
					else:
						if result_type == 'intersection':
							self.result_gene &= {i[0] for i in cursor.fetchall()}
						else:
							self.result_gene |= {i[0] for i in cursor.fetchall()}

						# print(i)
				except:
					pass
				finally:
					db.close()

		print(len(self.result_gene))
		return self.result_gene
		# try:
		# 	db = MySQLdb.connect('localhost', 'haoping', 'a012345', 'yna_database')
		# 	cursor = db.cursor()

		# except Exception as e:
		# 	raise e