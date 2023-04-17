from abc import ABC


class AbstractAPIClass(ABC):

    def __get_request(self, search_vacancy: str, page: int) -> list:
        pass

    def start_parse(self, keyword, pages) -> None:
        pass
