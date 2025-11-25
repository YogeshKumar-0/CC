import psutil, time, datetime

def get_cpu_usage():
    return psutil.cpu_percent(interval=1)

def get_memory_usage():
    m = psutil.virtual_memory()
    return m.percent, m.used / (1024**3), m.total / (1024**3)

def get_disk_usage(drive="C:\\"):
    d = psutil.disk_usage(drive)
    return d.percent, d.used / (1024**3), d.total / (1024**3)

def monitor_resources(interval=5, drive="C:\\"):
    try:
        while True:
            print("=" * 50)
            print(f"Cloud Resource Monitoring - {datetime.datetime.now()}")
            print("=" * 50)

            cpu = get_cpu_usage()
            print(f"CPU Usage    : {cpu:.2f}%")

            mem_percent, mem_used, mem_total = get_memory_usage()
            print(f"Memory Usage : {mem_percent:.2f}% | Used: {mem_used:.2f} GB / Total: {mem_total:.2f} GB")

            disk_percent, disk_used, disk_total = get_disk_usage(drive)
            print(f"Disk Usage   : {disk_percent:.2f}% | Used: {disk_used:.2f} GB / Total: {disk_total:.2f} GB")

            print("=" * 50)
            time.sleep(interval)
    except KeyboardInterrupt:
        print("\nMonitoring stopped by user.")

# Run it
monitor_resources(interval=5, drive="C:\\")
