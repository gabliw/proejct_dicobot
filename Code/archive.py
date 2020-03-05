import json

# archive json file
def load_archive():
    with open("archive.json", encoding="utf8") as fp:
        data = json.load(fp)
    return data


def save_archive(data):
    with open("archive.json", "w", encoding="utf8") as fp:
        fp.write(json.dumps(data, ensure_ascii=False, indent=4))