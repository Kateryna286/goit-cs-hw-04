from file_search_common import collect_files
from threading_version import main_threading
from multiprocessing_version import main_multiprocessing


DIRECTORY = "data" 
PATTERN = "*.txt"  
KEYWORDS = ["Windows", "GUID", "Script", "Name", "GUI", "windir"] 
KEYWORDS_LOWER = [keyword.lower() for keyword in KEYWORDS]


NUM_THREADS = 4
NUM_PROCESSES = 4


def print_results(title, results):
    print(f"\n[{title}] Результати:")
    for keyword, files in results.items():
        print(f"'{keyword}' знайдено в {len(files)} файлах:")
        for f in files:
            print(f"  - {f}")


if __name__ == "__main__":
    try:
        file_paths = collect_files(DIRECTORY, PATTERN)
    except Exception as e:
        print(f"[ERROR] {e}")
        raise SystemExit(1)

    if not file_paths:
        print("Немає файлів для аналізу.")
        raise SystemExit(0)

    print(f"Файлів для аналізу: {len(file_paths)}")
    print(f"Ключові слова: {KEYWORDS}")

    print()

    # --- threading ---
    threading_results = main_threading(file_paths, KEYWORDS_LOWER, NUM_THREADS)
    print_results("THREADING", threading_results)

    print()

    # --- multiprocessing ---
    multiprocessing_results = main_multiprocessing(
        file_paths, KEYWORDS_LOWER, NUM_PROCESSES
    )
    print_results("MULTIPROCESSING", multiprocessing_results)