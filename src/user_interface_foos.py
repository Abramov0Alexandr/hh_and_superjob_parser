def user_interaction(api_instance, api_interface, city_for_search=None):

    class_instance = api_instance()

    available_commands = {1: "Показать сформированную краткую информацию о всех вакансиях",
                          2: "Получить расширенную информацию о вакансии по id",
                          3: "Показать топ 10 вакансий по средней заработной плате",
                          4: "Завершение программы и выход"}

    pretty_view_commands = '\n'.join([f"{key}: {value}" for key, value in available_commands.items()])

    while True:

        search_vacancy = input('Введите вакансию, по которой вы хотите произвести поиск: ').title().strip()
        while not search_vacancy.replace(' ', '').isalpha():
            search_vacancy = input('Название вакансии должно быть строкового типа: ').title().strip()

        pages_for_search = input('Введите количество страниц с которых необходимо произвести парсинг.\n'
                                 'По умолчанию значение установлено на 10 и является максимальным: ').strip()
        print()
        while not pages_for_search.isdigit() or int(pages_for_search) > 10:
            pages_for_search = input('Некорректное значение, повторите ввод: ').strip()

        if city_for_search is None:
            class_instance.start_parse(search_vacancy, int(pages_for_search))
        else:
            class_instance.start_parse(search_vacancy, city_for_search, int(pages_for_search))
        result_info = class_instance.get_vacancies_list

        filename = input("Введите название файла, для записи полученной информации в формате JSON: ").strip()
        while filename == '':
            filename = input("Название файла не может быть пустым, повторите ввод: ").strip()

        api_interface = api_interface(filename)
        api_interface.create_json_array(result_info)

        print("\nТеперь вам доступны следующие команды для отображения полученной информации:")
        print(pretty_view_commands)
        print("Чтобы вызвать команду, введите ее номер.\n"
              "Также с помощью команды 'Помощь' можно получить список доступных к вызову команд.")

        user_command = input("\nОжидание номера команды: ").title().strip()

        while user_command != '4':

            if user_command == 'Помощь':
                print(pretty_view_commands)

            if user_command == '1':
                print(api_interface.show_all_vacancies())

            if user_command == '2':
                search_id = input("Введите id вакансии, информацию о которой вы хотите получить.\n"
                                  "Чтобы узнать id вакансии, воспользуйтесь командой 1: в меню выбора команд.\n"
                                  "Ожидание ввода id: ").strip()

                print(api_interface.get_full_information_by_id(search_id))

            if user_command == "3":
                print('Ниже представлена информация о топ 10 вакансиях по заработной плате.\n'
                      'ВНИМАНИЕ, топ лист состоит из вакансий, в которых зарплата указана в РУБЛЯХ\n')
                api_interface.top_ten_by_avg_salary()

            elif user_command not in ('1', '2', '3', 'Помощь'):
                print('Команда не найдена, пожалуйста, повторите ввод')

            user_command = input("\nОжидание номера команды: ").title().strip()

        print(f"Работа успешно завершена, файл {filename.title()}.json находится в основной директории.\n"
              f"До свидания!")
        exit(0)
