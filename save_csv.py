import os
import sys
import pathlib
import re
import csv
from pydub import AudioSegment
#既に存在するファイル
exist = []
#パス
if len(sys.argv) > 2:
	if((os.path.exists(sys.argv[1]))):
		path = pathlib.Path(sys.argv[1]).resolve()
		fieldnames = ['Path', 'Duration','Category','Tag','type']
		with open(sys.argv[2], 'a+') as csv_file:
			csv_file.seek(0)
			reader = csv.DictReader(csv_file)
			writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
			writer.writeheader()
			for row in reader:
				print(row['Path'])
				exist.append(row['Path'])
			for current_dir, sub_dirs, files_list in os.walk(path): 
				for file_name in files_list: 
					file_path=(os.path.join(current_dir,file_name))
					extension=(re.sub('.*\.', '', file_path))
					if file_path in exist:
						print(file_path+"は存在するため追加しません。")
					else:
						try:
							print(file_path+"を追加中...")
							sound = AudioSegment.from_file(file_path, extension)
							time = sound.duration_seconds # 再生時間(秒)
							print('再生時間：', time)
							writer.writerow({'Path': file_path, 'Duration': time})
						except Exception:
							pass
	else:
		print("使い方：python3 save_csv.py [音声ファイルが含まれているパス] [CSVファイル名]")
else:
	print("使い方：python3 save_csv.py [音声ファイルが含まれているパス] [CSVファイル名]")



    
    
