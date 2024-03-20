import multiprocessing
import threading
import time
from queue import Queue


# Функція для пошуку ключових слів у файлі
def search_in_file(file_path, keywords, results):
    try:
        with open(file_path, 'r') as file:
            text = file.read()
            for keyword in keywords:
                if keyword in text:
                    if keyword in results:
                        results[keyword].append(file_path)
                    else:
                        results[keyword] = [file_path]
    except Exception as e:
        print(f"Error processing file {file_path}: {e}")


# Функція робітника для threading
def worker_thread(files_queue, keywords, results):
    while not files_queue.empty():
        file_path = files_queue.get()
        search_in_file(file_path, keywords, results)
        files_queue.task_done()


# Функція робітника для multiprocessing
def worker_process(file_path, keywords, results_queue):
    results = {}
    search_in_file(file_path, keywords, results)
    results_queue.put(results)


# Багатопотокова обробка
def main_threading(files, keywords):
    start_time = time.time()
    files_queue = Queue()
    results = {}

    for file in files:
        files_queue.put(file)

    threads = []
    for _ in range(min(4, len(files))):
        thread = threading.Thread(target=worker_thread, args=(files_queue, keywords, results))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    print(f"Threading results: {results}")
    print(f"Threading time taken: {time.time() - start_time}")


# Багатопроцесорна обробка
def main_multiprocessing(files, keywords):
    start_time = time.time()
    results_queue = multiprocessing.Queue()
    processes = []

    for file in files:
        process = multiprocessing.Process(target=worker_process, args=(file, keywords, results_queue))
        process.start()
        processes.append(process)

    for process in processes:
        process.join()

    results = {}
    while not results_queue.empty():
        result = results_queue.get()
        for keyword, paths in result.items():
            if keyword in results:
                results[keyword].extend(paths)
            else:
                results[keyword] = paths

    print(f"Multiprocessing results: {results}")
    print(f"Multiprocessing time taken: {time.time() - start_time}")


if __name__ == "__main__":
    files = [f"./file{i}.txt" for i in range(1, 4)]
    keywords = ["example", "keyword", "test"]

    print("Running with threading:")
    main_threading(files, keywords)

    print("\nRunning with multiprocessing:")
    main_multiprocessing(files, keywords)
