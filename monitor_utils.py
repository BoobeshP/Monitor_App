cat << EOF > monitor_utils.py
import psutil
import time

def extended_metrics():
    return {
        "cpu_count": psutil.cpu_count(),
        "boot_time": time.ctime(psutil.boot_time()),
        "load_avg": psutil.getloadavg()
    }
EOF
