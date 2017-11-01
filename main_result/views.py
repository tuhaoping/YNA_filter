from django.shortcuts import render
from main_result.models import FilterResult
import json

# Create your views here.
def result(request):
	# print(request.POST['jdata'])
	a = json.loads(request.POST['jdata'])
	result = FilterResult(a)
	# print()
	total = result.getResult(request.POST['composition'])
	gene_set = result.getGeneName()
	# print(json.dumps(gene_set))
	request.session['genelist'] = json.dumps(gene_set)
	item = [_d.split("_") for i,d in a.items() for _d in d if d]
	# print(item)
	return render(request, 'test.html', {'gene':gene_set, 'total':total, 'composition':request.POST['composition'], 'condiction':item})