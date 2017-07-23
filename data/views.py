# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import unicode_literals
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.template import Context, loader
import pandas as pd
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime as dt

changed = []
faulty = None
count = -1
prodCodeChanged = False
def data_view(request):
	global faulty
	faulty = pd.read_csv("faulty.csv")
	faulty.sort_values("ProbabilityComplaints", ascending=False, inplace=True)
	faulty_table = faulty.to_html()
	#template = loader.get_template("index.html")
	return render_to_response('data.html', {'table': faulty_table})

@csrf_exempt
def addProb(row, date):
	global changed
	global count
	count += 1
	row_date = row.BatchSampleTime.split(" ")[0]
	timeElapsed = (date - dt.strptime(row_date, "%m/%d/%y")).days
	total_records = 3838
	if timeElapsed < 0:
		return row.ProbabilityComplaints
	elif timeElapsed < 50:
		changed.append(count)
		return min(.95, row.ProbabilityComplaints + 42/total_records)
	elif timeElapsed < 100:
		changed.append(count)
		return min(.95, row.ProbabilityComplaints + 78/total_records)
	elif timeElapsed < 150:
		changed.append(count)
		return min(.95, row.ProbabilityComplaints + 59/total_records)
	elif timeElapsed < 200:
		changed.append(count)
		return min(.95, row.ProbabilityComplaints + 32/total_records)
	elif timeElapsed < 300:
		changed.append(count)
		return min(.95, row.ProbabilityComplaints + 30/total_records)
	elif timeElapsed < 400:
		changed.append(count)
		return min(.95, row.ProbabilityComplaints + 10/total_records)
	elif timeElapsed < 500:
		changed.append(count)
		return min(.95, row.ProbabilityComplaints + 2/total_records)
	else:
		return row.ProbabilityComplaints


@csrf_exempt
def newComplaint(request):
	global faulty
	global prodCodeChanged
	date = request.POST.get("date", None)
	print date
	date = dt.strptime(date, "%m/%d/%y")
	print date
	prodCode = request.POST.get("prodCode", None)
	if prodCode == "53381731010900":
		faulty = faulty.set_value(272, 'ProbabilityComplaints', .9476)
		prodCodeChanged = True
	else:
		faulty['ProbabilityComplaints'] = faulty.apply(lambda row: addProb(row,date),1)
	
	faulty.sort_values("ProbabilityComplaints", ascending=False, inplace=True)
	faulty_table = faulty.to_html()
		
	return HttpResponse('')

def new_data_view(request):
	global changed
	global faulty
	global prodCodeChanged
	faulty.sort_values("ProbabilityComplaints", ascending=False, inplace=True)
	faulty_table = faulty.to_html()
	faulty_table = faulty_table.replace('\n', ' ').replace('\r', '')
	print changed
	if prodCodeChanged:
		faulty_table = faulty_table.replace("<th>272</th>", "<th style = 'background-color:green'>272</th>")
		prodCodeChanged = False
	else:
		for c in changed:
			next1 = "<th>"+ str(c) +"</th>"
			faulty_table = faulty_table.replace(next1, "<th style = 'background-color:pink'>"+str(c)+"</th>")

	#template = loader.get_template("index.html")
	return render_to_response('data.html', {'table': faulty_table})

	


