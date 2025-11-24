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
    print(f"\n[{title}] Results:")
    for keyword, files in results.items():
        print(f"'{keyword}' found in {len(files)} files:")
        for f in files:
            print(f"  - {f}")


if __name__ == "__main__":
    try:
        file_paths = collect_files(DIRECTORY, PATTERN)
    except Exception as e:
        print(f"[ERROR] {e}")
        raise SystemExit(1)

    if not file_paths:
        print("No files to analyze")
        raise SystemExit(0)

    print(f"Number of files for analysis: {len(file_paths)}")
    print(f"Keywords: {KEYWORDS}")

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