from django.shortcuts import render
from main_result.models import FilterResult
import json

# Create your views here.
def result(request):
	# print(request.POST['jdata'])
	a = json.loads(request.POST['jdata'])
	result = FilterResult(a)
	# print()
	gene_set = sorted(list(result.getResult()))
	return render(request, 'test.html', {'gene':gene_set})