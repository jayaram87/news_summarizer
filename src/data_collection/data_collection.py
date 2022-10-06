from pynytimes import NYTAPI
from src.utils.util import read_yaml
from datetime import datetime, timedelta
import os

class NytAPI:
    def __int__(self, nbr_articles=1):
        #self.results = nbr_articles
        pass

    def __api_collection(self, secrets_config_path: str) -> str:
        secrets = read_yaml(secrets_config_path)
        ny_api = secrets['nytimes']['api']
        nyt = NYTAPI(ny_api, parse_dates=True)
        return nyt

    def news_article(self, section):
        secrets_path = os.path.join(os.getcwd(), 'config', 'secret.yaml')
        nyt = self.__api_collection(secrets_path)
        year = int(datetime.now().strftime('%Y'))
        month = int(datetime.now().strftime('%m'))
        day = int(datetime.now().strftime('%d'))
        print(year, month, day)

        top_science_stories = nyt.top_stories(section = section)
    
        """
        article = nyt.article_search(
            query = keyword,
            results = 1,
            dates = {
                "begin": datetime(2022, 1, 31),
                "end": datetime(year, month, day)
            },
            options = {
                "sort": "newest",
                "sources": [
                    "New York Times",
                    "AP",
                    "Reuters",
                    "International Herald Tribune"
                ],
                "news_desk": [section],
                "type_of_material": ["News Analysis"]
            }
        )
        """

        return top_science_stories

a=NytAPI()
print(a.news_article('Politics'))
