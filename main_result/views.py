from django.shortcuts import render
from main_result.models import FilterResult
import json

# Create your views here.
def result(request):
	# print(request.POST['jdata'])
	a = json.loads(request.POST['jdata'])
	result = FilterResult(a)
	# print()
	gene_set, total = result.getResult(request.POST['composition'])
	gene_set = sorted(list(gene_set))
	return render(request, 'test.html', {'gene':gene_set, 'total':total})