from abc import ABC


class AbstractAPIClass(ABC):

    def __get_request(self, search_vacancy: str, page: int) -> list:
        pass

    def start_parse(self, keyword: str, pages=10) -> None:
        pass


# class SuperJobVacancyInterface(ABC):
#
#     @abstractmethod
#     def create_json_array(self,  data: list):
#         pass
#
#     @abstractmethod
#     def write_to_json_file(self):
#         pass
