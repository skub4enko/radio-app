import requests
import logging
import time
import json

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
            response = requests.get(station["url"], stream=True, timeout=5)  # Тайм-аут 5 секунд

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

# Удаляем недоступные станции из списка
stations_list = [station for station in stations_list if station["name"] not in unavailable_stations]

# Перенумерация станций с правильными номерами
for i, station in enumerate(stations_list):
    station["name"] = f"St.{str(i + 1).zfill(2)} {station['name'].split(' ', 1)[1]}"

# Запись обновленного списка станций в файл
try:
    with open("stations_old.json", "w", encoding="utf-8") as file:
        json.dump(stations_list, file, ensure_ascii=False, indent=4)
    logging.info("Обновленный список станций сохранен в файл: stations_old.json")
except Exception as e:
    logging.error(f"Ошибка при записи в файл stations_old.json: {e}")

# Запись недоступных станций в текстовый файл
if unavailable_stations:
    try:
        with open("unavailable_stations.txt", "w", encoding="utf-8") as file:
            file.write("\n".join(unavailable_stations))
        logging.info(f"Неактивные станции записаны в файл: unavailable_stations.txt")
    except Exception as e:
        logging.error(f"Ошибка при записи в файл unavailable_stations.txt: {e}")
else:
    logging.info("Все станции доступны.")
