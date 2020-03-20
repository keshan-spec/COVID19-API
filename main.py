import requests
from bs4 import BeautifulSoup

URL = 'https://www.worldometers.info/coronavirus/'

def run():
    return BeautifulSoup(requests.get(URL).content, features="html.parser")

def get_updates():
    soup = run()
    infect_count = soup.find_all("div", {"class": "maincounter-number"})
    infect_count = [i.find('span').findAll(text=True)[0].strip() for i in infect_count]
    return {"Infected": infect_count[0], "Deaths": infect_count[1], "Recovered": infect_count[2]}


def search_country(country='Sri Lanka'):
    soup = run()
    table = soup.find('table', {'id': 'main_table_countries_today'})
    # get countries
    countries = []
    for i in table.findAll('tr'):
        for j in i.findAll('td'):
            countries.append(j.findAll(text=True)[0])
            break
    # pop the last item , that's just 'total :'
    countries.pop()


# print(get_updates())
search_country()