# Smart DevOps Automation System

An intelligent DevOps automation system that combines deployment, monitoring, auto-healing, and machine learning for optimal system management.

## 🚀 Features

- **Automated Deployment**: Flask application deployment with configurable parameters
- **Intelligent Monitoring**: Real-time health monitoring with dynamic thresholds
- **Smart Auto-Healing**: AI-powered issue resolution using reinforcement learning
- **Interactive Dashboard**: Streamlit-based visualization of system metrics
- **Comprehensive Logging**: Detailed tracking of all system activities

## 📁 Project Structure

```
2. 5-DAY DEVOPS + INFRASTRUCTURE/
├── agents/
│   ├── deploy_agent.py      # Handles Flask app deployment
│   ├── monitor_agent.py     # Monitors application health
│   └── auto_fix_agent.py    # Automated issue resolution
├── logs/
│   ├── deployment_log.csv   # Deployment history
│   ├── monitor_log.csv      # Monitoring data
│   ├── issue_log.csv        # System issues and alerts
│   └── healing_log.csv      # Auto-healing actions
├── main.py                  # Main system orchestrator
├── smart_agent.py           # Reinforcement learning agent
├── dashboard.py             # Streamlit dashboard
├── app.py                   # Generated Flask application
├── states_actions.json      # AI agent state-action mappings
├── rl_table.csv             # Q-learning values (auto-generated)
└── requirements.txt         # Python dependencies
```

## 🧠 Smart Agent Architecture

The system uses **Q-Learning** reinforcement learning:

- **States**: `connection_failed`, `slow_response`, `healthy`
- **Actions**: `restart_deployment`, `rollback`, `monitor`
- **Learning**: Epsilon-greedy exploration with reward-based updates
- **Persistence**: Q-values stored in CSV for continuous improvement

## 🛠️ Installation

### Prerequisites
- Python 3.8+
- pip package manager

### Setup
1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Verify installation**:
   ```bash
   python -c "import flask, requests, streamlit, pandas, plotly; print('All packages installed')"
   ```

## 🚀 Usage

### Quick Start
```bash
python main.py
```

### Custom Configuration
```python
# Custom timing parameters
main(monitor_interval=15, slow_threshold=3, autofix_interval=30)
```

### Dashboard
```bash
streamlit run dashboard.py
```
Access at: `http://localhost:8501`

### Individual Components

**Deploy Flask App**:
```python
from agents.deploy_agent import DeployAgent
agent = DeployAgent()
agent.deploy_flask(message="Custom Hello!", port=8080)
```

**Monitor Application**:
```python
from agents.monitor_agent import MonitorAgent
monitor = MonitorAgent(slow_threshold=3, ping_interval=15)
monitor.start_monitoring()
```

**Smart Agent Testing**:
```python
from smart_agent import SmartAgent
agent = SmartAgent()
action = agent.choose_action("connection_failed")
print(f"Recommended: {action}")
```

## 📊 System Workflow

```
Deploy Flask App → Start Monitoring → Detect Issues → Smart Agent Analysis → Execute Action → Learn from Result → Repeat
```

### Detailed Flow
1. **Deployment**: Creates Flask "Hello World" app
2. **Monitoring**: Pings app every 30s, logs response times
3. **Issue Detection**: Identifies slow responses (>5s) or connection failures
4. **Smart Decision**: AI agent chooses optimal action based on learned experience
5. **Auto-Healing**: Executes restart or rollback actions
6. **Learning**: Updates Q-values based on action success/failure

## 📈 Monitoring & Logging

### Log Files
- **deployment_log.csv**: `timestamp, app_type, status`
- **monitor_log.csv**: `timestamp, response_time, status, error`
- **issue_log.csv**: `timestamp, alert_type, message`
- **healing_log.csv**: `timestamp, issue_type, action, status`

### Dashboard Metrics
- **Deployment Status**: Total deployments and last deployment time
- **Uptime Percentage**: Success rate calculation
- **Response Time Graphs**: Visual performance trends
- **Issue Distribution**: Pie charts of problem types
- **Real-time Tables**: Latest log entries

## ⚙️ Configuration

### Smart Agent Parameters
```python
SmartAgent(
    alpha=0.6,      # Learning rate (0-1)
    gamma=0.0,      # Discount factor (0-1)  
    epsilon=0.2     # Exploration rate (0-1)
)
```

### Monitor Settings
```python
MonitorAgent(
    url="http://127.0.0.1:5000",    # Target URL
    timeout=10,                      # Request timeout
    slow_threshold=5,                # Slow response threshold
    ping_interval=30                 # Monitoring frequency
)
```

### Deploy Options
```python
deploy_flask(
    app_name='app.py',              # Output filename
    message='Hello World!',         # Response message
    port=5000,                      # Flask port
    debug=True                      # Debug mode
)
```

## 🔧 Customization

### Adding New States/Actions
1. **Edit** `states_actions.json`:
   ```json
   {
     "actions": {
       "high_cpu": ["scale_up", "optimize", "restart"],
       "memory_leak": ["restart", "garbage_collect"]
     }
   }
   ```

2. **Implement** actions in `execute_action()` function

### Creating Custom Agents
```python
class CustomAgent:
    def __init__(self):
        self.log_file = "logs/custom_log.csv"
        self._init_log()
    
    def _init_log(self):
        os.makedirs("logs", exist_ok=True)
        # Initialize CSV with headers
```

## 🐛 Troubleshooting

### Common Issues

**Import Errors**:
```bash
pip install -r requirements.txt
```

**Port Already in Use**:
```python
# Change port in deploy_flask()
agent.deploy_flask(port=8080)
```

**Smart Agent Not Learning**:
- Verify `states_actions.json` exists
- Check `rl_table.csv` permissions
- Ensure issues are being logged to `logs/issue_log.csv`

**Dashboard Not Loading**:
```bash
# Install missing packages
pip install streamlit plotly
# Run dashboard
streamlit run dashboard.py
```

## 📝 Development

### Running Tests
```bash
# Test smart agent
python smart_agent.py

# Test individual agents
python -c "from agents.deploy_agent import DeployAgent; DeployAgent().deploy_flask()"
```

### Adding Features
1. Create new agent in `agents/` directory
2. Add logging initialization
3. Integrate with `main.py`
4. Update `requirements.txt` if needed
5. Add dashboard visualization

## 🔮 Future Enhancements

- [ ] Docker containerization
- [ ] Kubernetes integration
- [ ] Multi-application support
- [ ] Advanced ML algorithms (Deep Q-Learning)
- [ ] Cloud platform integration (AWS, Azure, GCP)
- [ ] Real-time alerting (Slack, Email)
- [ ] Performance metrics API
- [ ] Configuration management UI

## 📄 Dependencies

- **flask**: Web application framework
- **requests**: HTTP library for monitoring
- **streamlit**: Dashboard framework
- **pandas**: Data manipulation
- **plotly**: Interactive charts

## 🤝 Contributing

1. Fork the repository
2. Create feature branch
3. Add comprehensive tests
4. Update documentation
5. Submit pull request

## 📞 Support

For issues:
1. Check log files in `logs/` directory
2. Verify configuration files in root directory
3. Test individual components
4. Review troubleshooting section

---

**Built for intelligent DevOps automation with AI-powered decision making**