#!/usr/bin/env python
import argparse
import re
from itertools import groupby
import json
from os.path import isfile

def task_a(lines):
	return len(lines)

def task_b(requests):
	methods = ['OPTIONS','GET','HEAD','POST','PUT','DELETE','TRACE','CONNECT']
	stats = {}
	for dict_ in requests:
		method = dict_['method']
		if not method in methods: continue

		if not method in stats.keys():
			stats[method] = 0

		stats[method] += 1
	
	ret = []
	for key in stats:
		dict_ = {}
		dict_['method'] = key
		dict_['count'] = stats[key]
		ret.append(dict_)

	return ret

def task_c(requests):
	requests.sort(key=lambda x: x['url'])
	grouped = []
	for _,group in groupby(requests, lambda x: x['url']):
		group = list(group)
		group.sort(key=lambda x: x['len'], reverse=True)
		grouped.append(group[0])
		grouped[-1]['count'] = len(group)
	grouped.sort(key=lambda x: x['len'], reverse=True)
	grouped = grouped[:10]

	ret = []
	for request in grouped:
		dict_ = {}
		dict_['url'] = request['url']
		dict_['code'] = request['code']
		dict_['count'] = request['count']
		ret.append(dict_)

	return ret

def task_d(requests):
	requests = list(filter(lambda x: x['code'] in range(400, 500), requests))
	requests.sort(key=lambda x: x['url'])
	grouped = []
	for _,group in groupby(requests, lambda x: x['url']):
		group = list(group)
		grouped.append(group[0])
		grouped[-1]['count'] = len(group)
	grouped.sort(key=lambda x: x['count'], reverse=True)
	grouped = grouped[:10]

	ret = []
	for request in grouped:
		dict_ = {}
		dict_['url'] = request['url']
		dict_['code'] = request['code']
		dict_['ip'] = request['ip']
		ret.append(dict_)

	return ret

def task_e(requests):
	requests = list(filter(lambda x: x['code'] in range(500, 600), requests))
	requests.sort(key=lambda x: x['url'])
	grouped = []
	for _,group in groupby(requests, lambda x: x['url']):
		group = list(group)
		group.sort(key=lambda x: x['len'], reverse=True)
		grouped.append(group[0])
	grouped.sort(key=lambda x: x['len'], reverse=True)
	grouped = grouped[:10]

	ret = []
	for request in grouped:
		dict_ = {}
		dict_['url'] = request['url']
		dict_['code'] = request['code']
		dict_['ip'] = request['ip']
		ret.append(dict_)

	return ret

def to_requests(lines):
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

def main():
	outfile = 'analyzed'

	parser = argparse.ArgumentParser(usage='analyze.py  [--json]  task_a | task_b | task_c | task_d | task_e  <FILE>', epilog=f'Имя выходного файла - {outfile}.')
	parser.add_argument('task', action='store', help='см. в README.md', choices=['task_a', 'task_b', 'task_c', 'task_d', 'task_e'])
	parser.add_argument('file', action='store', metavar='FILE', help='входной файл')
	parser.add_argument('--json', action='store_true', help='записать вывод в формате JSON')

	args = parser.parse_args()

	if isfile(outfile):
		print(f"File '{outfile}' exists, overwrite? (yes/NO): ", end='')
		in_ = input()
		if not (in_ == 'y' or in_ == 'yes'):
			raise FileExistsError()

	with open(args.file) as f:
		lines = f.read().split('\n')

	if lines[-1] == '':
		del lines[-1]

	task = args.task
	if task == 'task_a':
		res = task_a(lines)
	else:
		requests = to_requests(lines)

		if   task == 'task_b': res = task_b(requests)
		elif task == 'task_c': res = task_c(requests)
		elif task == 'task_d': res = task_d(requests)
		elif task == 'task_e': res = task_e(requests)
		else:
			raise Exception()

	with open(outfile, 'w') as f:
		if args.json:
				f.write(json.dumps(res))
		else:
			if isinstance(res, list):
				for line in res:
					for key in line:
						f.write(str(line[key]) + ' ')
					f.write('\n')
			elif isinstance(res, int):
				f.write(str(res))
			else:
				raise Exception()

if __name__ == '__main__':
	main()