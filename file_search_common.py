from pathlib import Path

def search_in_file(file_path, keywords):
    """
    Повертає список ключових слів, які зустрічаються у файлі.
    Якщо файл прочитати не вдалося — повертає порожній список.
    """
    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as file:
            content = file.read().lower()
    except OSError as e:
        print(f"[ERROR] Не вдалося прочитати файл {file_path}: {e}")
        return []

    found = []
    for keyword in keywords:
        if keyword in content:
            found.append(keyword)

    return found


def collect_files(directory, pattern="*.txt"):
    """
    Повертає список шляхів до файлів у директорії за вказаним патерном.
    За замовчуванням шукає *.txt.
    """
    dir_path = Path(directory)
    if not dir_path.is_dir():
        raise ValueError(f"{directory} is not a directory")

    return list(dir_path.glob(pattern))
