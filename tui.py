import constants
from datetime import datetime, timedelta

# Вводим данные, которые регулирует пользователь:
# общее количество автобусов и количество водителей
def get_param():
    done = False
    while not done:
        try:
            quantity_buses = int(input("Задайте суммарное количество автобусов: "))
            done = True
        except Exception:
            print("Введите, пожалуйста одно целое число без разделителей.")
    done = False
    while not done:
        try:
            quantity_drivers_8 = int(input("Задайте количество водителей, рабочий день которых 8 часов: "))
            done = True
        except Exception:
            print("Введите, пожалуйста одно целое число без разделителей.")
    done = False
    while not done:
        try:
            quantity_drivers_12 = int(input("Задайте количество водителей, рабочий день которых 12 часов: "))
            done = True
        except Exception:
            print("Введите, пожалуйста одно целое число без разделителей.")
    print("Данные приняты, начинается генерация расписания.")
    return([quantity_buses, quantity_drivers_8, quantity_drivers_12])

# Для читабельного вывода времени
def f_time(delta):
    base_time = datetime(2024, 1, 1) + delta
    return base_time.strftime("%H:%M")

# Распечатываем расписание в виде таблички
def print_schedule(weekly_schedule, day_index):
    print(f"Расписание на {constants.WEEK[day_index-1]}:")
    print(
        f"{'Номер автобуса':<15}{'Начало маршрута':<20}{'Конец маршрута':<20}{'Тип водителя':<15}{'ID водителя':<15}")
    for record in weekly_schedule[day_index-1]:
        print(
            f"{record['bus']:<15}{f_time(record['start_time']):<20}{f_time(record['end_time']):<20}{record['driver_type']:<15}{record['driver_id']:<15}")


def final_result(weekly_schedule):
    # Просмотр расписания через консольный ввод
    while True:
        print("\nВыберите вариант работы:")
        print("1-7: Расписание на выбранный день недели")
        print("-1: Выход")

        try:
            option = int(input("Введите номер варианта: "))
            if option == -1:
                print("Выход из программы.")
                break
            elif 1 <= option <= 7:
                print_schedule(weekly_schedule, option)
            else:
                print("Неверный номер варианта, пожалуйста, попробуйте снова.")
        except ValueError:
            print("Введите корректную цифру.")