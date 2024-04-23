from curl_cffi import requests
import re

ep = "https://www.airbnb.com"

regx_api_key = re.compile(r'"key":".+?"')

def get(proxy_url: str) -> str:
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Language": "en",
        "Cache-Control": "no-cache",
        "Pragma": "no-cache",
        "Sec-Ch-Ua": '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": '"Windows"',
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    session = requests.Session()
    session.headers.update(headers)
    if proxy_url:
        session.proxies.update({'http': proxy_url, 'https': proxy_url})

    response = session.get(ep, timeout=60)  
    response.raise_for_status() 

    body = response.text
    api_key = regx_api_key.search(body).group()
    api_key = api_key.replace('"key":"', '')
    api_key = api_key.replace('"', "")
    return api_key
