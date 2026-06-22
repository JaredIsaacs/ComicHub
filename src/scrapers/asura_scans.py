"""Scraper class for scraping comics for asurascans.com"""

from bs4 import BeautifulSoup

from src.scrapers.scraper import Scraper
from src.scrapers.comic import Comic

class AsuraScans(Scraper):
    """Represents a Scraper object designed specifically to scrape the Asura Scans website."""

    def __init__(self, base_url):
        super().__init__(base_url)
        self.name = "Asura Scans"

    def get_all_comics(self) -> list[Comic]:
        '''
        Class designed to gather all the comics, but not on a deep level.
        Wont gather any non essential data for the dataclass.
        '''
        page = 1
        comics = []

        while True:
            response = self.session.get(f"{self.base_url}/browse?page={page}")
            soup = BeautifulSoup(response.content, features="lxml")

            series_grid = soup.find(id="series-grid")
            try:
                links = series_grid.find_all('a', class_=['block', 'relative',
                                                        'aspect-[3/4]', 'overflow-hidden'])
                for l in links:
                    name = l.img.get('alt', 'No Title')
                    cover = l.img.get('src', 'No Cover Image')
                    url = l.get('href', 'No Href')

                    slug = url.split('/')[-1]

                    comics.append(Comic(self, name, cover, slug))
            except AttributeError:
                break
            page += 1

        return comics

    def get_comic(self, slug: str) -> Comic:
        '''
        Class used to gather comic details that are important for the Scraper table.
        '''
        url = f"{self.base_url}/comics/{slug}"
        response = self.session.get(url)

        if response.status_code == 404:
            return None

        soup = BeautifulSoup(response.content, features="lxml")

        cover_image_tag = soup.find('img', id='cover-viewer-img')

        name = cover_image_tag.get("alt", "No Title")
        cover_image_url = cover_image_tag.get("data-full-src", "No Cover Image")
        status = soup.find("span", class_=["text-[#A78BFA]"]).text.strip()
        chapter_count = soup.find('span', class_=[
            "from-[#48C855]", "to-[#C6FFAB]"
            ]).text.strip()

        return Comic(self, name, cover_image_url, slug, chapter_count, status)


if __name__ == "__main__":
    scraper = AsuraScans("asurascans.com")
    comic = scraper.get_comic("a-dragonslayers-peerless-regression-7b57f74d")
    print('stop')
