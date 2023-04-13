from src.HeadHunterAPIparse import HeadHunterAPI, HeadHunterVacancyInterface

if __name__ == '__main__':
    hh_instance = HeadHunterAPI()

    available_commands = {1: "Показать сформированную краткую информацию о всех вакансиях",
                          2: "Получить расширенную информацию о вакансии по id",
                          3: "Показать топ 10 вакансий по средней заработной плате",
                          4: "Завершение программы и выход"}

    pretty_view_commands = '\n'.join([f"{key}: {value}" for key, value in available_commands.items()])

    while True:

        print('Приветствую, данная программа предназначена для парсинга вакансий HeadHunter\n')

        search_vacancy = input('Введите вакансию, по которой вы хотите произвести поиск: ').title().strip()
        while not search_vacancy.replace(' ', '').isalpha():
            search_vacancy = input('Название вакансии должно быть строкового типа: ')

        pages_for_search = input('Введите количество страниц с которых необходимо произвести парсинг.\n'
                                 'По умолчанию значение установлено на 10 и является максимальным: ').strip()
        print()

        while pages_for_search > '10' or pages_for_search.isalpha() or pages_for_search in '':

            pages_for_search = input("Введено некорректное значение, повторите попытку: ").strip()

        hh_instance.start_parse(search_vacancy, int(pages_for_search))
        result_info = hh_instance.get_vacancies_list

        filename = input("Введите название файла, для записи полученной информации в формате JSON: ")

        vacancy_interface = HeadHunterVacancyInterface(filename)
        vacancy_interface.create_json_array(result_info)  #: После создания файла, строчка не обязательна

        print("\nТеперь вам доступны следующие команды для отображения полученной информации:")
        print(pretty_view_commands)
        print("Чтобы вызвать команду, введите ее номер.\n"
              "Также с помощью команды 'Помощь' можно получить список доступных к вызову команд.")

        user_command = input("\nОжидание номера команды: ").title().strip()

        while user_command != '4':

            if user_command == 'Помощь':
                print(pretty_view_commands)

            if user_command == '1':
                print(vacancy_interface.show_all_vacancies())

            if user_command == '2':
                search_id = input("Введите id вакансии, информацию о которой вы хотите получить.\n"
                                  "Чтобы узнать id вакансии, воспользуйтесь командой 1: в меню выбора команд.\n"
                                  "Ожидание ввода id: ").strip()

                print(vacancy_interface.get_full_information_by_id(search_id))

            if user_command == "3":
                print('Ниже представлена информация о топ 10 вакансиях по заработной плате.\n'
                      'ВНИМАНИЕ, топ лист состоит из вакансий, в которых зарплата указана в РУБЛЯХ\n')
                vacancy_interface.top_ten_by_avg_salary()

            elif user_command not in ('1', '2', '3', 'Помощь'):
                print('Команда не найдена, пожалуйста, повторите ввод')

            user_command = input("\nОжидание номера команды: ").title().strip()

        print(f"Работа успешно завершена, файл {filename.title()}.json находится в основной директории.\n"
              f"До свидания!")
        exit(0)
