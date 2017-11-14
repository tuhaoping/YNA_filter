from __future__ import unicode_literals
from django.db import models

import time
from random import randint
from MySQLdb import connect

class YnaEnrichment(models.Model):
    Type = models.CharField(db_column='Type', primary_key=True, max_length=50)  # Field name made lowercase.
    pro_en = models.TextField(db_column='Pro_en')  # Field name made lowercase.
    pro_de = models.TextField(db_column='Pro_de')  # Field name made lowercase.
    cod_en = models.TextField(db_column='Cod_en')  # Field name made lowercase.
    cod_de = models.TextField(db_column='Cod_de')  # Field name made lowercase.

    def __str__(self):
        return self.Type

    class Meta:
        managed = False
        db_table = 'YNA_Enrichment'


class SqlCustomTable():

    SQLtable = {
        'H3K4ac vs H3':{'table':'YNA_Filter_HmAcWt_0', 'column':'Data0'},
        'H3K9ac vs H3 [YPD]':{'table':'YNA_Filter_HmAcWt_0', 'column':'Data1'},
        'H3K14ac vs H3 [YPD]':{'table':'YNA_Filter_HmAcWt_0', 'column':'Data2'},
        'H4ac vs H3 [YPD]':{'table':'YNA_Filter_HmAcWt_1', 'column':'Data5'},

        'H3K4ac [set1D] vs [WT]':{'table':'YNA_Filter_HmAcMut', 'column':'Data0'},
        'H3K4ac vs H3 [set1D]':{'table':'YNA_Filter_HmAcMut', 'column':'Data1'},
        
        'H3K4me3 vs H3 [WCE]':{'table':'YNA_Filter_HmMeWt_0', 'column':'Data0'},
        'H3K36me3 vs H3':{'table':'YNA_Filter_HmMeWt_0', 'column':'Data2'},
        'H3K79me2 vs H3':{'table':'YNA_Filter_HmMeWt_0', 'column':'Data3'},
        'H3K79me3 vs H3':{'table':'YNA_Filter_HmMeWt_0', 'column':'Data4'},
        'H3K4me1 vs H3':{'table':'YNA_Filter_HmMeWt_1', 'column':'Data5'},
        'H3K4me2 vs H3':{'table':'YNA_Filter_HmMeWt_1', 'column':'Data6'},
        'H3R2me2a vs H3':{'table':'YNA_Filter_HmMeWt_1', 'column':'Data7'},
        
        'H3K4me3 vs H3 [ubp8D]':{'table':'YNA_Filter_HmMeMut', 'column':'Data0'},
        'H3K36me3 vs H3 [ubp8D]':{'table':'YNA_Filter_HmMeMut', 'column':'Data1'},
        'H3K79me3 vs H3 [ubp8D]':{'table':'YNA_Filter_HmMeMut', 'column':'Data2'},
        'H3K4me3 vs H3 [ubp10D]':{'table':'YNA_Filter_HmMeMut', 'column':'Data3'},
        'H3K79me3 vs H3 [ubp10D]':{'table':'YNA_Filter_HmMeMut', 'column':'Data4'},

        'H2A.Z vs H2B':{'table':'YNA_Filter_H2AZ', 'column':'Data0'},
        'H2A vs H2B':{'table':'YNA_Filter_H2AZ', 'column':'Data1'},

        'H2BK123ub vs H2':{'table':'YNA_Filter_H2UbiWt', 'column':'Data0'},

        'H2BK123ub vs H2 [ubp8D]':{'table':'YNA_Filter_H2UbiMut', 'column':'Data0'},
        'H2BK123ub vs H2 [ubp10D]':{'table':'YNA_Filter_H2UbiMut', 'column':'Data1'},
    }

    def __init__(self):
        self.__name = 'yna_enrichment_' + str(randint(0, 100000) * randint(0, 100000))
        try:
            db = connect('localhost', 'haoping', 'a012345', 'yna_database')
            cursor = db.cursor()
            SQLcmd = 'CREATE TABLE `{}` LIKE `yna_enrichment`;'.format(self.__name)
            cursor.execute(SQLcmd)
            SQLcmd = 'INSERT `{}` select * from `yna_enrichment`;'.format(self.__name)
            cursor.execute(SQLcmd)
        finally:
            db.commit()
            db.close()

    @property
    def tableName(self):
        return self.__name

    @staticmethod
    def deleteTable(tableName):
        try:
            db = connect('localhost', 'haoping', 'a012345', 'yna_database')
            cursor = db.cursor()
            SQLcmd = 'select * into `{}` '
            SQLcmd = 'DROP TABLE `{}`'.format(tableName)
            cursor.execute(SQLcmd)
        except:
            # print(e)
            pass
        finally:
            db.commit()
            db.close()

    @staticmethod
    def updateTable(tableName, data):
        feature, enrich_type, cutoff = data.split("/")

        table = SqlCustomTable.SQLtable[feature]['table']
        column = SqlCustomTable.SQLtable[feature]['column']
        enrich_column = []

        if 'pro' in enrich_type:
            column += "_Pro"
            enrich_column.append('Pro')

        elif 'code' in enrich_type:
            column += "_Code"
            enrich_column.append('Cod')

        if 'enriched' in enrich_type:
            com = ">="
            enrich_column.append('en')

        elif 'depleted' in enrich_type:
            com = "<="
            enrich_column.append('de')

        enrich_column = "_".join(enrich_column)

        try:
            db = connect('localhost', 'haoping', 'a012345', 'yna_database')
            cursor = db.cursor()
            SQLcmd = "SELECT `Name_ORF` FROM `{}` WHERE `{}` {} {}".format(table, column, com, cutoff)
            cursor.execute(SQLcmd)
            res = ",".join([i[0] for i in cursor.fetchall()])
            SQLcmd = "UPDATE `{}` SET `{}` = '{}' WHERE `Type` = '{}'".format(tableName, enrich_column, res, feature)
            cursor.execute(SQLcmd)


        except Exception as e:
            raise e

        finally:
            db.commit()
            db.close()

    @staticmethod
    def getTableValue(tableName):
        try:
            db = connect('localhost', 'haoping', 'a012345', 'yna_database')
            cursor = db.cursor()
            SQLcmd = "SELECT * FROM `{}` WHERE 1".format(tableName)
            cursor.execute(SQLcmd)
            res = [{
                'Type':i[0],
                'pro_en':i[1],
                'pro_de':i[2],
                'cod_en':i[3],
                'cod_de':i[4]} for i in cursor.fetchall()]

        except Exception as e:
            raise e

        finally:
            db.commit()
            db.close()

        return res