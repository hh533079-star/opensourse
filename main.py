from fastapi import FastAPI
import psutil
import subprocess

app = FastAPI()

@app.get("/system")
def system_info():
    return {
        "cpu": psutil.cpu_percent(),
        "memory": psutil.virtual_memory().percent,
        "disk": psutil.disk_usage('/').percent
    }

@app.get("/battery")
def battery():
    batt = psutil.sensors_battery()
    if batt:
        return {"percent": batt.percent, "plugged": batt.power_plugged}
    return {"error": "No battery info"}

@app.get("/ports")
def ports():
    result = subprocess.check_output("ss -tuln", shell=True).decode()
    return {"ports": result}

@app.get("/docker")
def docker_status():
    try:
        result = subprocess.check_output("docker ps", shell=True).decode()
        return {"containers": result}
    except:
        return {"error": "Docker not running"}