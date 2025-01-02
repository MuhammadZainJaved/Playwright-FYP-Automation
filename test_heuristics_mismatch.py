import requests
import random
import time
import json

# Target Django endpoint
url = "http://localhost:8000/users/queue-data/"  # Update if running on Kubernetes

# Blacklisted IPs for testing
blacklisted_ips = [
    "192.99.34.64",
    "23.234.51.72",
    "185.220.101.6",
    "209.141.61.41",
    "46.161.9.8"
]

# Generate random mouse movement records
def generate_mouse_movements(num_records=50):
    return [
        {
            "time": int(time.time() * 1000) + i * 100,  # Simulate timestamps
            "x": random.randint(0, 1920),
            "y": random.randint(0, 1080)
        }
        for i in range(num_records)
    ]

# Loop through blacklisted IPs and send test requests
for ip in blacklisted_ips:
    # Test payload
    payload = {
        "sessionID": f"session-{random.randint(1000, 9999)}",
        "records": generate_mouse_movements(),
        "browserInfo": {
            "browserName": "Headless Chrome",  # Trigger 'unapproved_browser'
            "osName": "Mac OS",               # Simulate mismatched OS
            "userAgent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "engineVersion": "91.0.4472.124",
            "timezone": -300,                 # Timezone offset in minutes
            "language": "en-US",
            "viewportWidth": 1920,
            "viewportHeight": 1080
        }
    }

    # Set the X-Forwarded-For header to use the current blacklisted IP
    headers = {"X-Forwarded-For": ip}

    print(f"Testing with IP: {ip}")
    # Send the request
    response = requests.post(url, headers=headers, json=payload)

    # Print the server's response
    print(f"Response Status Code: {response.status_code}")
    try:
        print(f"Response Body: {response.json()}")
    except json.JSONDecodeError:
        print("Response is not JSON:")
        print(response.text)

    # Small delay between requests
    time.sleep(1)
