import requests
import datetime
from src.AbstractCLS import ParseCLS


class HeadHunterApi(ParseCLS):

    __base_url = "https://api.hh.ru/vacancies?only_with_salary=true"

    __slots__ = ("__error_logs", "__params", "__response", "__vacancies_list")

    def __init__(self, *args):
        self.__error_logs = []

        self.__params = {"text": args[:],
                         "page": 1,
                         "per_page": 20
                         }

        self.__response = requests.get(url=self.__base_url, params=self.__params)
        if self.__response.status_code == 200:
            self.__vacancies_list = self.__response.json()["items"]
        else:
            self.__error_logs.append(self.__response.status_code)
            print("Error: %s" % self.__response.status_code)

    def generate_vacancy(self):
        try:
            return self.__vacancies_list
        except AttributeError as e:
            return e

    @property
    def error_logs(self):
        return self.__error_logs


class HHVacancyInterface:

    def __init__(self, hh_instance: HeadHunterApi):
        self.__hh_instance = hh_instance
        self.__list_of_vacancies = []

        self.__now = datetime.datetime.now()
        self.__current_time = self.__now.strftime(f"%d.%m.%Y Время: %X")

    def fill_vacancy_list(self):

        try:
            for i in self.__hh_instance.generate_vacancy():
                if i['salary']['to'] is None:
                    i['salary']['to'] = "Максимальный порог не указан"

                if i['salary']['from'] is None:
                    i['salary']['from'] = "Начальная з/п не указана"

                self.__list_of_vacancies.append(f"ID вакансии: {i['id']}. "
                                                f"Наименование вакансии: {i['name']}. "
                                                f"Заработная плата: {i['salary']['from']} - {i['salary']['to']}. "
                                                f"Месторасположение: {i['area']['name']}. "
                                                f"Ссылка на вакансию: {i['alternate_url']}.")
            self.__list_of_vacancies.append(f"Время формирования запроса: {self.__current_time}")

        except TypeError as e:
            self.__hh_instance.error_logs.append(e)
            return e


    @property
    def show_vacancies(self):

        if len(self.__list_of_vacancies) == 0 and len(self.__hh_instance.error_logs) == 0:
            return 'Список вакансий пуст, чтобы заполнить его, воспользуйтесь методом "fill_vacancy_list"'

        if len(self.__hh_instance.error_logs) != 0:
            return f"{'Список задокументированных ошибок:'} {self.__hh_instance.error_logs}"

        return '\n'.join([i for i in self.__list_of_vacancies])

    @property
    def list_of_vacancies(self):
        if len(self.__list_of_vacancies) == 0:
            return 'Список вакансий пуст, чтобы заполнить его, воспользуйтесь методом "fill_vacancy_list"'

        return self.__list_of_vacancies[:-1]

    @property
    def dict_of_vacancies(self):

        test = self.__list_of_vacancies[:-1]
        result_data = []

        if len(self.__list_of_vacancies) == 0:
            return 'Список вакансий пуст, чтобы заполнить его, воспользуйтесь методом "fill_vacancy_list"'

        for i in test:
            vacancy_dict = {}
            part_of_dict = i.split('. ')

            for part in part_of_dict:
                key_value = part.split(': ')
                vacancy_dict[key_value[0]] = key_value[1]
            result_data.append(vacancy_dict)

        return result_data

    def get_full_information_by_id(self, id: str | int):

        result_info = []

        if len(self.__list_of_vacancies) == 0:
            return 'Список вакансий пуст, чтобы заполнить его, воспользуйтесь методом "fill_vacancy_list"'

        for i in self.__hh_instance.generate_vacancy():

            if i['salary']['to'] is None:
                i['salary']['to'] = "Максимальный порог не указан"

            if i['salary']['from'] is None:
                i['salary']['from'] = "Начальная з/п не указана"

            if str(id) == i['id']:
                if i['address'] is None:

                    result_info.append(f"Наименование вакансии: {i['name']}. "
                                       f"Заработная плата({i['salary']['currency']}): {i['salary']['from']} - {i['salary']['to']}. "
                                       f"Требования к кандидату: {i['snippet']['requirement']} "
                                       f"Обязанности: {i['snippet']['responsibility']} "
                                       f"Ссылка на вакансию: {i['alternate_url']}.")

                else:
                    result_info.append(f"Наименование вакансии: {i['name']}. "
                                       f"Заработная плата({i['salary']['currency']}): {i['salary']['to']} - {i['salary']['from']}. "
                                       f"Адрес офиса: {i['address']['city']} {i['address']['street']} {i['address']['building']}. "
                                       f"Требования к кандидату: {i['snippet']['requirement']} "
                                       f"Обязанности: {i['snippet']['responsibility']} "
                                       f"Ссылка на вакансию: {i['alternate_url']}.")

        return result_info
