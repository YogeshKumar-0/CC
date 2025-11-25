import requests
import time

# List of service endpoints to monitor
service_endpoints = [
    "https://www.google.com",
    "https://www.github.com",
    "https://www.wikipedia.org",
    "https://www.openai.com"
]

# Define response time threshold in seconds (SLA)
SLA_THRESHOLD = 0.8  # e.g., response time should be less than 0.8 seconds

print("----- SLA Monitoring Started -----\n")

# Monitor each endpoint
for service in service_endpoints:
    try:
        start_time = time.time()       # Record start time
        response = requests.get(service) # Send HTTP request
        end_time = time.time()         # Record end time

        response_time = end_time - start_time  # Calculate response time

        # Display results
        print(f"Service: {service}")
        print(f"Status Code: {response.status_code}")
        print(f"Response Time: {response_time:.3f} sec")

        # Check SLA compliance
        if response_time <= SLA_THRESHOLD:
            print("✅ SLA Met\n")
        else:
            print("⚠️ SLA Breached\n")

    except requests.exceptions.RequestException as e:
        print(f"❌ Error connecting to {service}: {e}\n")

print("----- SLA Monitoring Completed -----")
