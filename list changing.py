import json
import logging


# Чтение списка неработающих станций из текстового файла
def get_inactive_stations(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            inactive_stations = f.read().splitlines()
        logging.info(f"Неработающие станции: {inactive_stations}")
        return inactive_stations
    except Exception as e:
        logging.error(f"Ошибка при чтении файла неработающих станций: {e}")
        return []


# Функция для обновления плейлиста
def update_playlist(stations_file, inactive_stations_file, output_file):
    # Чтение списка станций из оригинального файла
    try:
        with open(stations_file, "r", encoding="utf-8") as file:
            stations_list = json.load(file)
        logging.info("Станции успешно загружены из файла.")
    except Exception as e:
        logging.error(f"Ошибка при открытии файла {stations_file}: {e}")
        return

    # Получаем список неработающих станций
    inactive_stations = get_inactive_stations(inactive_stations_file)

    # Фильтруем неработающие станции
    updated_stations = [station for station in stations_list if station["name"] not in inactive_stations]

    # Перенумеровка станций
    for idx, station in enumerate(updated_stations, start=1):
        station["name"] = f"St.{str(idx).zfill(2)} {station['name'][5:]}"  # Перенумерация

    # Запись обновленного списка станций в новый файл
    try:
        with open(output_file, "w", encoding="utf-8") as file:
            json.dump(updated_stations, file, ensure_ascii=False, indent=4)
        logging.info(f"Обновленный список станций сохранен в файл: {output_file}")
    except Exception as e:
        logging.error(f"Ошибка при записи в файл {output_file}: {e}")
        return


# Пример использования
update_playlist("stations_old.json", "unavailable_stations.txt", "stations.json")
