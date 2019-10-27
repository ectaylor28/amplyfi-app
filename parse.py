import json
import os

# Empty output object
data_object = {
    "total_results": 0,
    "bigrams": {"raw_total": {}, "articles_total": {}},
    "trigrams": {"raw_total": {}, "articles_total": {}},
    "doctype": {},
    "year": {},
    "companies": {},
    "people": {},
    "places": {},
    "geo_loc": {}
}

# Map default key to readable key in output json
simple_key_pairs = {
    "m_szSourceType": "doctype",
    "m_szGeo1": "geo_loc",
    "m_Places": "places",
    "m_szYear": "year",
    "m_Companies": "companies"
}

# Same as above but combination of two arrays
complex_key_pairs = {
    "m_BiGrams": "bigrams",
    "m_TriGrams": "trigrams"
}


# Add or update value in dictionary
def add_value(dict, key, value=1):
    if key in dict:
        dict[key] += value
    else:
        dict[key] = value


path = "c://Users//Emily//Documents//App//data//JSON".rstrip("\r\n")

# Iterate through directory
for file in os.listdir(path):
    data_object["total_results"] += 1
    with open(os.path.join(path, file), "r", errors="ignore") as f:
        for line in f.readlines():
            json_data = json.loads(line)
            for key in simple_key_pairs:
                if key in json_data and key != ("m_BiGrams" or "m_BiCnt") and json_data[key] != "":
                    if type(json_data[key]) is list:
                        for item in json_data[key]:
                            add_value(data_object[simple_key_pairs[key]], item)
                    else:
                        add_value(data_object[simple_key_pairs[key]], json_data[key])
            for pairs in [["m_BiGrams", "m_BiCnt"], ["m_TriGrams", "m_TriCnt"]]:
                key_value = dict(zip(json_data[pairs[0]], json_data[pairs[1]]))
                for key in key_value:
                    add_value(data_object[complex_key_pairs[pairs[0]]]["articles_total"], key)
                    add_value(data_object[complex_key_pairs[pairs[0]]]["raw_total"], key, int(key_value[key]))

# Removing all with value of raw_total = 1 to decrease size of json


with open("data.json", "w") as d:
    json.dump(data_object, d)
