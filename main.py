from src.HeadHunterAPIparse import HeadHunterAPI, HeadHunterVacancyInterface
from src.SuperJobAPI import SuperJobVacancyInterface, SuperJobParser
from src.user_interface_foos import user_interaction

if __name__ == '__main__':

    print('Приветствуем вас!\n'
          'Данная программа предназначена для парсинга вакансий на площадке Super Job и HeadHunter\n')

    necessary_platform = input('Пожалуйста, выберете один из доступных сервисов по его номеру:\n'
                               '1: Super Job\n'
                               '2: Head Hunter\n'
                               'Ожидание ввода: ').strip()
    while necessary_platform not in ('1', '2'):
        necessary_platform = input('Платформа не обнаружена, пожалуйста, повторите ввод: ').strip()

    if necessary_platform == '1':

        print('\nВы выбрали Super Job для поиска необходимых вакансий.\n'
              'Далее вам будет необходимо ввести уточняющую информацию для поиска\n')

        search_city = input('Введите город, по которому вы хотите произвести поиск вакансии: ').title().strip()

        while not search_city.replace(' ', '').isalpha():
            search_city = input('Название города должно быть строкового типа и не может быть пустым.\n'
                                'Пожалуйста, повторите ввод: ')

        print(user_interaction(SuperJobParser, SuperJobVacancyInterface, search_city))

    elif necessary_platform == '2':

        print('\nВы выбрали Head Hunter для поиска необходимых вакансий.\n'
              'Далее вам будет необходимо ввести уточняющую информацию для поиска\n')

        print(user_interaction(HeadHunterAPI, HeadHunterVacancyInterface))
