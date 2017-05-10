from urllib.parse import urlencode, urlparse, urljoin
from pprint import pprint
import requests

AUTHORIZE_URL = 'https://oauth.yandex.ru/authorize'
APP_ID = '3e3c424a05ec4c7a93b9e0c2e9f7b6e7'

auth_data = {
    'response_type': 'token',
    'client_id': APP_ID
}

print('?'.join((AUTHORIZE_URL, urlencode(auth_data))))


TOKEN = 'AQAAAAASdwmCAAQ-aLLvL5kPkUu5jO6N_PKx_3Q'


class YandexMetrika(object):
    _METRIKA_STAT_URL = 'https://api-metrika.yandex.ru/stat/v1/'
    _METRIKA_MANAGEMENT_URL = 'https://api-metrika.yandex.ru/management/v1/'
    token = None

    def __init__(self, token):
        self.token = token

    def get_header(self):
        return {
            'Content-Type': 'application/json',
            'Authorization': 'OAuth {}'.format(self.token),
            'User-Agent': 'asdasdasd'
        }

    def counter_list(self):
        url = urljoin(self._METRIKA_MANAGEMENT_URL, 'counters')
        headers = self.get_header()
        response = requests.get(url, headers=headers)
        counter_list = [c['id'] for c in response.json()['counters']]
        return counter_list

    def get_info(self, counter_id, metrics):
        url = urljoin(self._METRIKA_STAT_URL, 'data')
        headers = self.get_header()
        params = {
            'id': counter_id,
            'metrics': metrics
        }
        response = requests.get(url, params, headers=headers)
        output = int(response.json()['data'][0]['metrics'][0])
        return output

    def get_visits(self, counter_id):
        visits = self.get_info(counter_id, 'ym:s:visits')
        return visits

    def get_views(self, counter_id):
        views = self.get_info(counter_id, 'ym:pv:pageviews')
        return views

    def get_visitors(self, counter_id):
        visitors = self.get_info(counter_id, 'ym:pv:users')
        return visitors


metrika = YandexMetrika(TOKEN)

counters = metrika.counter_list()
print(counters)

print('Количество посещений: {}'.format(metrika.get_visits(counters[0])))
print('Количество просмотров: {}'.format(metrika.get_views(counters[0])))
print('Количество посетителей: {}'.format(metrika.get_visitors(counters[0])))
