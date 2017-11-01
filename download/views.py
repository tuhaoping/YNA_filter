from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.utils.encoding import smart_str

import csv
import json

def downloadfile(request, filename):
	# print(filename)
	# filename = 'testfile.txt'
	# print(request.session['genelist'])
	# response = HttpResponse(content_type='application/force-download') # mimetype is replaced by content_type for django 1.7
	# response['Content-Disposition'] = "attachment; filename=%s" % smart_str(filename.encode('utf-8'))
	# response['X-Sendfile'] = smart_str('/home/haoping/Django/yna_filter/static/file/testfile.txt')
	# with open('/home/haoping/Django/yna_filter/static/file/testfile.txt') as f:
		# c = f.read()


	response = HttpResponse(content_type='text/csv')
	response['Content-Disposition'] = 'attachment; filename="{}.csv"'.format(filename)

	writer = csv.writer(response)
	writer.writerow(['Feature Name', 'Standard Name', 'Alias'])
	for i in json.loads(request.session['genelist']):
		writer.writerow(i)

	return response