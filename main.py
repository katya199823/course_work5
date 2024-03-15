from config import config
from src.DBManager import DBManager
from src.hh_API import HeadHunterData
from src.utils import print_vacancies


def main():
    while True:
        params = config()

        dbmanager = DBManager(params)

        dbmanager.create_connection('postgres')
        dbmanager.create_database('hh_parser')
        dbmanager.close_connection()

        hh_data = HeadHunterData()
        hh_data.get_employers()
        hh_data.new_employers_dicts()
        hh_data.get_vacancies_from_emp()
        hh_data.new_vacancies_dicts()

        dbmanager.create_connection('hh_parser')
        dbmanager.create_tables()
        dbmanager.insert_data(hh_data.new_emp_list, hh_data.new_vac_list)

        employers = dbmanager.get_companies_and_vacancies_count()
        vacancies = dbmanager.get_all_vacancies()
        average_salary = dbmanager.get_avg_salary()
        high_salary_vacancies = dbmanager.get_vacancies_with_higher_salary()
        dbmanager.close_connection()

        print('Перед вами есть задания для выполнения команд\n'
              'Выберите нужную команду, введя ее номер и нажмите "Enter":\n'
              '1. Отобразить компании и количество предлагаемых вакансий\n'
              '2. Отобразить все вакансии\n'
              '3. Отобразить среднюю З/П по всем вакансиям '
              '(не учитываются вакансии, где не отображена З/П)\n'
              '4. Показать список вакансий, где З/П выше средней по вакансиям\n'
              '5. Ввести ключевое слово для сортировки вакансий\n')

        user_input = input()

        if user_input == '1':
            for emp in employers:
                print(f'Наименование компании: {emp['Name']}')
                print(f'Количество предлагаемых вакансий: {emp['Vacancies_count']}\n')
            continue
        elif user_input == '2':
            print_vacancies(vacancies)
            continue
        elif user_input == '3':
            print(f'Средняя З/П по всем вакансиям - {average_salary}\n')
            continue
        elif user_input == '4':
            print_vacancies(high_salary_vacancies)
            continue
        elif user_input == '5':
            dbmanager.create_connection('hh_parser')
            user_keyword = input('Введите ключевое слово: ')
            kw_vacs = dbmanager.get_vacancies_with_keyword(user_keyword)
            print_vacancies(kw_vacs)
            dbmanager.close_connection()
            continue
        else:
            print('Вы ввели не верные данные\n'
                  'Хотите продолжить работу с программой? (д/н)')
            user_int = input()

            if user_int == 'д':
                continue
            else:
                break


if __name__ == '__main__':
    main()