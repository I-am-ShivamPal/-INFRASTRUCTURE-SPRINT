import os
import csv
from datetime import datetime

class DeployAgent:
    def __init__(self):
        self.log_file = "logs/deployment_log.csv"
        self._init_log()
    
    def _init_log(self):
        os.makedirs("logs", exist_ok=True)
        if not os.path.exists(self.log_file):
            with open(self.log_file, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['timestamp', 'env', 'action', 'status', 'details'])
    
    def deploy_flask(self, app_name='app.py', message='Hello World!', port=5000, debug=True):
        app_content = f'''from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello():
    return "{message}"

if __name__ == '__main__':
    app.run(debug={debug}, port={port})'''
        
        with open(app_name, 'w') as f:
            f.write(app_content)
        
        self._log_deployment('flask', 'success')
        return f"Flask app deployed as {app_name}"
    

    
    def _log_deployment(self, app_type, status):
        with open(self.log_file, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([datetime.now().isoformat(), 'local', 'deploy', status, f'Flask {app_type} deployment'])