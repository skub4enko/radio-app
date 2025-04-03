import json
import requests
import logging
import time

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

# Загружаем список станций из JSON-файла
with open("stations_old.json", "r", encoding="utf-8") as file:
    stations_list = json.load(file)


# Функция для проверки доступности потока радиостанции
def check_station_availability(stations):
    unavailable_stations = []

    # Процесс проверки каждой станции
    for i, station in enumerate(stations):
        logging.info(f"Проверка {i + 1}/{len(stations)}: {station['name']}...")

        try:
            # Подключаемся к потоку
            response = requests.get(station["url"], stream=True, timeout=10)  # Тайм-аут 10 секунд

            # Проверка на успешное подключение (например, через чтение первых байт)
            start_time = time.time()
            for chunk in response.iter_content(chunk_size=1024):
                if time.time() - start_time > 5:  # Если прошло более 5 секунд — считаем недоступным
                    logging.warning(f"Станция '{station['name']}' не доступна (тайм-аут)")
                    unavailable_stations.append(station["name"])
                    break
                if chunk:  # Если получен хоть какой-то контент — значит поток работает
                    logging.info(f"Станция '{station['name']}' доступна.")
                    break
        except requests.Timeout:
            # Обработка ошибки тайм-аута при подключении
            logging.error(f"Тайм-аут при подключении к '{station['name']}'")
            unavailable_stations.append(station["name"])
        except requests.RequestException as e:
            # Обработка других ошибок
            logging.error(f"Ошибка при подключении к '{station['name']}': {str(e)}")
            unavailable_stations.append(station["name"])

    return unavailable_stations


# Проверка доступности станций
unavailable_stations = check_station_availability(stations_list)

# Запись неактивных станций в текстовый файл
if unavailable_stations:
    with open("unavailable_stations.txt", "w", encoding="utf-8") as file:
        file.write("\n".join(unavailable_stations))
    logging.info(f"Неактивные станции записаны в файл: unavailable_stations.txt")
else:
    logging.info("Все станции доступны.")
