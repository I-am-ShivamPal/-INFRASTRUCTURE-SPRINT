import streamlit as st
import pandas as pd
import os
from datetime import datetime, timedelta
import plotly.express as px

st.set_page_config(page_title="DevOps Dashboard", layout="wide")

st.title("🚀 DevOps Automation Dashboard")

# Helper function to load CSV safely
def load_csv(file_path):
    if os.path.exists(file_path):
        try:
            return pd.read_csv(file_path)
        except:
            return pd.DataFrame()
    return pd.DataFrame()

# Load data
deployment_df = load_csv("logs/deployment_log.csv")
monitor_df = load_csv("logs/monitor_log.csv")
issue_df = load_csv("logs/issue_log.csv")
healing_df = load_csv("logs/healing_log.csv")

# Sidebar
st.sidebar.header("System Status")
if st.sidebar.button("🔄 Refresh Data"):
    st.rerun()

# Main dashboard
col1, col2, col3, col4 = st.columns(4)

# Deployment Status
with col1:
    st.metric("Total Deployments", len(deployment_df))
    if not deployment_df.empty and 'timestamp' in deployment_df.columns:
        last_deploy = deployment_df.iloc[-1]['timestamp']
        st.write(f"Last: {last_deploy[:19]}")

# Uptime Calculation
with col2:
    if not monitor_df.empty and 'status' in monitor_df.columns:
        total_pings = len(monitor_df)
        successful_pings = len(monitor_df[monitor_df['status'] == 'success'])
        uptime = (successful_pings / total_pings * 100) if total_pings > 0 else 0
        st.metric("Uptime %", f"{uptime:.1f}%")
    else:
        st.metric("Uptime %", "N/A")

# Errors & Fixes
with col3:
    st.metric("Total Issues", len(issue_df))
    
with col4:
    st.metric("Auto Fixes", len(healing_df))

st.divider()

# Environment Health Panel
st.header("🏥 Environment Health Status")

# Load health data
health_dev_df = load_csv("logs/health_dev.csv")
health_staging_df = load_csv("logs/health_staging.csv")
health_cloud_df = load_csv("logs/health_cloud.csv")

def get_env_status(health_df):
    if health_df.empty:
        return "🔘", "No Data", 0
    
    latest = health_df.iloc[-1]
    status = latest.get('status', 'UNKNOWN')
    response_time = latest.get('response_time_ms', 0)
    
    if status == 'UP':
        return "🟢", "UP", response_time
    elif status == 'DOWN':
        return "🔴", "DOWN", response_time
    else:
        return "🟡", "UNKNOWN", response_time

# Environment status cards
col1, col2, col3 = st.columns(3)

with col1:
    icon, status, rt = get_env_status(health_dev_df)
    st.metric(f"{icon} Dev Environment", status, f"{rt}ms")
    
with col2:
    icon, status, rt = get_env_status(health_staging_df)
    st.metric(f"{icon} Staging Environment", status, f"{rt}ms")
    
with col3:
    icon, status, rt = get_env_status(health_cloud_df)
    st.metric(f"{icon} Cloud Environment", status, f"{rt}ms")

# Health Trends
st.subheader("📈 Health Trends (Last 20 Checks)")

col1, col2 = st.columns(2)

with col1:
    st.write("**Response Times**")
    if not health_dev_df.empty and 'response_time_ms' in health_dev_df.columns:
        # Prepare data for plotting
        plot_data = []
        
        for env_name, df in [('Dev', health_dev_df), ('Staging', health_staging_df), ('Cloud', health_cloud_df)]:
            if not df.empty and 'response_time_ms' in df.columns:
                env_data = df.tail(20).copy()
                env_data['Environment'] = env_name
                plot_data.append(env_data[['timestamp', 'response_time_ms', 'Environment']])
        
        if plot_data:
            combined_data = pd.concat(plot_data, ignore_index=True)
            fig = px.line(combined_data, x='timestamp', y='response_time_ms', 
                         color='Environment', title="Response Times by Environment")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No health data available")
    else:
        st.info("No health data available")

