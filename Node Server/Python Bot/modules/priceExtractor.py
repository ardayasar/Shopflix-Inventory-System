import requests
import json
import re


WEB_HDRS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
    'Accept': 'text/html,text/plain,application/xhtml+xml,application/xml,application/_json;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Charset': 'Windows-1252,utf-8;q=0.7,*;q=0.3',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'tr-TR,en;q=0.8;q=0.5',
    'Connection': 'keep-alive'
}


class priceExtractor:

    def __init__(self):
        print('Extractor started')

    def trendyol(self, link):
        try:
            response = requests.get(link)
            data = response.text
            match = re.search(r'(?<=type=application/ld\+json>)(.*)(?=</script>)', data)
            json_data = match.group(0).replace('@', '').replace('https://schema.org/', '')
            result = json.loads(json_data)

            del result['context']
            result['image'] = result['image'][0].split(',')

            return result
        except Exception as error:
            print(error)
            return False

    def hepsiburada(self, link):
        try:
            response = requests.get(link, headers=WEB_HDRS)
            data = response.text.strip()
            result = re.search(r'<script[^>]+?type="application\/ld\+json"[^>]*?>(.*?)<\/script>', data, re.DOTALL)
            result = result.group(0).replace('@', '').replace('https://schema.org/', '').replace('<script type="application/ld+json">', '').replace('</script>', '').strip()
            result = json.loads(result)

            del result['context']

            return result
        except Exception as error:
            print(error)
            return False

    def n11(self, link):
        try:
            response = requests.get(link, headers=WEB_HDRS)
            data = response.text.strip()
            resk = None
            result = re.findall(r'<script[^>]+?type="application\/ld\+json"[^>]*?>(.*?)<\/script>', data, re.DOTALL)
            for regex_data in result:
                gkh = json.loads(regex_data.replace('@', '').replace('https://schema.org/', '').replace(
                '<script type="application/ld+json">', '').replace('</script>', '').strip())
                if 'offers' in gkh:
                    resk = gkh


            del resk['context']

            return resk
        except Exception as error:
            print(error)
            return False
