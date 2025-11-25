import threading
import time

def workload(id, scale_type, power=1):
    print(f"{scale_type} scaling : Thread {id} initialized")
    result = 0
    for _ in range(1000000 * power):
        result += 1
    print(f"Thread {id} completed")

def horizontal(num_of_threads=4):
    threads = []
    for i in range(num_of_threads):
        t = threading.Thread(target=workload, args=(i, "Horizontal"))
        threads.append(t)
        t.start()
        
    for t in threads:
        t.join()
    print("Horizontal Scaling Completed")

def vertical(power=4):
    t = threading.Thread(target=workload, args=(1, "Vertical", power))
    t.start()
    t.join()
    print("Vertical Scaling Completed")

if __name__ == "__main__":
    start_ht = time.time()
    horizontal(num_of_threads=4)
    ht = time.time() - start_ht

    start_vt = time.time()
    vertical(power=4)
    vt = time.time() - start_vt

    print(f"Horizontal Scaling completed in {ht:.2f} seconds")
    print(f"Vertical Scaling completed in {vt:.2f} seconds")
