from src.HeadHunterAPIparse import HeadHunterApi, HHVacancyInterface


#: Создаем экземпляр класса АПИ. Можем через запятую передать ключевые слова в вакансии
hh_api_instance = HeadHunterApi("python, Python разработчик")

#: Создаем интерфейс для работы со списком полученных вакансий
hh_vacancy_interface = HHVacancyInterface(hh_api_instance)

#: Заполняем список вакансий полученной информацией
hh_vacancy_interface.fill_vacancy_list()


#: Можно получить список вакансий либо в виде списка, либо в виде словаря
# print(hh_vacancy_interface.dict_of_vacancies)
# print(hh_vacancy_interface.list_of_vacancies)

#: Также можно вывести краткую информацию по всем полученным вакансиям
print(hh_vacancy_interface.show_vacancies)

#: Можно получить более подробную информацию по конкретной вакансии
# print(hh_vacancy_interface.get_full_information_by_id(78431357))