import requests
from bs4 import BeautifulSoup
import sys
import json

URL = "https://www.worldometers.info/coronavirus/"


def run():
    return BeautifulSoup(requests.get(URL).content, features="html.parser")


def get_updates():
    soup = run()
    infect_count = soup.find_all("div", {"class": "maincounter-number"})
    infect_count = [i.find("span").findAll(text=True)[0].strip() for i in infect_count]
    return json.dumps(
        {
            "Infected": infect_count[0],
            "Deaths": infect_count[1],
            "Recovered": infect_count[2],
        }
    )


def get_info_table():
    soup = run()
    table = soup.find("table", {"id": "main_table_countries_today"})
    tmp = []
    keys = [
        "Country",
        "Total Cases",
        "New Cases",
        "Total Deaths",
        "New Deaths",
        "Total Recovered",
        "New Recovered",
        "Active Cases",
    ]  # the keys of the table

    for tr in table.findAll("tr")[:-1]:
        if tr.has_attr("data-continent") == False:
            for td in tr.findAll("td")[1:9]:
                if td.has_attr("data-continent") == False:
                    try:
                        tmp.append(
                            td.find(text=True)
                            .strip()
                            .lower()
                            .replace(".", "")
                            .replace("-", "")
                            .replace(" ", "_")
                        )
                    except Exception as e:
                        tmp.append(td.find(text=True))
                        pass

    s, e = 0, len(keys)
    entries = []

    # Loop through the temp list and make a dict with every 9 items
    for _ in range(len(tmp) // len(keys)):
        d = dict(zip(keys, tmp[s:e]))
        if d:
            entries.append(d)
        s += len(keys)
        e += len(keys)
    return entries


def get_country(country, entries):
    for entry in entries:
        if country.lower() == entry["Country"]:
            return json.dumps(entry)
    return json.dumps(f"Unable to find {country}")


def get_stats(opt, entries):
    opts = {
        "death": "Total Deaths",
        "recovered": "Total Recovered",
        "cases": "Total Cases",
    }
    if opt not in opts.keys():
        return json.dumps({"Invalid option": opts})

    key = opts[opt]
    key_vals = {}
    for entry in entries:
        if entry[key]:
            if entry["Country"] != "world":
                key_vals[entry["Country"]] = int(entry[key].replace(",", ""))

    max_key = max(key_vals, key=key_vals.get)
    return json.dumps({max_key: key_vals[max_key]})


# check for args passed
if len(sys.argv) > 1:
    args = sys.argv[1:]
    if args[0] == "updates":
        print(get_updates())
    elif args[0] == "show":
        entries = get_info_table()
        if args[1] == "all":
            print(json.dumps(entries))
        else:
            print(get_country(args[1], entries))
    elif args[0] == "stats":
        entries = get_info_table()
        print(get_stats(args[1], entries))
else:
    print("No argument's passed, what do i do? ")
    entries = get_info_table()
    print(json.dumps(entries[0:2], indent=2))
