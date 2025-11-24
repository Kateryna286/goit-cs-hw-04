# multiprocessing_version.py
import multiprocessing
import timeit
from collections import defaultdict

from file_search_common import search_in_file


def process_task(files, keywords, out_queue):
    """
    Завдання для окремого процесу: обробити свої файли
    і покласти локальний результат у чергу.
    """
    local_results = defaultdict(list)

    for file_path in files:
        found_keywords = search_in_file(file_path, keywords)
        if not found_keywords:
            continue

        for kw in found_keywords:
            local_results[kw].append(file_path)

    out_queue.put(dict(local_results))


def main_multiprocessing(file_paths, keywords, num_processes=4):
    """
    Основна функція для багатопроцесорного пошуку.
    Повертає словник: {keyword: [file_paths...]}.
    Також виводить час виконання.
    """
    start_time = timeit.default_timer()

    processes = []
    out_queue = multiprocessing.Queue()
    results = defaultdict(list)

    files_for_process = [[] for _ in range(num_processes)]
    for index, file_path in enumerate(file_paths):
        proc_index = index % num_processes
        files_for_process[proc_index].append(file_path)

    for i in range(num_processes):
        if not files_for_process[i]:
            continue

        p = multiprocessing.Process(
            target=process_task,
            args=(files_for_process[i], keywords, out_queue),
        )
        processes.append(p)
        p.start()

    for _ in processes:
        partial = out_queue.get()
        for kw, paths in partial.items():
            results[kw].extend(paths)

    for p in processes:
        p.join()

    elapsed = timeit.default_timer() - start_time
    print(f"[MULTIPROCESSING] Час виконання: {elapsed:.4f} сек")

    return dict(results)
