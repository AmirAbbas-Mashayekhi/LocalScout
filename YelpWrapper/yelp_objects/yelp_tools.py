from dataclasses import dataclass
import requests


@dataclass
class YelpClientWrapper:
    url: str
    api_key: str
    limit: int = 20
    sort_by: str = "best_match"

    @property
    def base_url(self):
        return "https://api.yelp.com/v3/"

    @property
    def filters(self):
        return ("best_math", "distance", "rating", "review_count")


class YelpBusinessSearcher:
    def __init__(self, yelp_client: YelpClientWrapper):
        self.yelp_client = yelp_client
        self.__filters = f"?sort_by={yelp_client.sort_by}&limit={yelp_client.limit}"
        self.url = yelp_client.base_url + yelp_client.url + self.__filters
        self.api_key = yelp_client.api_key
        self.__headers = {"Authorization": f"Bearer {yelp_client.api_key}"}

    def show_available_filters(self):
        return self.yelp_client.filters

    def search(self, location: str, term: str, top_result=False) -> list[dict]:
        params = {"term": term, "location": location}
        response = requests.get(
            url=self.url,
            headers=self.__headers,
            params=params,
        )
        if top_result:
            return response.json()["businesses"][0]
        return response.json()["businesses"]
