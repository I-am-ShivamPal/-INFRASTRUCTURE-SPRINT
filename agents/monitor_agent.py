import requests
import time
import csv
import os
from datetime import datetime

class MonitorAgent:
    def __init__(self, url="http://127.0.0.1:5000", timeout=10, slow_threshold=5, ping_interval=30):
        self.url = url
        self.timeout = timeout
        self.slow_threshold = slow_threshold
        self.ping_interval = ping_interval
        self.monitor_log = "logs/monitor_log.csv"
        self.issue_log = "logs/issue_log.csv"
        self._init_logs()
    
    def _init_logs(self):
        os.makedirs("logs", exist_ok=True)
        if not os.path.exists(self.monitor_log):
            with open(self.monitor_log, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['timestamp', 'response_time', 'status', 'error'])
        
        if not os.path.exists(self.issue_log):
            with open(self.issue_log, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['timestamp', 'alert_type', 'message'])
    
    def ping_app(self):
        try:
            start_time = time.time()
            response = requests.get(self.url, timeout=self.timeout)
            response_time = time.time() - start_time
            
            if response_time > self.slow_threshold:
                self._log_error(response_time, "slow_response", f"Response time: {response_time:.2f}s")
                self._send_alert("SLOW_RESPONSE", f"App responding slowly: {response_time:.2f}s")
                return False
            
            self._log_success(response_time)
            return True
            
        except Exception as e:
            self._log_error(0, "connection_failed", str(e))
            self._send_alert("CONNECTION_FAILED", f"App unreachable: {str(e)}")
            return False
    
    def _log_success(self, response_time):
        with open(self.monitor_log, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([datetime.now().isoformat(), f"{response_time:.2f}", "success", ""])
    
    def _log_error(self, response_time, status, error):
        with open(self.monitor_log, 'a', newline='') as f:
            writer = csv.writer(f)
            # Truncate long error messages
            short_error = error[:100] + "..." if len(error) > 100 else error
            writer.writerow([datetime.now().isoformat(), f"{response_time:.2f}", status, short_error])
    
    def _send_alert(self, alert_type, message):
        print(f"ALERT [{alert_type}]: {message}")
        with open(self.issue_log, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([datetime.now().isoformat(), alert_type, message])
    
    def start_monitoring(self):
        print(f"Starting monitoring of {self.url} (interval: {self.ping_interval}s, threshold: {self.slow_threshold}s)")
        while True:
            self.ping_app()
            time.sleep(self.ping_interval)