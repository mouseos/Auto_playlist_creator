import os
import sys
import pathlib
import re
import csv
import random
import numpy as np
#後10秒の差を許容
pd=0
#前10秒の差を許容
md=10
#時間(秒)
set_duration=7000
duration=[]
track=[]
if len(sys.argv) > 1:
	if((os.path.exists(sys.argv[1]))):
		path = pathlib.Path(sys.argv[1]).resolve()
		with open('audio_files.csv', 'r') as csv_file:
			reader = csv.DictReader(csv_file)
			for row in reader:
				duration.append((float(row['Duration'])))
				track.append([(row['Path']),(row['Duration'])])
			#print(track)

#参考：https://phst.hateblo.jp/entry/2022/01/17/080000
def get_integral_value_combination(items, target):
	def a(idx, l, r, t):
		p=t-(pd/round(set_duration/3600))
		m=t-(md/round(set_duration/3600))
		if (p>=sum(l) and sum(l)>=m): 
			r.append(l)
		elif t < sum(l): 
			return
		for u in range(idx, len(items)):
			a((u + 1), l + [items[u]], r, t)
		return r
	return a(0, [], [], target)


result1=[]
items=[]
while True:
	if ((set_duration)>0):
		items =(random.sample(list( set(duration) - set(result1) ), 20))#20個に分割 result1を引くことで重複回避
		if ((set_duration)<=3600) :
			#残りの長さが3600以下
			result0 = get_integral_value_combination(items, set_duration)
			result1=result1+(random.choice(result0))
			set_duration-=3600
		if ((set_duration)>3600) :
			#残りの長さが3600以上
			result0 = get_integral_value_combination(items, 3600)
			result1=result1+(random.choice(result0))
			set_duration-=3600
	elif (set_duration<=0):
			print(result1)#長さ一覧
			print(sum(result1))#合計時間
			for dur in result1:
				track = np.array(track)
				print(np.argwhere(track==str(dur)))
					
			print("終了します。")
			break


