import threading
import queue
import time

print_lock = threading.Lock()

def process(task_id):
    with print_lock:
        print(f"Task - {task_id} processing...")
    time.sleep(1)
    with print_lock:
        print(f"Task - {task_id} completed")

def worker(task_queue,thread_id):
    while True:
        try:
            task_id = task_queue.get(timeout=2)
            with print_lock:
                print(f"Thread {thread_id} is executing Task {task_id}")
            process(task_id)
            task_queue.task_done()
        except queue.Empty:
            with print_lock:
                print("No more tasks remaining!")
            break

def elasticity():
    num_threads = 2
    threads = []
    print("Starting with 2 worker threads")

    task_queue = queue.Queue()
    for i in range(1,5):
        task_queue.put(i)
        
    for t_id in range(num_threads):
        t = threading.Thread(target=worker, args=(task_queue,t_id))
        t.start()
        threads.append(t)
    time.sleep(3)
    print("\nIncreased workload\nStarting with 5 worker threads\n")

    for i in range(5,15):
        task_queue.put(i)
        
    for t_id in range(2,5):
        t = threading.Thread(target=worker, args=(task_queue,t_id))
        t.start()
        threads.append(t)
        
    for t in threads:
        t.join()

elasticity()
