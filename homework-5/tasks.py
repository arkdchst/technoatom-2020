#!/usr/bin/env python
import re
from itertools import groupby
from os.path import isfile
from db.models import *


class Tasks:
	def task_a(self):
		return [TaskA(result = len(self.requests))]

	def task_b(self):
		methods = ['OPTIONS','GET','HEAD','POST','PUT','DELETE','TRACE','CONNECT']
		stats = {}
		for dict_ in self.requests:
			method = dict_['method']
			if not method in methods: continue

			if not method in stats.keys():
				stats[method] = 0

			stats[method] += 1
		
		res = []
		for key in stats:
			res.append(TaskB(method=key, count=stats[key]))

		return res

	def task_c(self):
		requests = list(self.requests)
		requests.sort(key=lambda x: x['url'])
		grouped = []
		for _,group in groupby(requests, lambda x: x['url']):
			group = list(group)
			group.sort(key=lambda x: x['len'], reverse=True)
			grouped.append(group[0])
			grouped[-1]['count'] = len(group)
		grouped.sort(key=lambda x: x['len'], reverse=True)
		grouped = grouped[:10]

		res = []
		for request in grouped:
			res.append(TaskC(url=request['url'], code=request['code'], count=request['count']))

		return res

	def task_d(self):
		requests = list(self.requests)
		requests = list(filter(lambda x: x['code'] in range(400, 500), requests))
		requests.sort(key=lambda x: x['url'])
		grouped = []
		for _,group in groupby(requests, lambda x: x['url']):
			group = list(group)
			grouped.append(group[0])
			grouped[-1]['count'] = len(group)
		grouped.sort(key=lambda x: x['count'], reverse=True)
		grouped = grouped[:10]

		res = []
		for request in grouped:
			res.append(TaskD(url=request['url'], code=request['code'], ip=request['ip']))

		return res

	def task_e(self):
		requests = list(self.requests)
		requests = list(filter(lambda x: x['code'] in range(500, 600), requests))
		requests.sort(key=lambda x: x['url'])
		grouped = []
		for _,group in groupby(requests, lambda x: x['url']):
			group = list(group)
			group.sort(key=lambda x: x['len'], reverse=True)
			grouped.append(group[0])
		grouped.sort(key=lambda x: x['len'], reverse=True)
		grouped = grouped[:10]

		res = []
		for request in grouped:
			res.append(TaskE(url=request['url'], code=request['code'], ip=request['ip']))

		return res

	def to_requests(self, lines):
		requests = []
		for line in lines:
			dict_ = {}
			splited = re.split('[ "]', line)
			dict_['ip'] = splited[0]
			dict_['method'] = splited[6]
			dict_['url'] = splited[7]
			dict_['code'] = int(splited[10])
			dict_['len'] = 0 if splited[11] == '-' else int(splited[11])
			requests.append(dict_)

		return requests

	def __init__(self):
		with open('access.log') as f:
			lines = f.read().split('\n')

		if lines[-1] == '':
			del lines[-1]

		self.requests = self.to_requests(lines)

