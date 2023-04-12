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

        params = {"text": search_vacancy,
                  "page": page,
                  "per_page": 100
                  }
        return requests.get(self.__base_url, params=params).json()['items']

    def start_parse(self, keyword: str, pages=10) -> None:
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
        return self.__vacancies_list


class HeadHunterVacancyInterface:

    def __init__(self, keyword: str):
        self.__filename = f"{keyword.title().strip()}.json"

    def create_json_array(self, data: list) -> str | None:
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
        result_info = []

        with open(self.__filename, encoding='utf-8') as file:
            vacancies = json.load(file)

        for i in vacancies:
            if i['salary']['to'] is None:
                i['salary']['to'] = "Максимальный порог не указан"

            if i['salary']['from'] is None:
                i['salary']['from'] = "Начальная з/п не указана"

            result_info.append(f"ID вакансии: {i['id']}. "
                               f"Наименование вакансии: {i['name']}. "
                               f"Заработная плата({i['salary']['currency']}): {i['salary']['from']} - {i['salary']['to']}. "
                               f"Ссылка на вакансию: {i['alternate_url']}.")

        return '\n'.join(result_info)

    def get_full_information_by_id(self, id: str | int) -> str:
        result_info = []

        with open(self.__filename, encoding='utf-8') as file:
            vacancies = json.load(file)

            for i in vacancies:

                if i['id'] == str(id):
                    if i.get('address') is None:
                        address_info = 'адрес не указан'
                    else:
                        address_info = f"{i['address']['city']} {i['address']['street']} {i['address']['building']}"

                    result_info.append(f"Вакансия: {i['name']}. "
                                       f"Наименование организации {i['employer']['name']}. "
                                       f"Адрес офиса: {address_info}. "
                                       f"Требования к кандидату: {i['snippet']['requirement']}. "
                                       f"Основные задачи: {i['snippet']['responsibility']}. "
                                       f"Заработная плата({i['salary']['currency']}): {i['salary']['from']} - {i['salary']['to']}. "
                                       f"Ссылка на вакансию: {i['alternate_url']}.")

                    return '\n'.join(result_info)
        return 'Вакансии по такому ID не найдено'
