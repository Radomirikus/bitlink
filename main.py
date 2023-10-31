import requests
import os
from urllib.parse import urlparse
from dotenv import load_dotenv
import argparse


def shorten_link(token, link):
    
    payload = {
        "long_url" : link
    }
    headers = {
        "Authorization" : f"Bearer {token}"
    }
    url = 'https://api-ssl.bitly.com/v4/shorten'
    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    return response.json()["link"]


def count_clicks(token, link):
    headers = {
        "Authorization" : f"Bearer {token}"
    }
    link = urlparse(link)
    bitlink = f'{link.netloc}{link.path}'
    url = f"https://api-ssl.bitly.com/v4/bitlinks/{bitlink}/clicks/summary"
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()['total_clicks']


def is_bitlink(url, token):
    headers = {
        "Authorization" : token
    }
    url = urlparse(url)
    bitlink = f'{url.netloc}{url.path}'
    bitlink_url = f"https://api-ssl.bitly.com/v4/bitlinks/{bitlink}"
    response = requests.get(bitlink_url, headers=headers)
    return response.ok


def main():
    load_dotenv()
    parser = argparse.ArgumentParser(description='Делает ссылку короче и считает количество кликов')
    parser.add_argument('link', help=('Суда нада писат сылку катарую вы хатите сакратит'))
    args = parser.parse_args()
    link = args.link
    bitly_token = os.getenv("BITLY_TOKEN")
    try:
        if is_bitlink(link, bitly_token):
            print("По вашей ссылке прошли:", count_clicks(bitly_token, link), "раз(а)")
        else:
            bitlink = shorten_link(bitly_token, link)
            print("Битлинк: ", bitlink)
        
    except requests.exceptions.HTTPError:
        print("Неправильная ссылка")

if __name__ == "__main__":
    main()