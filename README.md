# Auto\_playlist\_creator

指定時間に収まるm3u形式のプレイリストを自動生成します。

## 使い方

１，csvにパスと長さを登録

python3 save\_csv.py \[音声ファイルが含まれているパス\] \[CSVファイル名\]

2,csvから読み込んで作成

python3 ./create\_playlist.py \[CSVパス\] \[前許容秒数\] \[後許容秒数\] \[プレイリスト全体の秒数\] \[m3uファイル名\]

例：

長さ１時間。１０秒の無音、０秒の超過を許可。音声保存先./audio。CSVのパスaudio.csv。m3uファイル名playlist.m3u。

1,./audio以下のファイルを登録（新しいファイルを追加するたびに追加）

python3 save\_csv.py ./audio audio.csv

2,１時間=3600秒

python3 ./create\_playlist.py audio.csv 10 0 3600 playlist,m3u
