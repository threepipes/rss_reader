import json
import os
import hashlib
from rss_reader import read_rss

rss_history = 'history.json'


def make_table(rss_list):
    table = {}
    for entry in rss_list:
        key = entry['title'] + entry['published']
        key = key.encode('utf-8')
        table[hashlib.md5(key).hexdigest()] = entry
    return table


def reduce_list(rss_list):
    """
    rss_listのうち，history.jsonに存在するトピックを除外
    publishedでソートして返す
    """
    if not os.path.exists(rss_history):
        with open(rss_history, 'w', encoding='utf-8') as f:
            json.dump(rss_list, f)
        return sorted(rss_list, key=lambda x: x['published'])
    with open(rss_history, encoding='utf-8') as f:
        history = json.load(f)
    table = make_table(rss_list)
    with open(rss_history, 'w', encoding='utf-8') as f:
        json.dump(rss_list, f)
    for old_entry in history:
        key = old_entry['title'] + old_entry['published']
        key = key.encode('utf-8')
        md5_hash = hashlib.md5(key).hexdigest()
        if md5_hash in table:
            del table[md5_hash]
    return sorted(table.values(), key=lambda x: x['published'])


def get_newests():
    rss_list = read_rss()
    return reduce_list(rss_list)


if __name__ == '__main__':
    print(get_newests())
