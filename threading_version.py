import threading
import timeit
from collections import defaultdict
from file_search_common import search_in_file


def thread_task(files, keywords, results, lock):
    """
    Завдання для окремого потоку: обробити свої файли
    і покласти локальний результат у чергу.
    """
    for file_path in files:
        found_keywords = search_in_file(file_path, keywords)
        if not found_keywords:
            continue

        with lock:
            for kw in found_keywords:
                results[kw].append(file_path)


def main_threading(file_paths, keywords, num_threads=4):
    """
    Основна функція для багатопотокового пошуку.
    Повертає словник: {keyword: [file_paths...]}.
    Також виводить час виконання.
    """
    start_time = timeit.default_timer()

    threads = []
    results = defaultdict(list)
    lock = threading.Lock()

    files_for_thread = [[] for _ in range(num_threads)]

    for index, file_path in enumerate(file_paths):
        thread_index = index % num_threads
        files_for_thread[thread_index].append(file_path)

    for i in range(num_threads):
        if not files_for_thread[i]:
            continue

        thread = threading.Thread(
            target=thread_task,
            args=(files_for_thread[i], keywords, results, lock),
        )
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    elapsed = timeit.default_timer() - start_time
    print(f"[THREADING] Execution time: {elapsed:.4f} sec")

    return dict(results)
