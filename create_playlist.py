import os
import sys
import pathlib
import re
import csv
#後10秒の差を許容
pd=10
#前10秒の差を許容
md=10
duration=[]
if len(sys.argv) > 1:
	if((os.path.exists(sys.argv[1]))):
		path = pathlib.Path(sys.argv[1]).resolve()
		with open('audio_files.csv', 'r') as csv_file:
			reader = csv.DictReader(csv_file)
			for row in reader:
				duration.append(round(float(row['Duration'])))
			print(duration)
items =(duration)

def get_integral_value_combination(items, target):
	def a(idx, l, r, t):
		p=t+pd
		m=t-md
		if (p>=sum(l) and sum(l)>=m): 
			r.append(l)
		elif t < sum(l): 
			return
		for u in range(idx, len(items)):
			a((u + 1), l + [items[u]], r, t)
		return r
	return a(0, [], [], target)

result = get_integral_value_combination(items, 3600)
for res in result:
	print(res)
	print(sum(res))
