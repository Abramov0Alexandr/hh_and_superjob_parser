import requests
import datetime
from AbstractCLS import ParseCLS


class HeadHunterApi(ParseCLS):

    base_url = "https://api.hh.ru/vacancies?only_with_salary=true"

    __slots__ = ("error_logs", "params", "response", "vacancies_list")

    def __init__(self, *args):
        self.error_logs = []

        self.params = {"text": args[:],
                       "page": 1,
                       "per_page": 20
                       }

        self.response = requests.get(url=self.base_url, params=self.params)
        if self.response.status_code == 200:
            self.vacancies_list = self.response.json()["items"]
        else:
            self.error_logs.append(self.response.status_code)
            print("Error: %s" % self.response.status_code)

    def generate_vacancy(self):
        try:
            return self.vacancies_list
        except AttributeError as e:
            return e


class HHVacancyInterface:

    def __init__(self, hh_instance: HeadHunterApi):
        self.hh_instance = hh_instance
        self.__list_of_vacancies = []

        self.__now = datetime.datetime.now()
        self.__current_time = self.__now.strftime(f"%d.%m.%Y Время: %X")

    def fill_vacancy_list(self):

        try:
            for i in self.hh_instance.generate_vacancy():
                if i['salary']['to'] is None:
                    i['salary']['to'] = "Максимальный порог не указан"

                if i['salary']['from'] is None:
                    i['salary']['from'] = "Начальная з/п не указана"

                self.__list_of_vacancies.append(f"Наименование вакансии: {i['name']}. "
                                                f"Месторасположение: {i['area']['name']}. "
                                                f"Заработная плата: {i['salary']['from']} - {i['salary']['to']}. "
                                                f"Ссылка на вакансию: {i['alternate_url']}.")
            self.__list_of_vacancies.append(f"Время формирования запроса: {self.__current_time}")

        except TypeError as e:
            self.hh_instance.error_logs.append(e)
            return e

    def vacancy_title(self):
        pass

    @property
    def show_vacancies(self):

        if len(self.__list_of_vacancies) != 0:
            return '\n'.join([i for i in self.__list_of_vacancies])

        if len(self.hh_instance.error_logs) != 0:
            return f"{'Список задокументированных ошибок:'} {self.hh_instance.error_logs}"

        elif len(self.__list_of_vacancies) == 0 and len(self.hh_instance.error_logs) == 0:
            return 'Список вакансий пуст, чтобы заполнить его, воспользуйтесь методом "fill_vacancy_list"'

    @property
    def list_of_vacancies(self):
        if len(self.__list_of_vacancies) == 0:
            return 'Список вакансий пуст, чтобы заполнить его, воспользуйтесь методом "fill_vacancy_list"'

        return self.__list_of_vacancies[:-1]




hh_api_instance = HeadHunterApi("Python разработчик")
hh_vacancy_interface = HHVacancyInterface(hh_api_instance)


hh_vacancy_interface.fill_vacancy_list()
# print()
print(hh_vacancy_interface.show_vacancies)
# print(hh_vacancy_interface.list_of_vacancies)
# print(hh_api_instance.vacancies_list[0])
print()





