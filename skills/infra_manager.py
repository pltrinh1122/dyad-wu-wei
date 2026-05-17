import subprocess

def _verify_daemon_type(daemon_type: str):
    if daemon_type != 'systemd_user':
        raise ValueError(f"Unsupported daemon_type: {daemon_type}. Only 'systemd_user' is currently implemented.")

def start_daemon(service_name: str, daemon_type: str = 'systemd_user') -> str:
    """Starts the specified infrastructure daemon."""
    _verify_daemon_type(daemon_type)
    
    if daemon_type == 'systemd_user':
        subprocess.run(["systemctl", "--user", "start", service_name], check=True)
        return f"Successfully started daemon: {service_name}"
    return ""

def stop_daemon(service_name: str, daemon_type: str = 'systemd_user') -> str:
    """Stops the specified infrastructure daemon."""
    _verify_daemon_type(daemon_type)
    
    if daemon_type == 'systemd_user':
        subprocess.run(["systemctl", "--user", "stop", service_name], check=True)
        return f"Successfully stopped daemon: {service_name}"
    return ""

def get_daemon_status(service_name: str, daemon_type: str = 'systemd_user') -> str:
    """Gets the status of the specified infrastructure daemon."""
    _verify_daemon_type(daemon_type)
    
    if daemon_type == 'systemd_user':
        # is-active returns 0 if active, >0 otherwise. We don't want check=True because it throws an error if inactive
        result = subprocess.run(["systemctl", "--user", "is-active", service_name], capture_output=True, text=True)
        return result.stdout.strip()
    return ""
