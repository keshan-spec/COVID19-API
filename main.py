import requests
from bs4 import BeautifulSoup
import sys
import json

URL = 'https://www.worldometers.info/coronavirus/'


def run():
    return BeautifulSoup(requests.get(URL).content, features="html.parser")


def get_updates():
    soup = run()
    infect_count = soup.find_all("div", {"class": "maincounter-number"})
    infect_count = [i.find('span').findAll(text=True)[0].strip() for i in infect_count]
    return json.dumps({"Infected": infect_count[0], "Deaths": infect_count[1], "Recovered": infect_count[2]})


def get_info_table():
    soup = run()
    table = soup.find('table', {'id': 'main_table_countries_today'})
    tmp = []
    keys = ['Country', 'Total Cases', 'New Cases', 'Total Deaths', 'New Deaths',
            'Total Recovered', 'Active Cases', 'Serious', 'Tot']  # the keys of the table

    for tr in table.findAll('tr'):
        for td in tr.findAll('td'):
            try:
                tmp.append(td.find(text=True).strip())
            except Exception:
                tmp.append(td.find(text=True))
                pass
    tmp.pop()  # pop the last item , that's just 'total :'
    s, e = 0, 9
    entries = []

    # Loop through the temp list and make a dict with every 9 items
    for x in range(len(tmp) // 9):
        entries.append(dict(zip(keys, tmp[s:e])))
        s += 9
        e += 9


# check for args passed
if len(sys.argv) > 1:
    args = sys.argv[1:]
    if args[0] == "updates":
        print(get_updates())
else:
    print("No argument's passed, what do i do? ")

