import aiohttp
import asyncio
import urllib.parse
from urllib.parse import urlparse, parse_qs
import json
import re
import os
import requests
from bs4 import BeautifulSoup
import ssl


class Session:
    def __init__(self, token):
        self.token = token


async def login(url, token):
    # Send authentication request
    async with aiohttp.ClientSession() as session:
        url = f"{url}api/v1/auth/login"
        headers = {"User-Agent": "CTFer"}
        data = {
            "teamToken": token,
        }

        async with session.post(url, json=data, headers=headers, allow_redirects=False) as response:
            response_data = await response.json()
            token = response_data['data']['authToken']
            # print(response_data)
            # print(token)
            return Session(token=token)


def token_handling(token):
    parsed_token = urlparse(token)
    token = parse_qs(parsed_token.query)["token"][0]
    return urllib.parse.unquote(token)


async def main(url, token):
    # Authorize if needed
    session = await login(url, token)
    header = {"User-Agent": "Eruditus",
              "Authorization": "Bearer " + session.token}
    data = ["e3de660b-5bb2-4f6a-9456-43f7aa941478", 'squ1rrel{'+flag+"}"]
    payload = json.dumps(data)
    async with aiohttp.ClientSession(headers=header) as session:
        async with session.post(url='https://ctf.squ1rrel.dev/api/v1/challs/e3de660b-5bb2-4f6a-9456-43f7aa941478/submit', json={"flag": flag}, headers=header) as response:
            print(response)

if __name__ == "__main__":
    url = 'https://ctf.squ1rrel.dev/'
    token = 'https://ctf.squ1rrel.dev/login?token=uMsPnFCN8a5Hxj6ujqFerA88uFtPyqQeeNL8I%2FxwZbUkgq0%2B%2FaEGXtXZRWnkOIiK2YvkGD2%2FcOHdwuma1RH0MRFLsvcPLRuRG2CUnCOMwFzLzpHMSNmQO5jHMTZ3'
    flag = input('flag: ')
    token = token_handling(token)
    asyncio.run(main(url, token))
