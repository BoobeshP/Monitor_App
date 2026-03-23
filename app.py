from flask import Flask, jsonify, render_template
import psutil
import socket
import time
from monitor_utils import extended_metrics

app = Flask(__name__)

START_TIME = time.time()

def get_uptime():
    uptime_seconds = int(time.time() - START_TIME)
    return f"{uptime_seconds} seconds"

@app.route("/")
def dashboard():
    data = {
        "hostname": socket.gethostname(),
        "cpu": psutil.cpu_percent(interval=1),
        "memory": psutil.virtual_memory().percent,
        "disk": psutil.disk_usage('/').percent,
        "uptime": get_uptime()
    }
    return render_template("dashboard.html", data=data)

@app.route("/health")
def health():
    return jsonify(status="UP")

@app.route("/metrics")
def metrics():
    return jsonify(
        hostname=socket.gethostname(),
        cpu_usage=psutil.cpu_percent(interval=1),
        memory_usage=psutil.virtual_memory().percent,
        disk_usage=psutil.disk_usage('/').percent,
        uptime=get_uptime()
    )
@app.route("/extended-metrics")
def extended():
    return extended_metrics()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
