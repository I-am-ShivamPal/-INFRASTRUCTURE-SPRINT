import csv
import os
import time
from datetime import datetime
from .deploy_agent import DeployAgent

class AutoFixAgent:
    def __init__(self, check_interval=60):
        self.check_interval = check_interval
        self.issue_log = "logs/issue_log.csv"
        self.healing_log = "logs/healing_log.csv"
        self.deploy_agent = DeployAgent()
        self._init_log()
    
    def _init_log(self):
        os.makedirs("logs", exist_ok=True)
        if not os.path.exists(self.healing_log):
            with open(self.healing_log, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['timestamp', 'issue_type', 'action', 'status'])
    
    def check_issues(self):
        if not os.path.exists(self.issue_log):
            return False
        
        with open(self.issue_log, 'r') as f:
            reader = csv.DictReader(f)
            issues = list(reader)
        
        if len(issues) > 0:
            latest_issue = issues[-1]
            return self._handle_issue(latest_issue)
        return False
    
    def _handle_issue(self, issue):
        alert_type = issue['alert_type']
        
        # Dynamic action mapping
        action_map = {
            'CONNECTION_FAILED': self._restart_deployment,
            'SLOW_RESPONSE': self._rollback_deployment
        }
        
        action = action_map.get(alert_type)
        if action:
            return action()
        return False
    
    def _restart_deployment(self):
        try:
            self.deploy_agent.deploy_flask()
            self._log_healing('CONNECTION_FAILED', 'restart', 'success')
            print("AUTO-FIX: Restarted deployment")
            return True
        except Exception as e:
            self._log_healing('CONNECTION_FAILED', 'restart', f'failed: {str(e)}')
            return False
    
    def _rollback_deployment(self):
        try:
            # Simple rollback - redeploy basic version
            self.deploy_agent.deploy_flask()
            self._log_healing('SLOW_RESPONSE', 'rollback', 'success')
            print("AUTO-FIX: Rolled back deployment")
            return True
        except Exception as e:
            self._log_healing('SLOW_RESPONSE', 'rollback', f'failed: {str(e)}')
            return False
    
    def _log_healing(self, issue_type, action, status):
        with open(self.healing_log, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([datetime.now().isoformat(), issue_type, action, status])