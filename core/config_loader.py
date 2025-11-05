import json
import os

# Try to load dotenv if available
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # Continue without dotenv

def get_env_profile(env_name):
    """Load environment profile from config/env_profiles.json"""
    config_path = os.path.join("config", "env_profiles.json")
    
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Config file not found: {config_path}")
    
    with open(config_path, 'r') as f:
        profiles = json.load(f)
    
    if env_name not in profiles:
        raise ValueError(f"Environment '{env_name}' not found in profiles")
    
    profile = profiles[env_name].copy()
    
    # Override with environment variables if they exist
    for key, value in profile.items():
        env_key = f"{env_name.upper()}_{key.upper()}"
        env_value = os.getenv(env_key)
        if env_value:
            profile[key] = env_value
    
    return profile

def get_all_profiles():
    """Get all available environment profiles"""
    config_path = os.path.join("config", "env_profiles.json")
    
    with open(config_path, 'r') as f:
        return json.load(f)

def get_current_env():
    """Get current environment from ENV variable, default to 'dev'"""
    return os.getenv('ENV', 'dev')