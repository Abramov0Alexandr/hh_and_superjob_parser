import json
import os.path
import pprint
import datetime
from operator import itemgetter
import requests


class SuperJobParser:

    URL = "https://api.superjob.ru/2.0/vacancies/?"

    def __init__(self):

        self.__vacancies_list = []

    def __get_request(self, vacancy_for_search: str, preferred_city: str, pages_for_parse=1) -> list:
        """
        Метод для финальной реализации парсинга,
        в качестве аргументов принимаются ключевое слово и кол-во страниц для парсинга,
        после передачи всех необходимых аргументов происходит парсинг,
        метод скрыт и используется в качестве финального шага.
        """

        header = {
            'X-Api-App-Id': 'v3.r.137491480.efc206e4525fb50a0bc91e6c0ecff6cec64b1fdb.20452df5d70be14cfb657a43773b962c328135b5'
        }

        params = {'keywords': vacancy_for_search.title(),
                  'town': preferred_city,
                  'count': 100,
                  'page': pages_for_parse,
                  'more': True}

        return requests.get(self.URL, headers=header, params=params).json()['objects']

    def start_parse(self, vacancy_for_search: str, preferred_city: str, pages_for_parse=10) -> None:
        """
        Метод используется в качестве настройки метода 'get_request'.
        В качестве аргумента метод принимает ключевое слово по поиску вакансии и количество страниц для парсинга.
        В дальнейшем, метод вызывает внутри себя 'get_request' и передает эти аргументы ему
        После получения всех данных, информация записывается в список 'vacancies_list'
        В конце выводится краткая информация о процессе
        """

        current_page = 0

        for i in range(pages_for_parse):
            current_page += 1
            print(f"Парсинг страницы {i + 1}", end=': ')
            values = self.__get_request(vacancy_for_search, preferred_city, i)
            print(f"Найдено {len(values)} вакансий")
            self.__vacancies_list.extend(values)

    @property
    def get_vacancies_list(self) -> list:
        """Метод для вывода или использования сырых собранных данных"""

        return self.__vacancies_list


class SuperJobVacancyInterface:

    def __init__(self, file_title: str):
        self.__file_title = f"{file_title.title().strip()}.json"

    def create_json_array(self, data: list):

        if not os.path.isfile(self.__file_title):
            self.__write_to_json_file(data)

        else:
            while True:
                answer = input(f"Файл с именем {self.__file_title} уже создан, перезаписать?"
                               f"\nВаш ответ(yes\\no): ").lower().strip()
                if answer == 'yes':
                    self.__write_to_json_file(data)
                    print('Информация в файле была перезаписана')
                    return
                elif answer == 'no':
                    print("Файл не перезаписан")
                    return
                else:
                    print("Некорректный ввод. Введите 'yes' или 'no'.")

    def show_all_vacancies(self) -> str:
        """Метод для вывода краткой информации о всех собранных вакансиях"""

        result_info = []

        for i in self.__data_from_json_file:

            salary_from = 'Начальная плата не указана' if i['payment_from'] == 0 else i['payment_from']
            salary_to = 'Максимальный порог не указан' if i['payment_to'] == 0 else i['payment_to']

            result_info.append(f"ID вакансии: {i['id']}. "
                               f"Наименование вакансии: {i['profession']}. "
                               f"Заработная плата({i['currency']}): {salary_from} - {salary_to}. "
                               f"Ссылка на вакансию: {i['link']}.")

        return '\n'.join(result_info)

    def get_full_information_by_id(self, id: str | int) -> str:
        """Метод для вывода более подробной информации о вакансии по ее ID"""

        result_info = []

        try:
            for i in self.__data_from_json_file:
                raw_date_published = i['date_published']
                pre_formatted_date = datetime.datetime.fromtimestamp(raw_date_published)
                final_date = pre_formatted_date.strftime('%Y-%m-%d %H:%M:%S')

                if i['id'] == int(id):
                    address_info = 'адрес не указан' if i.get('address') is None else i.get('address')

                    salary_from = 'начальная плата не указана' if i['payment_from'] == 0 else i['payment_from']
                    salary_to = 'максимальный порог не указан' if i['payment_to'] == 0 else i['payment_to']

                    result_info.append(f"Дата размещения вакансии: {final_date}. \n"
                                       f"ID Вакансии: {i['id']}.\n"
                                       f"Наименование вакансии: {i['profession']}. \n"
                                       f"Заработная плата({i['currency']}): от {salary_from} до {salary_to}. \n"
                                       f"Адрес: {address_info}. \n"
                                       f"Требование к кандидату: {i.get('candidat')}. \n"
                                       f"Описание вакансии: {i.get('work')}. \n"
                                       f"Ссылка на вакансию: {i['link']}.\n")

                    return ''.join(result_info)

            return 'Вакансии по такому ID не найдено'

        except ValueError:
            return 'Вакансии по такому ID не найдено'

    def top_ten_by_avg_salary(self):
        """
        Метод для вывода информации о топ 10 вакансиях по заработной плате.
        Метод выводит только те вакансии, в которых заработная плата указана в рублях
        """
        leaders_list = []

        for i in self.__data_from_json_file:
            salary_avg = (i['payment_from'] + i['payment_to']) / 2

            if i['payment_from'] == 0 or i['payment_to'] == 0 or i['currency'] != 'rub':
                continue

            else:
                leaders_list.append({"ID вакансии": i['id'],
                                     "Наименование вакансии": i['profession'],
                                     "Средняя заработная плата": salary_avg,
                                     "Ссылка на вакансию": {i['link']}})
        sorted_data = sorted(leaders_list, key=itemgetter("Средняя заработная плата"), reverse=True)
        pprint.pprint(sorted_data[:10], width=110)

    def __write_to_json_file(self, data: list):
        with open(self.__file_title, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

    @property
    def __data_from_json_file(self):
        """
        Метод для получения данных из записанного JSON файла.
        Метод служит для облегчения интерфейса класса
        """
        with open(self.__file_title, encoding='utf-8') as file:
            vacancies = json.load(file)
            return vacancies
