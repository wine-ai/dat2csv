import os
import glob
import csv

# 最も古いデータ年
OLDEST_YEAR = 1978
NEWEST_YEAR = 2077

# データ種別とそのkey
DAT_KEY_VALUES = {
    "PR": "日降水量",
    "SD": "日照時間",
    "SR": "日積算日射量",
    "TM": "日平均気温",
    "TN": "日最低気温",
    "TX": "日最高気温",
}

# 気温に関する気象値のkey
TEMPERATURE_KEYS = ["TM", "TN", "TX"]

# 気温に関する気象値を氷点下と判定するかどうかの閾値
TEMPERATURE_THRESHOLD = 500


class Dat2Csv:
    def __init__(self):
        self.meshdatas = {}

    def get_key_from(self, datfile_path: str) -> str:
        """
        DATファイルの名前からデータ種別を取得

        Args:
            datfile_path (str): DATファイルへの絶対パス

        Returns:
            str: データ種別(DAT_KEY_VALUESに準ずる)
        """
        filename = os.path.basename(datfile_path)
        for key in DAT_KEY_VALUES:
            if key in filename:
                return key

        # ファイル名が不正な場合
        raise ValueError()

    def get_year_from(self, datfile_path: str) -> int:
        """
        DATファイルの名前からデータ年を取得

        Args:
            datfile_path (str): DATファイルへの絶対パス

        Returns:
            int: データ年
        """
        yy = datfile_path[-6:-4]
        if int("19" + yy) < OLDEST_YEAR:
            return int("20" + yy)
        else:
            return int("19" + yy)

    def read_datfile(self, datfile_path: str):
        """DATファイルからデータ読み込み

        Args:
            datfile_path (str): DATファイルへの絶対パス
        """
        # ファイル名からデータ種別と年を取得
        key = self.get_key_from(datfile_path)
        year = self.get_year_from(datfile_path)

        with open(datfile_path, mode='r', encoding='shift-jis') as d:
            lines = d.readlines()
            lines_count = len(lines)

            meshnum = ""
            meshdata = {}
            for i in range(1, lines_count):
                # DATファイルは13行で1周期
                # 1行目はメッシュコードなど
                # 2~13行目が1〜12月に対応している
                if i % 13 == 1:
                    meshnum = lines[i][0:8]
                    meshdata = {}
                    """
                    height = lines[i][8:12]
                    area_land = lines[i][12:16]
                    area_suiden = lines[i][16:20]
                    area_hata = lines[i][20:24]
                    area_kaju = lines[i][24:28]
                    area_shinrin = lines[i][28:32]
                    """
                else:
                    # 行単位の文字列を所定の位置で区切ってデータ整形
                    yyyy = str(year)
                    mm = lines[i][2:4].strip().zfill(2)
                    # 気象値は3文字ごとで区切る
                    values = [int(lines[i][j*3+4: j*3+7].strip())
                              for j in range((len(lines[i]) - 4) // 3)]
                    # 行ごとの気象値の数はその月の日数に等しい
                    for k in range(len(values)):
                        dd = str(k + 1).zfill(2)
                        yyyymmdd = yyyy + "-" + mm + "-" + dd
                        # 対象データが温度系の場合
                        if key in TEMPERATURE_KEYS:
                            if values[k] > TEMPERATURE_THRESHOLD:
                                values[k] -= 1000
                            values[k] = round(values[k] * 0.1, 1)
                        meshdata[yyyymmdd] = {DAT_KEY_VALUES[key]: values[k]}

                    if i % 13 == 0:
                        # クラスで保持している読み込み済みデータを、新たに読み込んだデータで更新
                        if self.meshdatas.get(meshnum) is None:
                            self.meshdatas[meshnum] = meshdata
                        else:
                            for key_ymd in meshdata:
                                if self.meshdatas[meshnum].get(key_ymd) is None:
                                    self.meshdatas[meshnum][key_ymd] = meshdata[key_ymd]
                                else:
                                    self.meshdatas[meshnum][key_ymd].update(
                                        meshdata[key_ymd])

    def write_csv(self, output_dir: str):
        """
        読み込んだデータすべてをCSVに書き出す
        出力形式：<出力先ディレクトリ>/<2次メッシュコード>/<3次メッシュコード>.csv

        Args:
            output_dir (str): CSV出力先ディレクトリ
        """

        for key_meshnum in self.meshdatas:
            # 上位の2次メッシュコードでフォルダ生成
            parent_mesh_dir = os.path.join(output_dir, key_meshnum[0:-2])
            os.makedirs(parent_mesh_dir, exist_ok=True)

            # CSV書き込み
            csv_path = os.path.join(parent_mesh_dir, key_meshnum + ".csv")
            write_mode = 'w'
            if os.path.exists(csv_path):
                write_mode = 'a'
            with open(csv_path, mode=write_mode, encoding='utf-8', newline="") as f:
                writer = csv.DictWriter(
                    f, ["年月日"] + list(DAT_KEY_VALUES.values()))
                if not write_mode == 'a':
                    writer.writeheader()

                # 年月日順に書き込み
                sorted_ymd_list = sorted(self.meshdatas[key_meshnum])
                for ymd in sorted_ymd_list:
                    self.meshdatas[key_meshnum][ymd].update({"年月日": ymd})
                    writer.writerow(self.meshdatas[key_meshnum][ymd])


def get_years(datfiles: list) -> list:
    """
    DATファイルのパス配列から、重複なしの年数リストを取得する
    ここで得られる年数は、2078など-100する必要がある文字列そのまま
    順序は実際の年数順にソートして返す（2078,2079...2000,2001...)
    Args:
        datfiles (list): [description]

    Returns:
        list: [description]
    """
    years = []
    for datfile in datfiles:
        years.append(datfile[-8:-4])
    years = sorted(list(set(years)))

    index = 0
    for i in range(len(years)):
        if int(years[i]) > NEWEST_YEAR:
            index = i
            break
    if index > 0:
        return years[index:] + years[0:index]
    else:
        return years


if __name__ == "__main__":
    # コマンド初期化
    print("initalizing...")
    import argschemes
    args = argschemes.ARGSCHEME.parse_args()

    # datファイル保存先は必須、csv出力先はオプション
    src_dir = args.src_dir
    output_dir = args.output_dir

    # csv出力先が指定されていない場合本スクリプトと同じディレクトリにoutputフォルダを生成し保存
    if output_dir is None:
        output_dir = os.path.join(os.path.dirname(__file__), "output")
        os.makedirs(output_dir, exist_ok=True)
    else:
        if os.path.exists(output_dir):
            raise Exception('出力先フォルダが既に存在します')

    # 指定ディレクトリ内のdatファイルすべてを取得
    datfile_paths = glob.glob(os.path.join(src_dir, "*.dat"))

    # DATファイルの配列からすべての年数を取得
    years = get_years(datfile_paths)
    print(str(len(years)) + " years found")

    # 1年単位で読み込み->CSV書き込みを行う
    for index, year in enumerate(years):
        print(str(index + 1) + '/' + str(len(years)) + ':' + year)
        datfile_paths_of_year = [
            os.path.join(src_dir, 'MSPR' + year + '.dat'),
            os.path.join(src_dir, 'MSSD' + year + '.dat'),
            os.path.join(src_dir, 'MSSR' + year + '.dat'),
            os.path.join(src_dir, 'MSTM' + year + '.dat'),
            os.path.join(src_dir, 'MSTN' + year + '.dat'),
            os.path.join(src_dir, 'MSTX' + year + '.dat'),
        ]
        d2c = Dat2Csv()
        for path in datfile_paths_of_year:
            if not os.path.exists(path):
                print(path + 'は存在しません、スキップします…')
                continue
            print('loading:' + path)
            d2c.read_datfile(path)
        print('writing...')
        d2c.write_csv(output_dir)

    print("done")
