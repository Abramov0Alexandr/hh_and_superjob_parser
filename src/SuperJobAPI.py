import json
import pprint
import datetime
import requests


class SuperJobParser:

    URL = "https://api.superjob.ru/2.0/vacancies/?"

    def __init__(self):

        self.__vacancies_list = []

    def __get_request(self, vacancy_for_search, preferred_city, pages_for_parse=1):

        header = {
            'X-Api-App-Id': 'v3.r.137491480.efc206e4525fb50a0bc91e6c0ecff6cec64b1fdb.20452df5d70be14cfb657a43773b962c328135b5'
        }

        params = {'keywords': vacancy_for_search.title(),
                  'town': preferred_city,
                  'count': 3,
                  'page': pages_for_parse}

        return requests.get(self.URL, headers=header, params=params).json()['objects']

    def start_parse(self, vacancy_for_search: str, preferred_city: str, pages_for_parse=2) -> None:
        current_page = 0

        for i in range(pages_for_parse):
            current_page += 1
            print(f"Парсинг страницы {i + 1}", end=': ')
            values = self.__get_request(vacancy_for_search, preferred_city, i)
            print(f"Найдено {len(values)} вакансий")
            self.__vacancies_list.extend(values)

    @property
    def get_vacancies(self):
        return self.__vacancies_list


sj = SuperJobParser()
sj.start_parse('python', 'Москва')

pprint.pprint(sj.get_vacancies)



header = {
    'X-Api-App-Id': 'v3.r.137491480.efc206e4525fb50a0bc91e6c0ecff6cec64b1fdb.20452df5d70be14cfb657a43773b962c328135b5'
}

params = {'keywords': 'Python',
          'town': 'Москва',
          'count': 2,
          'page': 1}



url = "https://api.superjob.ru/2.0/vacancies/?"

test = requests.get(url, headers=header, params=params).json()['objects']


vac_list = []

for i in test:

    text_splitter = 'Информация окончена'
    raw_date_published = i['date_published']
    pre_formatted_date = datetime.datetime.fromtimestamp(raw_date_published)
    final_date = pre_formatted_date.strftime('%Y-%m-%d %H:%M:%S')

    vac_list.append(f"Дата размещения вакансии: {final_date}. \n"
                    f"ID Вакансии: {i['id']}.\n"
                    f"Наименование вакансии: {i['profession']}. \n"
                    f"Заработная плата: от {i['payment_from']} до {i['payment_to']}. \n"
                    f"Адрес: {i.get('address')}. \n"
                    f"Требование к кандидату: {i.get('candidat')}. \n"
                    f"Описание вакансии: {i.get('work')}. \n"
                    f"Ссылка на вакансию: {i['link']}.\n"
                    f"{text_splitter:.^100}\n")

# print(*[i for i in vac_list])

