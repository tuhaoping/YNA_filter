from __future__ import unicode_literals
from django.db import models


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
