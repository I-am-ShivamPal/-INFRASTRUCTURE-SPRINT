# Smart DevOps Automation System

A complete 5-day DevOps automation system with multi-environment deployment, intelligent monitoring, AI-powered auto-healing, and comprehensive integration testing.

## 🚀 Features

- **Multi-Environment Deployment**: Support for dev (local), staging (Docker), and cloud (Render) environments
- **Environment-Specific Health Monitoring**: Real-time health checks with per-environment logging
- **Smart Auto-Healing**: Q-learning reinforcement learning agent for intelligent issue resolution
- **Enhanced Interactive Dashboard**: Environment health visualization with status indicators
- **Comprehensive Integration Testing**: End-to-end testing with failure simulation and reporting
- **Configuration Management**: JSON-based environment profiles with CLI support

## 📁 Project Structure

```
2. 5-DAY DEVOPS + INFRASTRUCTURE/
├── agents/
│   ├── deploy_agent.py           # Original Flask deployment agent
│   ├── monitor_agent.py          # Original monitoring agent
│   ├── auto_fix_agent.py         # Automated issue resolution
│   ├── multi_env_deploy_agent.py # Multi-environment deployment
│   └── health_check_agent.py     # Environment health monitoring
├── config/
│   └── env_profiles.json         # Environment configurations
├── core/
│   └── config_loader.py          # Configuration management
├── logs/
│   ├── deployment_log.csv        # Deployment history
│   ├── monitor_log.csv           # Original monitoring data
│   ├── issue_log.csv             # System issues and alerts
│   ├── healing_log.csv           # Auto-healing actions
│   ├── health_dev.csv            # Dev environment health logs
│   ├── health_staging.csv        # Staging environment health logs
│   ├── health_cloud.csv          # Cloud environment health logs
│   └── final_integration_run.csv # Integration test results
├── reports/
│   └── integration_report.md     # Integration test report
├── main.py                       # Main system orchestrator
├── smart_agent.py                # Q-learning reinforcement agent
├── dashboard.py                  # Enhanced Streamlit dashboard
├── app.py                        # Generated Flask application
├── states_actions.json           # AI agent state-action mappings
├── rl_table.csv                  # Q-learning values (auto-generated)
└── requirements.txt              # Python dependencies
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

### Multi-Environment Deployment
```bash
# Deploy to development (local)
python agents/multi_env_deploy_agent.py --env dev

# Deploy to staging (Docker simulation)
python agents/multi_env_deploy_agent.py --env staging

# Deploy to cloud (Render API)
python agents/multi_env_deploy_agent.py --env cloud
```

### Health Monitoring
```bash
# Continuous monitoring (all environments)
python agents/health_check_agent.py

# Single health check
python agents/health_check_agent.py --once
```

### Enhanced Dashboard
```bash
streamlit run dashboard.py
```
Access at: `http://localhost:8501`
- Environment health status with color indicators
- Response time trends and deployment history
- Real-time log monitoring

### Integration Testing
```bash
# Run complete system integration test
python main.py
```

### Individual Components

**Multi-Environment Deployment**:
```python
from agents.multi_env_deploy_agent import MultiEnvDeployAgent
agent = MultiEnvDeployAgent()
agent.deploy_to_environment("dev")  # or "staging", "cloud"
```

**Health Check Monitoring**:
```python
from agents.health_check_agent import HealthCheckAgent
health = HealthCheckAgent()
health.check_all_environments()
```

**Smart Agent with Q-Learning**:
```python
from smart_agent import SmartAgent
agent = SmartAgent()
action = agent.choose_action("connection_failed")
reward = agent.update_q_value("connection_failed", action, 1.0)
```

## 📊 System Workflow

```
Environment Config → Multi-Env Deploy → Health Monitoring → Issue Detection → Smart Agent → Auto-Healing → Learning → Dashboard Visualization
```

### 5-Day Implementation Flow
1. **Day 1 - Environment Profiles**: JSON configuration system with dev/staging/cloud profiles
2. **Day 2 - Multi-Environment Deploy**: CLI-based deployment agent supporting multiple environments
3. **Day 3 - Health Check Agent**: Per-environment health monitoring with CSV logging
4. **Day 4 - Enhanced Dashboard**: Environment health visualization with status indicators
5. **Day 5 - Integration Testing**: End-to-end testing with comprehensive reporting

### Smart Agent Integration
- **State Detection**: Monitors connection_failed, slow_response, healthy states
- **Action Selection**: Uses epsilon-greedy Q-learning for optimal decisions
- **Learning**: Updates Q-values based on action outcomes for continuous improvement

## 📈 Monitoring & Logging

