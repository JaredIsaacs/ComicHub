import json

from requests import get
from bs4 import BeautifulSoup

from Scraper import Scraper
from Comic import Comic

class MangaBall(Scraper):
    def __init__(self, base_url):
        super().__init__(base_url)

        self.api_headers = {
            "X-CSRF-Token": "",
            "Referer": f"{self.base_url}/",
            "Origin": self.base_url,
            "X-Requested-With": "XMLHttpRequest",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        self._init_csrf()


    def _init_csrf(self) -> None:
        """Fetch the homepage and extract the CSRF token from the meta tag."""
        resp = self.session.get(self.base_url, headers=self.api_headers, timeout=15)
        resp.raise_for_status()

        soup = BeautifulSoup(resp.text, "lxml")
        meta = soup.find("meta", {"name": "csrf-token"})

        if not meta or not meta.get("content"):
            raise RuntimeError("CSRF token not found on homepage")

        self.api_headers['X-CSRF-Token'] = meta["content"]


    def _refresh_csrf(self) -> None:
        self._init_csrf()


    def get_all_comics(self) -> list[Comic]:
        comics = []
        url = f"{self.base_url}/api/v1/title/search-advanced/"
        payload = {'filters[page]': 1}

        response = self.session.post(url, headers=self.api_headers, data=payload)
        data = response.json()

        while data['pagination']['current_page'] != data['pagination']['last_page']:
            payload['filters[page]'] += 1
            response = self.session.post(url, headers=self.api_headers, data=payload)

            if response.status_code in (403, 419) or "csrf" in response.text.lower():
                self._refresh_csrf()
                response = self.session.post(url, headers=self.api_headers, data=payload)


    def get_comic(self, title: str) -> Comic:
        pass