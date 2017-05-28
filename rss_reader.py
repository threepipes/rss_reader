import feedparser as fp
import json

with open('site_data.json', encoding='utf-8') as f:
    site_data = json.load(f)

disp_key = [
    'title',
    'published',
    'link',
]

for data in site_data:
    url = data['url']
    news_dic = fp.parse(url)

    for entry in news_dic.entries[:10]:
        for key in disp_key:
            if key in entry:
                print(entry[key])
        print()
