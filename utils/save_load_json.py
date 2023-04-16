import json

JSON_FILE = "data/recent_logs.json"


def save_data_to_json(new_data, max_items=5):
    data_list = load_data_from_json()

    # リストの先頭に新しいデータを追加
    data_list.insert(0, new_data)

    # リストの要素数が最大値を超えた場合、古いデータを削除
    if len(data_list) > max_items:
        data_list = data_list[:max_items]

    # JSONファイルにデータを書き込む
    with open(JSON_FILE, "w") as f:
        json.dump(data_list, f)


def load_data_from_json():
    try:
        # JSONファイルが存在する場合、データを読み込む
        with open(JSON_FILE, "r") as f:
            data_list = json.load(f)
    except FileNotFoundError:
        # JSONファイルが存在しない場合、空のリストを返す
        data_list = []

    return data_list
