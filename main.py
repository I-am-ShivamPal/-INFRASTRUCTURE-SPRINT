import time
import threading
import os
import csv
from agents.deploy_agent import DeployAgent
from agents.monitor_agent import MonitorAgent
from agents.auto_fix_agent import AutoFixAgent
from smart_agent import SmartAgent

def deploy_cycle():
    deploy_agent = DeployAgent()
    deploy_agent.deploy_flask()
    print("Deployment completed")

def monitor_cycle(ping_interval=30, slow_threshold=5):
    monitor_agent = MonitorAgent(ping_interval=ping_interval, slow_threshold=slow_threshold)
    monitor_agent.start_monitoring()

def autofix_cycle(check_interval=60):
    autofix_agent = AutoFixAgent(check_interval=check_interval)
    smart_agent = SmartAgent()
    
    while True:
        if autofix_agent.check_issues():
            state = get_system_state()
            action = smart_agent.choose_action(state)
            
            if action:
                success = execute_action(action, autofix_agent)
                smart_agent.update(state, action, 1 if success else -1)
                print(f"Smart Agent: {action} -> {'Success' if success else 'Failed'}")
        
        time.sleep(check_interval)

def get_system_state():
    if not os.path.exists("logs/issue_log.csv"):
        return "healthy"
    
    try:
        with open("logs/issue_log.csv", 'r') as f:
            reader = csv.DictReader(f)
            issues = list(reader)
        return issues[-1]['alert_type'].lower() if issues else "healthy"
    except:
        return "healthy"

def execute_action(action, autofix_agent):
    try:
        # Dynamic action mapping
        action_map = {
            "restart_deployment": autofix_agent._restart_deployment,
            "rollback": autofix_agent._rollback_deployment,
            "monitor": lambda: True  # No-op for monitor action
        }
        
        if action in action_map:
            return action_map[action]()
        else:
            print(f"Unknown action: {action}")
            return False
    except Exception as e:
        print(f"Action execution failed: {e}")
        return False

def main(monitor_interval=None, slow_threshold=None, autofix_interval=None):
    # Dynamic configuration with defaults
    monitor_interval = monitor_interval or int(os.getenv('MONITOR_INTERVAL', 30))
    slow_threshold = slow_threshold or int(os.getenv('SLOW_THRESHOLD', 5))
    autofix_interval = autofix_interval or int(os.getenv('AUTOFIX_INTERVAL', 60))
    
    print(f"Starting DevOps automation system...")
    print(f"Config: Monitor={monitor_interval}s, Threshold={slow_threshold}s, AutoFix={autofix_interval}s")
    
    # Initial deployment
    deploy_cycle()
    
    # Start monitoring in background
    monitor_thread = threading.Thread(target=lambda: monitor_cycle(monitor_interval, slow_threshold), daemon=True)
    monitor_thread.start()
    
    # Start auto-fix in background
    autofix_thread = threading.Thread(target=lambda: autofix_cycle(autofix_interval), daemon=True)
    autofix_thread.start()
    
    print("System running: Deploy → Monitor → AutoFix")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nSystem stopped")

if __name__ == "__main__":
    main()