from datetime import datetime, timedelta
import random
import tui
import constants


def peak_hour(now, is_weekend):
    if is_weekend:
        return False
    hour = now.seconds // 3600
    return any(start <= hour < end for start, end in constants.PEAK_HOURS)


def generate_schedule(num_buses, drivers_type_a, drivers_type_b):
    # Создаем cписок расписаний для каждого дня недели
    weekly_schedule = []

    driver_b_work_days = {}
    for i in range(drivers_type_b):
        # Водители 2 сдвигаются по дням недели для равномерной нагрузки
        start_day = i % 3
        # Создает ID водителя, например 11,12, где первая цифра всегда тип водителя, а вторая номер
        driver_b_work_days[f"{constants.DRIVER_12_HOUR}{i + 1}"] = [
            constants.WEEK[j] for j in range(start_day, len(constants.WEEK), 3)
        ]

    for day_index, day in enumerate(constants.WEEK):
        is_weekend = day in ["СБ", "ВС"]
        schedule = []
        now = timedelta(hours=constants.WORKING_DAY_BEGINS)

        driver_next_free_time = {
            constants.DRIVER_8_HOUR: [timedelta(hours=8)] * drivers_type_a if not is_weekend else [], #водители типа 1 свободны всегда с 8 утра
            constants.DRIVER_12_HOUR: [timedelta(hours=0)] * drivers_type_b, #доступны всегда с начала до конца
        }
        bus_next_free_time = [now] * num_buses

        # Список для проверки расписания обедов водителей типа 1
        driver_lunch_taken = [False] * drivers_type_a

        while now < timedelta(hours=constants.WORKING_DAY_ENDS):
            required_buses = int(num_buses * (constants.PEAK_LOAD if peak_hour(now, is_weekend) else constants.NORMAL_LOAD))
            active_buses = sum(  1 for entry in schedule
                                 if entry["start_time"] <= now and entry["end_time"] > now)

            for bus in range(num_buses):
                if bus_next_free_time[bus] <= now and active_buses < required_buses:
                    driver_type, driver_id = None, None

                    #пытаемся найти водителя типа 1
                    for i, free_time in enumerate(driver_next_free_time.get(constants.DRIVER_8_HOUR, [])):
                        if free_time <= now and now < timedelta(hours=17):
                            # Проверяем, взял ли водитель уже обед
                            if not driver_lunch_taken[i]:
                                # Проверяем, что текущее время >= 12:00
                                absolute_hour = constants.WORKING_DAY_BEGINS + (now.seconds // 3600)
                                if absolute_hour >= 12:
                                    driver_type = constants.DRIVER_8_HOUR
                                    driver_id = f"{constants.DRIVER_8_HOUR}{i + 1}"
                                    break
                            else:
                                driver_type = constants.DRIVER_8_HOUR
                                driver_id = f"{constants.DRIVER_8_HOUR}{i + 1}"
                                break


                    # Если нет доступного водителя типа 1, ищем водителя типа 2
                    if driver_type is None:
                        for i, free_time in enumerate(driver_next_free_time[constants.DRIVER_12_HOUR]):
                            driver_b_id = f"{constants.DRIVER_12_HOUR}{i + 1}"
                            if free_time <= now and day in driver_b_work_days[driver_b_id]:
                                driver_type = constants.DRIVER_12_HOUR
                                driver_id = driver_b_id
                                break

                    # Если нет доступных водителей, пропускаем этот автобус
                    if driver_type is None:
                        continue

                    # Генерируем время маршрута
                    route_time = constants.TRAVEL_TIME + random.randint(-constants.POSSIBLE_DELAY, constants.POSSIBLE_DELAY)
                    start_time = now
                    end_time = now + timedelta(minutes=route_time)


                    schedule.append({
                        "bus": bus + 1,
                        "driver_id": driver_id,
                        "driver_type": driver_type,
                        "start_time": start_time,
                        "end_time": end_time
                    })

                    bus_next_free_time[bus] = end_time + timedelta(minutes=15)

                    if driver_type == constants.DRIVER_8_HOUR:
                        if not driver_lunch_taken[int(driver_id[1:]) - 1]:
                            driver_lunch_taken[int(driver_id[1:]) - 1] = True
                            driver_next_free_time[constants.DRIVER_8_HOUR][int(driver_id[1:]) - 1] = end_time + timedelta(
                                minutes=60)  # Обед
                        else:

                            driver_next_free_time[constants.DRIVER_8_HOUR][int(driver_id[1:]) - 1] = end_time + timedelta(
                                minutes=15)
                    else:
                        driver_next_free_time[constants.DRIVER_12_HOUR][int(driver_id[1:]) - 1] = end_time + timedelta(
                            minutes=15)

                    active_buses += 1

            # Обновляем текущее время с шагом в 5 минут
            now += timedelta(minutes=5)
        weekly_schedule.append(schedule)

    return weekly_schedule


# Получаем начальные данные от пользователя
data = tui.get_param()

# Высчитываем и выводим расписания на неделю
tui.final_result(generate_schedule(data[0], data[1], data[2]))