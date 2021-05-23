import datetime
from urllib.parse import urljoin

import requests_cache
from django.conf import settings


class FixerClient(object):
    base_url = "http://data.fixer.io/api/"
    access_key = getattr(settings, "FIXER_ACCESS_KEY", "")
    path = None
    extra_params = None

    def get_url(self):
        return urljoin(self.base_url, self.path)

    def get_params(self):
        return {**{'access_key': self.access_key}, **(self.extra_params or {})}

    def call(self):
        session = requests_cache.CachedSession('fixerio_cache')
        return session.get(self.get_url(), params=self.get_params())

    def latest(self, base=None, symbols=None):
        assert not symbols or type(symbols) == list
        self.path = "latest"
        if base:
            # TODO: This option is not FREE
            # self.extra_params = {**(self.extra_params or {}), **{'base': base}}
            pass
        if symbols:
            self.extra_params = {**(self.extra_params or {}), **{'symbols': ",".join(symbols)}}
        response = self.call()
        return response.json()

    def historical(self, date, base=None, symbols=None):
        assert not symbols or type(symbols) == list
        assert type(date) == datetime.date
        self.path = date.strftime("%Y-%m-%d")
        if base:
            # TODO: This option is not FREE
            # self.extra_params = {**(self.extra_params or {}), **{'base': base}}
            pass
        if symbols:
            self.extra_params = {**(self.extra_params or {}), **{'symbols': ",".join(symbols)}}
        response = self.call()
        return response.json()