### Log Files
- **deployment_log.csv**: `timestamp, app_type, status`
- **monitor_log.csv**: `timestamp, response_time, status, error`
- **issue_log.csv**: `timestamp, alert_type, message`
- **healing_log.csv**: `timestamp, issue_type, action, status`
- **health_dev.csv**: `timestamp, environment, status, response_time, http_code, error`
- **health_staging.csv**: Environment-specific health monitoring for staging
- **health_cloud.csv**: Environment-specific health monitoring for cloud
- **final_integration_run.csv**: Combined integration test results

### Enhanced Dashboard Metrics
- **Environment Health Panel**: Real-time status indicators (🟢🔴🟡) for all environments
- **Deployment History**: Environment-specific deployment tracking
- **Response Time Trends**: Interactive charts with environment filtering
- **Health Status Cards**: Current status with last check timestamps
- **Integration Test Results**: Success rates and failure analysis
- **Real-time Log Monitoring**: Latest entries from all log files

## ⚙️ Configuration

### Environment Profiles (`config/env_profiles.json`)
```json
{
  "dev": {
    "host": "127.0.0.1",
    "port": 5000,
    "deploy_command": "python app.py"
  },
  "staging": {
    "host": "127.0.0.1",
    "port": 5001,
    "deploy_command": "docker run -p 5001:5000 flask-app"
  },
  "cloud": {
    "host": "your-app.onrender.com",
    "port": 443,
    "deploy_command": "render deploy"
  }
}
```

### Environment Variable Overrides
```bash
# Override any configuration
export DEV_HOST=localhost
export STAGING_PORT=8080
export CLOUD_HOST=production.example.com
```

### Smart Agent Parameters
```python
SmartAgent(
    alpha=0.6,      # Learning rate
    gamma=0.0,      # Discount factor
    epsilon=0.2     # Exploration rate
)
```

## 🔧 Customization

### Adding New Environments
1. **Edit** `config/env_profiles.json`:
   ```json
   {
     "production": {
       "host": "prod.example.com",
       "port": 443,
       "deploy_command": "kubectl apply -f deployment.yaml"
     }
   }
   ```

2. **Add health monitoring**: System automatically creates `health_production.csv`

### Custom Health Checks
```python
class CustomHealthCheck(HealthCheckAgent):
    def custom_check(self, environment):
        # Add custom health validation logic
        return {"status": "UP", "custom_metric": value}
```

### Integration with External Systems
```python
# Add to smart_agent.py execute_action()
def execute_action(self, action):
    if action == "scale_up":
        # Integrate with Kubernetes/Docker Swarm
        subprocess.run(["kubectl", "scale", "deployment", "app", "--replicas=3"])
```

## 🐛 Troubleshooting

### Common Issues

**Environment Configuration**:
```bash
# Verify config file exists
cat config/env_profiles.json

# Test configuration loading
python -c "from core.config_loader import get_env_profile; print(get_env_profile('dev'))"
```

**Multi-Environment Deployment**:
```bash
# Test individual environment
python agents/multi_env_deploy_agent.py --env dev

# Check deployment logs
tail -f logs/deployment_log.csv
```

**Health Check Issues**:
```bash
# Run single health check
python agents/health_check_agent.py --once

# Verify environment-specific logs
ls -la logs/health_*.csv
```

**Dashboard Not Loading**:
```bash
# Install all dependencies
pip install -r requirements.txt

# Test dashboard import
python -c "import dashboard; print('Dashboard imports successfully')"
```

**Integration Test Failures**:
- Check `reports/integration_report.md` for detailed analysis
- Verify all log files exist in `logs/` directory
- Ensure Q-learning table `rl_table.csv` has proper permissions

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

### Completed in 5-Day Implementation
- [x] Multi-environment deployment support
- [x] Environment-specific health monitoring
- [x] Enhanced dashboard with status visualization
- [x] Comprehensive integration testing
- [x] Q-learning reinforcement learning agent

### Planned Enhancements
- [ ] Docker containerization for all environments
- [ ] Kubernetes native deployment
- [ ] Advanced ML algorithms (Deep Q-Learning, Actor-Critic)
- [ ] Real-time alerting (Slack, Email, SMS)
- [ ] Performance metrics API with REST endpoints
- [ ] Configuration management UI
- [ ] Multi-application orchestration
- [ ] Cloud-native integrations (AWS ECS, Azure Container Instances)
- [ ] GitOps integration with automated CI/CD
- [ ] Prometheus/Grafana monitoring integration

## 📄 Dependencies

- **flask>=2.0.0**: Web application framework
- **requests>=2.25.0**: HTTP library for health monitoring
- **streamlit>=1.0.0**: Interactive dashboard framework
- **pandas>=1.3.0**: Data manipulation and CSV processing
- **plotly>=5.0.0**: Interactive charts and visualizations
- **python-dotenv>=0.19.0**: Environment variable management

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