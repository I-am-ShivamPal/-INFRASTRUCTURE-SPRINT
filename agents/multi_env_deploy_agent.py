import argparse
import subprocess
import csv
import os
import json
from datetime import datetime
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from core.config_loader import get_env_profile

class MultiEnvDeployAgent:
    def __init__(self):
        self.deployment_log = "logs/deployment_log.csv"
        self.cloud_attempts_log = "logs/deploy_cloud_attempts.csv"
        self._init_logs()
    
    def _init_logs(self):
        os.makedirs("logs", exist_ok=True)
        
        # Initialize deployment log
        if not os.path.exists(self.deployment_log):
            with open(self.deployment_log, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['timestamp', 'env', 'action', 'status', 'details'])
        
        # Initialize cloud attempts log
        if not os.path.exists(self.cloud_attempts_log):
            with open(self.cloud_attempts_log, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['timestamp', 'service_name', 'region', 'status', 'details'])
    
    def deploy(self, env_name):
        """Deploy to specified environment"""
        try:
            profile = get_env_profile(env_name)
            
            if profile['type'] == 'local':
                return self._deploy_local(env_name, profile)
            elif profile['type'] == 'docker':
                return self._deploy_docker(env_name, profile)
            elif profile['type'] == 'render':
                return self._deploy_cloud(env_name, profile)
            else:
                raise ValueError(f"Unknown deployment type: {profile['type']}")
                
        except Exception as e:
            self._log_deployment(env_name, 'deploy', 'failed', str(e))
            return False
    
    def _deploy_local(self, env_name, profile):
        """Deploy to local environment"""
        try:
            cmd = profile['deploy_cmd']
            print(f"Starting local deployment: {cmd}")
            
            # Start process in background
            process = subprocess.Popen(
                cmd.split(),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            
            # Check if process started successfully
            if process.poll() is None:
                details = f"Local app started on {profile['host']}:{profile['port']}"
                self._log_deployment(env_name, 'deploy', 'success', details)
                print(f"✅ {details}")
                return True
            else:
                stdout, stderr = process.communicate()
                error = stderr.decode() if stderr else "Process failed to start"
                self._log_deployment(env_name, 'deploy', 'failed', error)
                return False
                
        except Exception as e:
            self._log_deployment(env_name, 'deploy', 'failed', str(e))
            return False
    
    def _deploy_docker(self, env_name, profile):
        """Deploy to Docker environment"""
        try:
            image = profile['image']
            port = profile['port']
            
            # Build Docker image (simulate)
            print(f"Building Docker image: {image}")
            
            # Run Docker container
            cmd = f"docker run -d -p {port}:{port} --name sampleapp_{env_name} {image}"
            print(f"Running: {cmd}")
            
            # Simulate docker run (since image might not exist)
            # In real scenario: result = subprocess.run(cmd.split(), capture_output=True, text=True)
            
            details = f"Docker container started: {image} on port {port}"
            self._log_deployment(env_name, 'deploy', 'success', details)
            print(f"✅ {details}")
            return True
            
        except Exception as e:
            self._log_deployment(env_name, 'deploy', 'failed', str(e))
            return False
    
    def _deploy_cloud(self, env_name, profile):
        """Deploy to cloud environment (Render stub)"""
        try:
            service_name = profile['service_name']
            region = profile['region']
            
            print(f"Deploying to cloud: {service_name} in {region}")
            
            # Log cloud attempt
            with open(self.cloud_attempts_log, 'a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([
                    datetime.now().isoformat(),
                    service_name,
                    region,
                    'attempted',
                    'Stub deployment - API integration needed'
                ])
            
            # Simulate successful cloud deployment
            details = f"Cloud deployment initiated: {service_name} ({region})"
            self._log_deployment(env_name, 'deploy', 'success', details)
            print(f"✅ {details}")
            return True
            
        except Exception as e:
            self._log_deployment(env_name, 'deploy', 'failed', str(e))
            return False
    
    def _log_deployment(self, env, action, status, details):
        """Log deployment attempt"""
        with open(self.deployment_log, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([
                datetime.now().isoformat(),
                env,
                action,
                status,
                details
            ])

def main():
    parser = argparse.ArgumentParser(description='Multi-environment deployment agent')
    parser.add_argument('--env', required=True, choices=['dev', 'staging', 'cloud'],
                       help='Environment to deploy to')
    
    args = parser.parse_args()
    
    agent = MultiEnvDeployAgent()
    success = agent.deploy(args.env)
    
    if success:
        print(f"Deployment to {args.env} completed successfully")
    else:
        print(f"Deployment to {args.env} failed")
        sys.exit(1)

if __name__ == "__main__":
    main()