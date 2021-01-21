import re
import requests
from bs4 import BeautifulSoup
import pprint as p
import bs4

patterns = ['digital', 'phone', 'lines']
# patterns = ['digital', 'phone', 'Network', 'Internet',
# 'the\\sfirst(\\s\\w+){1,5}', 'messaging', 'connects', "commercially", 'commercial', '(home|personal)\\scomputers']
errors = []


def print_desc(desc, time, title):
    desc = desc.get_text()
    matches = []
    for i in patterns:
        pattern = re.compile(i, re.IGNORECASE)
        match = re.search(pattern, desc)
        if match:
            matches.append(match.group())
        else:
            pass
    if len(matches) > 0:
        print(matches)
        print(time)
        print(title)
        print(desc)
        print('-'*50)


# URL = 'https://www.computerhistory.org/timeline/computers/'
URL = 'https://www.computerhistory.org/timeline/networking-the-web/'

source = requests.get(URL)
src = source.content

soup = BeautifulSoup(src, 'html.parser')

time_box_catergories = soup.find(
    'div', {'id': 'chm-timeline-content-category'})
a = time_box_catergories.find_all(
    'a', class_='chm-category-timeline-section-year')
aval_times = [i.text for i in a]

period = input('Search Period?')
period = period.split('-')
time = [i for i in aval_times if (i >= period[0] and i <= period[1])]
d_type = []
for i in time:
    dtime = time_box_catergories.find('div', {'rel': i})
    if dtime:
        desc_section = dtime.select_one(
            'div.chm-category-timeline-section-content')
        desc_container = desc_section.find_all(
            'div', class_='chm-category-timeline-record')
        for container in desc_container:
            desc = container.select_one('div.description > p')
            title = container.a.h2.text
            print_desc(desc, i, title)
