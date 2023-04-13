import json
import os
import requests
import datetime

from src.AbstractCLS import HeadHunterAPIAbstract


class HeadHunterAPI(HeadHunterAPIAbstract):

    __base_url = "https://api.hh.ru/vacancies?only_with_salary=true"

    def __init__(self):
        self.__vacancies_list = []

    def __get_request(self, search_vacancy: str, page: int) -> list:
        """
        Метод для финальной реализации парсинга,
        в качестве аргументов принимаются ключевое слово и кол-во страниц для парсинга,
        после передачи всех необходимых аргументов происходит парсинг,
        метод скрыт и используется в качестве финального шага.
        """

        params = {"text": search_vacancy,
                  "page": page,
                  "per_page": 100
                  }
        return requests.get(self.__base_url, params=params).json()['items']

    def start_parse(self, keyword: str, pages=10) -> None:
        """
        Метод используется в качестве настройки метода 'get_request'.
        В качестве аргумента метод принимает ключевое слово по поиску вакансии и количество страниц для парсинга.
        В дальнейшем, метод вызывает внитри себя 'get_request' и передает эти аргументы ему
        После получения всех данных, информация записывается в список 'vacancies_list'
        В конце выводится краткая информация о процессе
        """

        current_page = 0
        now = datetime.datetime.now()
        current_time = now.strftime(f"%d.%m.%Y Время: %X")

        for i in range(pages):
            current_page += 1
            print(f"Парсинг страницы {i + 1}", end=': ')
            values = self.__get_request(keyword, i)
            print(f"Найдено {len(values)} вакансий")
            self.__vacancies_list.extend(values)

        print(f"Парсинг окончен, собрано {len(self.__vacancies_list)} вакансий с {current_page} страниц\n"
              f"Информация собрана {current_time}\n")

    @property
    def get_vacancies_list(self):
        """Метод для вывода или использования сырых собранных данных"""

        return self.__vacancies_list


class HeadHunterVacancyInterface:

    def __init__(self, keyword: str):
        self.__filename = f"{keyword.title().strip()}.json"

    def create_json_array(self, data: list) -> str | None:
        """
        Метод для записи полученных в процессе парсинга данных в файл формата JSON.
        Также происходит дополнительная проверка, существует ли файл с таким же именем.
        В случае, если файл уже существует есть возможность перезаписать данные или оставить их.
        """

        if not os.path.isfile(self.__filename):
            with open(self.__filename, 'w', encoding='utf-8') as file:
                json.dump(data, file, indent=4, ensure_ascii=False)

        else:
            while True:
                answer = input(f"Файл с именем {self.__filename} уже создан, перезаписать?\nВаш ответ(yes\\no): ").lower().strip()
                if answer == 'yes':
                    with open(self.__filename, 'w', encoding='utf-8') as file:
                        json.dump(data, file, indent=4, ensure_ascii=False)
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

        with open(self.__filename, encoding='utf-8') as file:
            vacancies = json.load(file)

        for i in vacancies:

            salary_from = 'Начальная плата не указана' if not i['salary'].get('from') else i['salary'].get('from')
            salary_to = 'Максимальный порог не указан' if not i['salary'].get('to') else i['salary'].get('to')

            result_info.append(f"ID вакансии: {i['id']}. "
                               f"Наименование вакансии: {i['name']}. "
                               f"Заработная плата({i['salary']['currency']}): {salary_from} - {salary_to}. "                               
                               f"Ссылка на вакансию: {i['alternate_url']}.")

        return '\n'.join(result_info)

    def get_full_information_by_id(self, id: str | int) -> str:
        """Метод для вывода более подробной информации о вакансии по ее ID"""

        result_info = []

        with open(self.__filename, encoding='utf-8') as file:
            vacancies = json.load(file)

            for i in vacancies:

                if i['id'] == str(id):
                    if i.get('address') is None:
                        address_info = 'адрес не указан'
                    else:
                        address_info = f"{i['address']['city']} {i['address']['street']} {i['address']['building']}"

                    result_info.append(f"\nВакансия: {i['name']}.\n"
                                       f"Наименование организации {i['employer']['name']}.\n"
                                       f"Адрес офиса: {address_info}.\n"
                                       f"Требования к кандидату: {i['snippet']['requirement']}.\n"
                                       f"Основные задачи: {i['snippet']['responsibility']}.\n"
                                       f"Заработная плата({i['salary']['currency']}): {i['salary']['from']} - {i['salary']['to']}.\n"
                                       f"Ссылка на вакансию: {i['alternate_url']}.")

                    return ''.join(result_info)
        return 'Вакансии по такому ID не найдено'
