import argparse
import requests
import csv
import os
import time
import sys
from datetime import datetime
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from core.config_loader import get_env_profile

class HealthCheckAgent:
    def __init__(self):
        self.health_logs = {
            'dev': 'logs/health_dev.csv',
            'staging': 'logs/health_staging.csv', 
            'cloud': 'logs/health_cloud.csv'
        }
        self._init_logs()
    
    def _init_logs(self):
        os.makedirs("logs", exist_ok=True)
        
        for env, log_file in self.health_logs.items():
            if not os.path.exists(log_file):
                with open(log_file, 'w', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow(['timestamp', 'env', 'status', 'http_code', 'response_time_ms'])
    
    def check_health(self, env_name, once=False):
        """Perform health check for specified environment"""
        try:
            profile = get_env_profile(env_name)
            
            if once:
                return self._single_check(env_name, profile)
            else:
                return self._continuous_check(env_name, profile)
                
        except Exception as e:
            print(f"Error checking {env_name}: {e}")
            return False
    
    def _single_check(self, env_name, profile):
        """Perform single health check"""
        result = self._perform_check(env_name, profile)
        self._log_health(env_name, result)
        
        status_msg = "UP" if result['status'] == 'UP' else "DOWN"
        print(f"Health check {env_name}: {status_msg} (HTTP {result['http_code']}, {result['response_time_ms']}ms)")
        
        return result['status'] == 'UP'
    
    def _continuous_check(self, env_name, profile):
        """Perform continuous health checks every 30s"""
        print(f"Starting continuous health checks for {env_name} (every 30s)")
        
        try:
            while True:
                result = self._perform_check(env_name, profile)
                self._log_health(env_name, result)
                
                status_msg = "UP" if result['status'] == 'UP' else "DOWN"
                print(f"{datetime.now().strftime('%H:%M:%S')} - {env_name}: {status_msg}")
                
                time.sleep(30)
        except KeyboardInterrupt:
            print(f"\nStopped health checks for {env_name}")
            return True
    
    def _perform_check(self, env_name, profile):
        """Perform actual health check based on environment type"""
        if profile['type'] == 'local':
            return self._check_local(env_name, profile)
        elif profile['type'] == 'docker':
            return self._check_docker(env_name, profile)
        elif profile['type'] == 'render':
            return self._check_cloud(env_name, profile)
        else:
            return {
                'status': 'DOWN',
                'http_code': 0,
                'response_time_ms': 0
            }
    
    def _check_local(self, env_name, profile):
        """Check local environment health"""
        url = f"http://{profile['host']}:{profile['port']}"
        return self._http_check(url)
    
    def _check_docker(self, env_name, profile):
        """Check Docker environment health"""
        url = f"http://localhost:{profile['port']}"
        return self._http_check(url)
    
    def _check_cloud(self, env_name, profile):
        """Simulate cloud environment health check"""
        # Simulate cloud API check
        import random
        
        # Simulate response time and status
        response_time = random.randint(100, 500)
        is_up = random.choice([True, True, True, False])  # 75% uptime
        
        return {
            'status': 'UP' if is_up else 'DOWN',
            'http_code': 200 if is_up else 503,
            'response_time_ms': response_time
        }
    
    def _http_check(self, url):
        """Perform HTTP health check"""
        try:
            start_time = time.time()
            response = requests.get(url, timeout=10)
            response_time = int((time.time() - start_time) * 1000)
            
            return {
                'status': 'UP' if 200 <= response.status_code < 300 else 'DOWN',
                'http_code': response.status_code,
                'response_time_ms': response_time
            }
            
        except requests.exceptions.RequestException:
            return {
                'status': 'DOWN',
                'http_code': 0,
                'response_time_ms': 0
            }
    
    def _log_health(self, env_name, result):
        """Log health check result"""
        log_file = self.health_logs[env_name]
        
        with open(log_file, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([
                datetime.now().isoformat(),
                env_name,
                result['status'],
                result['http_code'],
                result['response_time_ms']
            ])

def main():
    parser = argparse.ArgumentParser(description='Health check agent for multi-environment monitoring')
    parser.add_argument('--env', required=True, choices=['dev', 'staging', 'cloud'],
                       help='Environment to check')
    parser.add_argument('--once', action='store_true',
                       help='Run single check instead of continuous monitoring')
    
    args = parser.parse_args()
    
    agent = HealthCheckAgent()
    success = agent.check_health(args.env, args.once)
    
    if args.once and not success:
        sys.exit(1)

if __name__ == "__main__":
    main()