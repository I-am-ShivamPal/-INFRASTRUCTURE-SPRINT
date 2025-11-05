# DevOps System Architecture

## System Overview

The Smart DevOps Automation System is a comprehensive 5-day implementation featuring:

- **Multi-Agent Architecture**: Deploy, Monitor, Health Check, and Smart Agents
- **Environment Management**: dev/staging/cloud configuration profiles
- **AI-Powered Decision Making**: Q-learning reinforcement learning
- **Real-Time Monitoring**: Health checks with CSV logging
- **Interactive Visualization**: Streamlit dashboard with status indicators

## Component Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Config Loader │    │ Multi-Env Deploy│    │ Health Check    │
│                 │    │     Agent       │    │     Agent       │
│ env_profiles.   │───▶│                 │───▶│                 │
│ json + env vars │    │ dev/staging/    │    │ Per-env health  │
└─────────────────┘    │ cloud support   │    │ monitoring      │
                       └─────────────────┘    └─────────────────┘
                                │                       │
                                ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Smart Agent   │    │      Main       │    │   Dashboard     │
│                 │    │   Orchestrator  │    │                 │
│ Q-Learning RL   │◀───│                 │───▶│ Environment     │
│ State/Action    │    │ Integration &   │    │ Health Status   │
│ Learning        │    │ Coordination    │    │ Visualization   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## Data Flow

1. **Configuration Loading**: `config_loader.py` reads `env_profiles.json` + environment variables
2. **Multi-Environment Deployment**: CLI-based deployment to dev/staging/cloud
3. **Health Monitoring**: Continuous health checks with per-environment CSV logging
4. **Issue Detection**: Smart agent analyzes system state from health logs
5. **Action Selection**: Q-learning algorithm chooses optimal remediation action
6. **Dashboard Visualization**: Real-time status display with color-coded indicators

## File Organization

### Core Components
- `main.py`: System orchestrator and integration coordinator
- `smart_agent.py`: Q-learning reinforcement learning engine
- `dashboard.py`: Streamlit-based visualization dashboard

### Agent Layer
- `multi_env_deploy_agent.py`: Multi-environment deployment management
- `health_check_agent.py`: Environment-specific health monitoring
- `deploy_agent.py`: Original Flask deployment agent
- `monitor_agent.py`: Original monitoring agent
- `auto_fix_agent.py`: Automated issue resolution

### Configuration & Data
- `config/env_profiles.json`: Environment configuration profiles
- `core/config_loader.py`: Configuration management with env var overrides
- `logs/*.csv`: Structured logging for all system components
- `reports/integration_report.md`: Comprehensive integration test results

## Integration Points

### Smart Agent Integration
- **Input**: System state from health check logs
- **Processing**: Q-learning action selection with epsilon-greedy exploration
- **Output**: Optimal remediation action (restart_deployment, rollback, monitor)
- **Learning**: Q-value updates based on action success/failure

### Dashboard Integration
- **Data Sources**: All CSV log files in `logs/` directory
- **Visualization**: Environment health status, response time trends, deployment history
- **Real-Time Updates**: Automatic refresh of metrics and status indicators

### Multi-Environment Support
- **Configuration**: JSON-based profiles with environment variable overrides
- **Deployment**: CLI interface supporting `--env dev|staging|cloud`
- **Monitoring**: Per-environment health checks with separate CSV logging
- **Scalability**: Easy addition of new environments via configuration

## Extensibility

The system is designed for easy extension:

1. **New Environments**: Add to `env_profiles.json`
2. **Custom Health Checks**: Extend `HealthCheckAgent` class
3. **Additional Actions**: Update `states_actions.json` and `smart_agent.py`
4. **Dashboard Metrics**: Add new visualizations to `dashboard.py`
5. **Integration APIs**: Extend agents with external system connectors

## Performance Characteristics

- **Deployment Time**: < 30 seconds per environment
- **Health Check Frequency**: Configurable (default: 30 seconds)
- **Dashboard Refresh**: Real-time updates every 5 seconds
- **Learning Convergence**: Q-values stabilize after ~50 iterations
- **Log File Size**: ~1KB per day per environment (typical usage)