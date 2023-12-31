# 気象情報CSV化プログラム取扱説明書
[日本語](README-ja.md) | [English](./README.md)

## 動作確認済みの動作環境
- macOS, Python3.7.7
- Windows10, Python3.7.0
  - ※OSはいずれも64bit

## メインプログラム
`./script/dat2csv.py`がメインの処理が記述されたプログラムです。

## 使⽤⽅法
- 規定の形式・ファイル名の気象情報DATファイルを特定フォルダの直下に格納する
- シェル上で以下のコマンドにより処理を実⾏する  
`python ./script/dat2csv.py <DAT ファイルが保存されたフォルダへのパス>  出⼒先ディレクトリ（オプション）>`

### 実⾏例
```
# カレントディレクトリにある dat という名前のフォルダの中の DAT ファイルを変換し、
# カレントディレクトリに output_dir というフォルダを⽣成し CSV ファイルを出⼒する例
python ./script/dat2csv.py dat -o output_dir
```

出⼒先ディレクトリの指定はオプションなので省略する事ができます。

```
# 出⼒先を省略した場合メインプログラムと同じディレクトリに
# outputというディレクトリが⽣成されそこにCSVが出⼒されます
python ./script/dat2csv.py dat
```

### 出⼒例
1. ディレクトリ構造  
![fig1](https://github.com/wine-ai/dat2csv/assets/3130494/fbf01bdc-43de-4b49-8da1-e31937a0f090)

2. CSVファイル構造  
![fig2](https://github.com/wine-ai/dat2csv/assets/3130494/ac4bf981-015d-4ce7-bab8-6d161db31a40)

## その他
データ量が膨⼤なので、処理に時間がかかります（1978年〜2017年の全件処理で、概ね2時間程度）  
出⼒されるCSVファイルの⽂字コードはUTF-8です
