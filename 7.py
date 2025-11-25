import time, random, threading

class CloudInstance:
    "Simulates a cloud instance (Primary/Backup)."

    def __init__(self, name):
        self.name = name
        self.is_active = True #Health Status

    def process_request(self, request_id):
        "Process request if instsnce is healthy."
        if not self.is_active:
            raise Exception(f"{self.name} instance is DOWN in cloud!")
        print(f"Cloud ☁ {self.name} handled request {request_id}")

class CloudFailoverSystem:
    "Manages cloud failover between primary and backup."
    def __init__(self, primary, backup):
        self.primary = primary
        self.backup = backup
        self.active_instance = primary
        self.lock = threading.Lock()

    def send_request(self, request_id):
        "Send request to active cloud instance."
        with self.lock:
            try:
                self.active_instance.process_request(request_id)
            except Exception as e:
                print(f"Cloud Failover Detected: {e}")
                self.failover()

                # Retry with the new active instance (likely backup)
                try:
                    self.active_instance.process_request(request_id)
                except Exception as e2:
                    print(f"Both cloud instances failed! Dropping request {request_id} ({e2})")

    def failover(self):
        "Switch trafffic between cloud instances."
        if self.active_instance == self.primary:
            print("Redirecting traffic to BACKUP cloud instance...")
            self.active_instance = self.backup
        else:
            print("Redirecting traffic back to PRIMARY cloud instance...")
            self.active_instance = self.primary

def client_requests(system, client_id, total=5):
    "Simulate client sending requests in the cloud."
    for i in range(1, total + 1):
        request_id = f"Client{client_id} - Req{i}"

        # Simulate random primary failure (~33% chance)
        if random.choice([True, False, False]):
            system.primary.is_active = False

        system.send_request(request_id)
        time.sleep(random.uniform(0.5, 1.5))

def cloud_health_monitor(system):
    "Background thread: restores primary after failure (simulates cloud self-healing)"
    while True:
        time.sleep(5)
        if not system.primary.is_active:
            print("Cloud Monitor: Restoring PRIMARY instance...")
            system.primary.is_active = True

if __name__ == "__main__":

    # Create cloud instances
    primary_instance = CloudInstance("PRIMARY")
    backup_instance = CloudInstance("BACKUP")

    # Create Failover System
    system = CloudFailoverSystem(primary_instance, backup_instance)

    # Start cloud health monitoring thread
    monitor_thread = threading.Thread(target = cloud_health_monitor, args = (system,), daemon = True)
    monitor_thread.start()

    # Start multiple client threads
    clients = []
    for cid in range(1,4): # 3 clients
        t = threading.Thread(target = client_requests, args = (system, cid, 6))
        clients.append(t)
        t.start()

    # Wait for all clients to finish
    for t in clients:
        t.join()

    print("\n Cloud Failover Simulation Complete.")