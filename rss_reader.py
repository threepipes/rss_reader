import feedparser as fp
import json

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
    url = data['url']
    news_dic = fp.parse(url)

    whitelist = []
    blacklist = []
    if 'white' in rss_info:
        whitelist = rss_info['white']
    if 'black' in rss_info:
        blacklist = rss_info['black']
    return filtering(news_dic.entries, whitelist, blacklist)


with open('site_data.json', encoding='utf-8') as f:
    site_data = json.load(f)

disp_key = [
    'title',
    'published',
    'link',
]

for data in site_data:
    for entry in get_entries(data)[:10]:
        key_set = disp_key
        if 'additional' in data:
            key_set += data['additional']
        for key in disp_key:
            if key in entry:
                print(entry[key])
        print()
