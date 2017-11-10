from django.shortcuts import render
from django.http import JsonResponse
from django.template.loader import render_to_string
from enrichment.models import YnaEnrichment

import json
import scipy.stats

def showEnrich(request):
	# print(type(json.loads(request.session['geneset'])))
	data = YnaEnrichment.objects.all()
	if 'gene' in request.POST:
		geneset = set(filter(None,request.POST['gene'].split('\n')))
	else:
		geneset = set(request.session['geneset'].split(','))

	S = len(geneset)
	# pvalue = []
	# intersects_value = []
	enrich_value = []

	for i in data:
		temp_enrich = []
		temp_intersects = []

		gene = [set(i.pro_en.split(',')), set(), set(i.cod_en.split(',')), set()]
		# gene = [set(i.pro_en.split(',')), set(i.pro_de.split(',')), set(i.cod_en.split(',')), set(i.cod_de.split(','))]
		# temp_enrich.append(i.Type)
		# print(i.Type)
		
		for g in gene:
			T = len(g & geneset)
			G = len(g)
			temp_enrich.append(Hypergeometric_pvalue(T, S, G))
			temp_intersects.append([T, S, "{:0<.2f}%".format(T/S*100), G, 6576, "{:0<.2f}%".format(G/6576*100)])

		# pvalue.append(temp_enrich)
		# intersects_value.append(temp_intersects)

		enrich_value.append([i.Type, zip(temp_enrich, temp_intersects)])
	# return JsonResponse({'list':request.session['geneset'].split(",")})
	render_dict = {
		# 'pvalue':pvalue,
		# 'intersects_value':intersects_value,
		'enrich_value': enrich_value,
	}
	return render(request, 'enrich_template.html', render_dict)


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
    
    # print((T, S, G, F), (T, S_T, G_T, F_G_S_T))
    pvalue = scipy.stats.fisher_exact( [ [T,G_T] , [S_T,F_G_S_T]] ,'greater')[1]
    # less = stats.fisher_exact( [ [T,G_T] , [S_T,F_G_S_T]] ,'less')[1]
    
    # return pvalue
    if pvalue < (10**-2):
    	return "{:1.3E}".format(pvalue)
    else:
    	return ""

