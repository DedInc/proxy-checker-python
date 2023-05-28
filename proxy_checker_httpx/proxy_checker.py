import httpx
import random
import re
import json
import warnings
from httpx import Timeout
from urllib3.exceptions import InsecureRequestWarning
import asyncio

warnings.simplefilter("ignore", InsecureRequestWarning)

class ProxyChecker:
    def __init__(self):        
        self.proxy_judges = [
            'http://proxyjudge.us/azenv.php',
            'http://mojeip.net.pl/asdfa/azenv.php'
        ]

    async def initialize(self):
        self.ip = await self.get_ip()

    async def get_ip(self):
        r = await self.send_query(url='https://api.ipify.org/')

        if not r:
            return ""

        return r['response']

    async def detect_proxy_protocol(self, proxy):
        for protocol in ['http://', 'https://', 'socks4://', 'socks5://']:
            proxies = {protocol: proxy}
            try:
                async with httpx.AsyncClient(proxies=proxies, verify=False) as client:
                    response = await client.get(
                        random.choice(self.proxy_judges),
                        timeout=Timeout(5.0)
                    )
                    response.raise_for_status()
                return protocol
            except (httpx.HTTPError, httpx.RequestError) as e:
                continue
        return None

    async def send_query(self, proxy=False, url=None, user=None, password=None):
        if proxy:
            protocol = await self.detect_proxy_protocol(proxy)
            if protocol is None:
                return False
            proxies = {protocol: proxy}
        else:
            proxies = None

        auth = None
        if user is not None and password is not None:
            auth = (user, password)

        async with httpx.AsyncClient(proxies=proxies, auth=auth, verify=False) as client:
            try:
                response = await client.get(
                    url or random.choice(self.proxy_judges),
                    timeout=Timeout(5.0)                    
                )
                response.raise_for_status()
            except httpx.HTTPError as e:
                return False

            return {
                'timeout': int(response.elapsed.total_seconds() * 1000),
                'response': response.text
            }

    def parse_anonymity(self, r):
        if self.ip in r:
            return 'Transparent'

        privacy_headers = [
            'VIA',
            'X-FORWARDED-FOR',
            'X-FORWARDED',
            'FORWARDED-FOR',
            'FORWARDED-FOR-IP',
            'FORWARDED',
            'CLIENT-IP',
            'PROXY-CONNECTION'
        ]

        if any([header in r for header in privacy_headers]):
            return 'Anonymous'

        return 'Elite'

    async def get_country(self, ip):
        r = await self.send_query(url='https://ip2c.org/' + ip)

        if r and r['response'][0] == '1':
            r = r['response'].split(';')
            return [r[3], r[1]]

        return ['-', '-']

    async def check_proxy(self, proxy, check_country=True, check_address=False, user=None, password=None):
        protocols = {}
        timeout = 0

        proxy_url = 'http://' + proxy

        r = await self.send_query(proxy=proxy_url, user=user, password=password)

        if not r:
            return False

        protocols['http'] = r
        timeout += r['timeout']

        r = protocols['http']['response']

        if check_country:
            country = await self.get_country(proxy.split(':')[0])

        anonymity = self.parse_anonymity(r)

        timeout = timeout // len(protocols)

        if check_address:
            remote_regex = r'REMOTE_ADDR = (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
            remote_addr = re.search(remote_regex, r)
            if remote_addr:
                remote_addr = remote_addr.group(1)

        results = {
            'protocols': list(protocols.keys()),
            'anonymity': anonymity,
            'timeout': timeout
        }

        if check_country:
            results['country'] = country[0]
            results['country_code'] = country[1]

        if check_address:
            results['remote_address'] = remote_addr

        return results