from abc import ABC


class HeadHunterAPIAbstract(ABC):

    def __get_request(self, search_vacancy: str, page: int) -> list:
        pass

    def start_parse(self, keyword: str, pages=10) -> None:
        pass
