import os
import sys
import pathlib
import re
import csv
import random
import numpy as np
#使い方：python3 ./create_playlist.py [CSVパス] [前許容秒数] [後許容秒数] [プレイリスト全体の秒数] [m3uファイル名]
def help ():
	print("使い方：python3 ./create_playlist.py [CSVパス] [前許容秒数] [後許容秒数] [プレイリスト全体の秒数] [m3uファイル名]")

if (len(sys.argv) > 5) and ((float(sys.argv[4]))>0) and ((float(sys.argv[3]))>=0)and ((float(sys.argv[2]))>=0):
	#前の許容秒数
	md=float(sys.argv[2])
	#後の許容秒数
	pd=float(sys.argv[3])
	
	#時間(秒)
	set_duration=float(sys.argv[4])
	duration=[]
	track=[]
	m3u=[]
	if((os.path.exists(sys.argv[1]))):
		path = pathlib.Path(sys.argv[1]).resolve()
		with open('audio_files.csv', 'r') as csv_file:
			reader = csv.DictReader(csv_file)
			for row in reader:
				duration.append((float(row['Duration'])))
				track.append([(row['Path']),(row['Duration'])])
	else:
		help()
		exit()
else:
	help()
	exit()

#参考：https://phst.hateblo.jp/entry/2022/01/17/080000
def get_integral_value_combination(items, target):
	def a(idx, l, r, t):
		p=t+(pd/(set_duration/3600))
		m=t-(md/(set_duration/3600))
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
set_duration_bak=set_duration
track_bak=track
retry=0#再試行回数。２０回でできないと判断。
while True:
	if ((set_duration)>0):
		items =(random.sample(list( set(duration) - set(result1) ), 20))#20個に分割 result1を引くことで重複回避
		if ((set_duration)<=3600) :
			#残りの長さが3600以下
			result0 = get_integral_value_combination(items, set_duration)
			result1=result1+(random.choice(result0))
			set_duration-=3600
		elif ((set_duration)>3600) :
			#残りの長さが3600以上
			result0 = get_integral_value_combination(items, 3600)
			result1=result1+(random.choice(result0))
			set_duration-=3600
		else:
			print("この条件では作成できません。")
	elif (set_duration<=0):
			#print(result1)#長さ一覧
			for dur in result1:
				track = np.array(track)
				ind=(np.argwhere(track==str(dur)))
				print(track[ind][0][0][0])#パス表示
				m3u.append(track[ind][0][0][0])
				random.shuffle(m3u)
				
			print("合計時間"+str(sum(result1))+"秒")#合計時間
			if (sum(result1)<=(set_duration_bak-md) or sum(result1)>=(set_duration_bak+pd)):#何故か時間が足りないor多いことがあるのでその場合はやり直す
				print("条件に合わないため、やり直します")
				result1=[]
				items=[]
				m3u=[]
				set_duration=set_duration_bak
				track=track_bak
				retry+=1
				if retry==20:
					print("20回再試行しましたが作成できませんでした。この条件では作成できません。")
					exit()
			else:
				#print("m3u")
				#print(m3u)
				with open(sys.argv[5], 'w') as m:
					for p in m3u:
						m.write("%s\n" % p)
				break
				print("終了します。")



