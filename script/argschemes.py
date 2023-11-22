import argparse

ARGSCHEME = argparse.ArgumentParser()
ARGSCHEME.add_argument('src_dir', help='.datファイルを格納したディレクトリ')
ARGSCHEME.add_argument('-o', '--output_dir', help='.csvファイルの出力先ディレクトリ')
