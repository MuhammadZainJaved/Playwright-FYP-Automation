# from locust import HttpUser, task, between
# import random
# import time

# class LoadTestUser(HttpUser):
#     # Base URL for your Django application
#     host = "http://localhost:8000"  # Update to the correct URL if running elsewhere

#     # Simulate user wait time between tasks
#     wait_time = between(1, 2)

#     # Blacklisted IPs for testing
#     blacklisted_ips = [
#         "192.99.34.64",
#         "23.234.51.72",
#         "185.220.101.6",
#         "209.141.61.41",
#         "46.161.9.8"
#     ]

#     def generate_mouse_movements(self, num_records=50):
#         """
#         Generate random mouse movement records.
#         """
#         return [
#             {
#                 "time": int(time.time() * 1000) + i * 100,  # Simulate timestamps
#                 "x": random.randint(0, 1920),
#                 "y": random.randint(0, 1080)
#             }
#             for i in range(num_records)
#         ]

#     @task
#     def test_queue_data(self):
#         """
#         Simulate a single request to the queue-data endpoint.
#         """
#         # Choose a random blacklisted IP
#         ip = random.choice(self.blacklisted_ips)

#         # Test payload
#         payload = {
#             "sessionID": f"session-{random.randint(1000, 9999)}",
#             "records": self.generate_mouse_movements(),
#             "browserInfo": {
#                 "browserName": "Headless Chrome",
#                 "osName": "Mac OS",
#                 "userAgent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
#                 "engineVersion": "91.0.4472.124",
#                 "timezone": -300,
#                 "language": "en-US",
#                 "viewportWidth": 1920,
#                 "viewportHeight": 1080
#             }
#         }

#         # Set the X-Forwarded-For header to use the current blacklisted IP
#         headers = {"X-Forwarded-For": ip}

#         # Send POST request
#         with self.client.post("/users/queue-data/", headers=headers, json=payload, catch_response=True) as response:
#             if response.status_code == 200:
#                 response.success()
#                 print(f"IP: {ip} - Request succeeded with status {response.status_code}")
#             else:
#                 response.failure(f"IP: {ip} - Request failed with status {response.status_code}")


from locust import HttpUser, task, between
import random
import time

class LoadTestUser(HttpUser):
    # Base URL for your Django application
    host = "http://localhost:8000"  # Update to the correct URL if running elsewhere

    # Simulate user wait time between tasks
    wait_time = between(1, 2)

    # Blacklisted IPs for testing
    blacklisted_ips = [
        "192.99.34.64",
        "23.234.51.72",
        "185.220.101.6",
        "209.141.61.41",
        "46.161.9.8"
    ]

    def generate_mouse_movements(self, num_records=50):
        """
        Generate random mouse movement records.
        """
        return [
            {
                "time": int(time.time() * 1000) + i * 100,  # Simulate timestamps
                "x": random.randint(0, 1920),
                "y": random.randint(0, 1080)
            }
            for i in range(num_records)
        ]

    def generate_human_like_browser_info(self):
        """
        Generate browser info for legitimate human-like behavior.
        """
        return {
            "browserName": "Chrome",  # Human-like browser
            "osName": "Windows",      # Common OS
            "userAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36",
            "engineVersion": "96.0.4664.45",
            "timezone": -240,  # Common timezone offset
            "language": "en-US",
            "viewportWidth": 1366,
            "viewportHeight": 768
        }

    def generate_bot_like_browser_info(self):
        """
        Generate browser info for bot-like behavior.
        """
        return {
            "browserName": "Headless Chrome",  # Bot-like browser
            "osName": "Mac OS",                # Mismatched OS
            "userAgent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "engineVersion": "91.0.4472.124",
            "timezone": -300,  # Anomalous timezone offset
            "language": "en-US",
            "viewportWidth": 1920,
            "viewportHeight": 1080
        }

    @task
    def test_queue_data(self):
        """
        Simulate a request to the queue-data endpoint, randomly choosing human-like or bot-like behavior.
        """
        # Determine if this is a human-like or bot-like request (70% human-like, 30% bot-like)
        is_human_like = random.random() < 0.7  # 70% chance for human-like

        # Choose browser info based on type
        if is_human_like:
            browser_info = self.generate_human_like_browser_info()
            ip = "192.168.1.100"  # Legitimate IP for human-like behavior
        else:
            browser_info = self.generate_bot_like_browser_info()
            ip = random.choice(self.blacklisted_ips)  # Blacklisted IP for bot-like behavior

        # Test payload
        payload = {
            "sessionID": f"session-{random.randint(1000, 9999)}",
            "records": self.generate_mouse_movements(),
            "browserInfo": browser_info
        }

        # Set the X-Forwarded-For header to use the appropriate IP
        headers = {"X-Forwarded-For": ip}

        # Send POST request
        with self.client.post("/users/queue-data/", headers=headers, json=payload, catch_response=True) as response:
            if response.status_code == 200:
                response.success()
                print(f"IP: {ip} - {'Human' if is_human_like else 'Bot'} request succeeded with status {response.status_code}")
            else:
                response.failure(f"IP: {ip} - {'Human' if is_human_like else 'Bot'} request failed with status {response.status_code}")
