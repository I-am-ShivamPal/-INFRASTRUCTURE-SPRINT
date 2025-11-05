# 5-Day DevOps System Setup Guide

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Verify Installation
```bash
python -c "import flask, requests, streamlit, pandas, plotly; print('✅ All packages installed successfully')"
```

### 3. Test Multi-Environment Deployment
```bash
# Deploy to development
python agents/multi_env_deploy_agent.py --env dev

# Check health
python agents/health_check_agent.py --once
```

### 4. Launch Dashboard
```bash
streamlit run dashboard.py
```
Access at: http://localhost:8501

### 5. Run Integration Test
```bash
python main.py
```

## Environment Configuration

The system uses `config/env_profiles.json` for environment settings:

- **dev**: Local development (port 5000)
- **staging**: Docker simulation (port 5001) 
- **cloud**: Render deployment (HTTPS)

Override any setting with environment variables:
```bash
export DEV_HOST=localhost
export STAGING_PORT=8080
```

## File Structure Overview

```
├── agents/           # Deployment and monitoring agents
├── config/           # Environment configurations
├── core/             # Configuration management
├── logs/             # All system logs (CSV format)
├── reports/          # Integration test reports
├── main.py           # System orchestrator
├── dashboard.py      # Streamlit dashboard
└── smart_agent.py    # Q-learning AI agent
```

## Key Features

✅ **Multi-Environment Support**: dev/staging/cloud deployment
✅ **Health Monitoring**: Per-environment health checks with CSV logging  
✅ **Smart Auto-Healing**: Q-learning reinforcement learning agent
✅ **Interactive Dashboard**: Real-time environment status visualization
✅ **Integration Testing**: Comprehensive end-to-end testing with reporting

## Troubleshooting

**Configuration Issues**: Check `config/env_profiles.json` exists
**Health Check Failures**: Verify target applications are running
**Dashboard Errors**: Ensure all dependencies installed with `pip install -r requirements.txt`
**Integration Test Issues**: Check `reports/integration_report.md` for detailed analysis

## Next Steps

1. Customize environment profiles in `config/env_profiles.json`
2. Add custom health checks in `agents/health_check_agent.py`
3. Extend smart agent actions in `smart_agent.py`
4. Monitor system performance via dashboard at http://localhost:8501