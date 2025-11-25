class ServiceInstance:
    def __init__(self, name):
        self.name = name

    def handle_request(self, request_id):
        print(f"{self.name} is handling request {request_id}")

class RoundRobinLoadBalancer:
    def __init__(self, instances):
        self.instances = instances
        self.index = 0  # Keeps track of which instance to use next

    def get_instance(self):
        instance = self.instances[self.index]
        # Move index to next instance (wrap around using modulo)
        self.index = (self.index + 1) % len(self.instances)
        return instance

    def handle_request(self, request_id):
        instance = self.get_instance()
        instance.handle_request(request_id)

# ------------------ Simulation ------------------
if __name__ == "__main__":
    # Create 3 service instances
    instances = [ServiceInstance("Service-1"),
                 ServiceInstance("Service-2"),
                 ServiceInstance("Service-3")]

    # Create Round-Robin Load Balancer
    lb = RoundRobinLoadBalancer(instances)

    # Simulate 10 incoming requests
    for req in range(1, 11):
        lb.handle_request(req)
