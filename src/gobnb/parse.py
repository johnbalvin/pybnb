import re
import json
from bs4 import BeautifulSoup
from gobnb.standardize import standardize_details
from gobnb.utils import remove_space

regxApiKey = re.compile(r'"key":".+?"')
regexLanguage = re.compile(r'"language":".+?"')


def parse_body_details_wrapper(body:str):
    data_raw, language, api_key = parse_body_details(body)
    data_formatted = standardize_details(data_raw) 
    data_formatted["language"] = language
    price_dependency_input={
        "product_id": data_raw['variables']['id'],
        "impression_id": data_raw['variables']['pdpSectionsRequest']['p3ImpressionId'],
        "api_key": api_key
    }
    return data_formatted, price_dependency_input

def parse_body_details(body:str):
    soup = BeautifulSoup(body, 'html.parser')
    data_deferred_state = soup.select("#data-deferred-state-0")[0].getText()
    html_data = remove_space(data_deferred_state)
    language = regexLanguage.search(body).group()
    language = language.replace('"language":"', "")
    language = language.replace('"', "")
    api_key = regxApiKey.search(body).group()
    api_key = api_key.replace('"key":"', "")
    api_key = api_key.replace('"', "")
    data = json.loads(html_data)
    details_data = data["niobeMinimalClientData"][0][1]
    return details_data, language, api_key
