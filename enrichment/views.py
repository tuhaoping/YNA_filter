from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.template.loader import render_to_string
from enrichment.models import YnaEnrichment, SqlCustomTable

import json
import scipy.stats
from MySQLdb import connect

def showEnrich(request):
	data = SqlCustomTable.getTableValue(request.session['tableName'])
	if 'gene' in request.POST:
		geneset = set(filter(None,request.POST['gene'].split('\n')))
	else:
		geneset = set(request.session['geneset'].split(','))

	S = len(geneset)
	enrich_value = []

	for i in data:
		temp_enrich = []
		temp_intersects = []

		gene = [set(i['pro_en'].split(',')), set(), set(i['cod_en'].split(',')), set()]
		# gene = [set(i.pro_en.split(',')), set(i.pro_de.split(',')), set(i.cod_en.split(',')), set(i.cod_de.split(','))]
		
		for g in gene:
			T = len(g & geneset)
			G = len(g)
			temp_enrich.append(Hypergeometric_pvalue(T, S, G))
			temp_intersects.append([T, S, "{:0<.2f}%".format(T/S*100), G, 6576, "{:0<.2f}%".format(G/6576*100)])

		enrich_value.append([i['Type'], zip(temp_enrich, temp_intersects)])

	render_dict = {
		'enrich_value': enrich_value,
	}
	return render(request, 'enrich_template.html', render_dict)

def operateCustomTable(request, m):
	if m == 'init':
		customTable = SqlCustomTable()
		request.session['tableName'] = customTable.tableName
		return JsonResponse({'tableName':customTable.tableName})
	elif m == 'close':
		SqlCustomTable.deleteTable(request.session['tableName'])
		return HttpResponse(status=200)
	elif m == 'update':
		SqlCustomTable.updateTable(request.session['tableName'], request.GET['f'])
		return HttpResponse(status=200)

def Hypergeometric_pvalue(T, S, G, F=6576):
    '''calculate every pvalue of each feature'''
    # T = 'intersects'         #交集數         1
    # S = 'input_gene'         #輸入 genes數   18
    # G = 'feature_gene'       #genes 樣本數   1117
    # F = 'total_feature_gene'         #總 genes數     6572

    S_T = S-T
    G_T = G-T
    F_G_S_T = F-G-S+T
    
    if F_G_S_T <= 0:
    	return ""
    
    pvalue = scipy.stats.fisher_exact( [ [T,G_T] , [S_T,F_G_S_T]] ,'greater')[1]

    if pvalue < (10**-2):
    	return "{:1.3E}".format(pvalue)
    else:
    	return ""
