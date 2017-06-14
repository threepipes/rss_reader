import json
import feedparser as fp


def contains_word(word_list, sentence):
    for word in word_list:
        if word in sentence:
            return True
    return False


def filtering(entries, whitelist=[], blacklist=[]):
    entry_flt = []
    for entry in entries:
        title = entry['title']
        if blacklist and contains_word(blacklist, title):
            continue
        if whitelist and not contains_word(whitelist, title):
            continue
        entry_flt.append(entry)
    return entry_flt


def get_entries(rss_info):
    if not 'url' in rss_info:
        print('no url in information')
        return []
    url = rss_info['url']
    news_dic = fp.parse(url)

    whitelist = []
    blacklist = []
    if 'white' in rss_info:
        whitelist = rss_info['white']
    if 'black' in rss_info:
        blacklist = rss_info['black']
    return filtering(news_dic.entries, whitelist, blacklist)


disp_key = [
    'title',
    'published',
    'link',
]


def read_rss():
    """
    site_data.jsonに登録されているRSSのトピックを返す
    フィルタリング済み
    [title, published, link]の3つを含む(+additionalで指定したもの)
    """

    with open('site_data.json', encoding='utf-8') as f:
        site_data = json.load(f)

    rss_list = []
    for data in site_data:
        for entry in get_entries(data)[:50]:
            key_set = disp_key
            if 'additional' in data:
                key_set += data['additional']
            item = {}
            for key in disp_key:
                if key in entry:
                    item[key] = entry[key]
                else:
                    item[key] = ''
            rss_list.append(item)
    return rss_list


if __name__ == '__main__':
    rss_list = read_rss()
    for entry in rss_list:
        for key, value in entry:
            print(key, value)