with col2:
    st.write("**Uptime Statistics**")
    status_data = []
    for env_name, df in [('Dev', health_dev_df), ('Staging', health_staging_df), ('Cloud', health_cloud_df)]:
        if not df.empty and 'status' in df.columns:
            up_count = len(df[df['status'] == 'UP'])
            total = len(df)
            uptime = (up_count / total * 100) if total > 0 else 0
            status_data.append({
                'Environment': env_name, 
                'Uptime %': f"{uptime:.1f}%", 
                'Total Checks': total,
                'Status': '🟢' if uptime > 90 else '🟡' if uptime > 70 else '🔴'
            })
    
    if status_data:
        st.dataframe(pd.DataFrame(status_data), use_container_width=True)
    else:
        st.info("No status data available")

# Deploy History
st.subheader("🚀 Recent Deployments (Last 5 per Environment)")

if not deployment_df.empty and 'env' in deployment_df.columns:
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.write("**Dev Deployments**")
        dev_deploys = deployment_df[deployment_df['env'] == 'dev'].tail(5)
        if not dev_deploys.empty:
            st.dataframe(dev_deploys[['timestamp', 'action', 'status']], use_container_width=True)
        else:
            st.info("No dev deployments")
    
    with col2:
        st.write("**Staging Deployments**")
        staging_deploys = deployment_df[deployment_df['env'] == 'staging'].tail(5)
        if not staging_deploys.empty:
            st.dataframe(staging_deploys[['timestamp', 'action', 'status']], use_container_width=True)
        else:
            st.info("No staging deployments")
    
    with col3:
        st.write("**Cloud Deployments**")
        cloud_deploys = deployment_df[deployment_df['env'] == 'cloud'].tail(5)
        if not cloud_deploys.empty:
            st.dataframe(cloud_deploys[['timestamp', 'action', 'status']], use_container_width=True)
        else:
            st.info("No cloud deployments")
else:
    st.info("No deployment data available")

st.divider()

# Charts section
col1, col2 = st.columns(2)

with col1:
    st.subheader("📊 Response Times")
    if not monitor_df.empty and 'response_time' in monitor_df.columns:
        monitor_df['response_time'] = pd.to_numeric(monitor_df['response_time'], errors='coerce')
        fig = px.line(monitor_df.tail(50), y='response_time', 
                     title="Last 50 Response Times (seconds)")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No monitoring data available")

with col2:
    st.subheader("🚨 Issues Over Time")
    if not issue_df.empty and 'alert_type' in issue_df.columns:
        issue_counts = issue_df['alert_type'].value_counts()
        fig = px.pie(values=issue_counts.values, names=issue_counts.index,
                    title="Issue Types Distribution")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No issues recorded")

st.divider()

# Data tables
tab1, tab2, tab3, tab4 = st.tabs(["📋 Deployments", "📈 Monitoring", "🚨 Issues", "🔧 Healing"])

with tab1:
    st.subheader("Deployment Log")
    if not deployment_df.empty:
        st.dataframe(deployment_df.tail(20), use_container_width=True)
    else:
        st.info("No deployment data")

with tab2:
    st.subheader("Monitor Log")
    if not monitor_df.empty:
        st.dataframe(monitor_df.tail(20), use_container_width=True)
    else:
        st.info("No monitoring data")

with tab3:
    st.subheader("Issue Log")
    if not issue_df.empty:
        st.dataframe(issue_df.tail(20), use_container_width=True)
    else:
        st.info("No issues recorded")

with tab4:
    st.subheader("Healing Log")
    if not healing_df.empty:
        st.dataframe(healing_df.tail(20), use_container_width=True)
    else:
        st.info("No healing actions recorded")

# Auto-refresh
st.sidebar.markdown("---")
if st.sidebar.checkbox("Auto-refresh (30s)"):
    import time
    time.sleep(30)
    st.rerun()