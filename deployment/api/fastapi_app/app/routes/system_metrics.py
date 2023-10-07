from fastapi import APIRouter
import psutil

router = APIRouter()

@router.get("/battery")
async def get_battery_metrics():
    try:
        battery = psutil.sensors_battery()
        if battery:
            percent = battery.percent
            charging = battery.power_plugged
            battery_status = "Charging" if charging else "Discharging"
            return {"status": battery_status, "percent": percent}
        else:
            return {"status": "Not Available"}
    except Exception as e:
        return {"error": str(e)}

@router.get("/system")
async def get_system_metrics():
    uptime = psutil.boot_time()
    boot_time = psutil.datetime.datetime.fromtimestamp(uptime)
    return {"uptime_seconds": uptime, "boot_time": str(boot_time)}

@router.get("/network")
async def get_network_metrics():
    net_io = psutil.net_io_counters()
    return {"bytes_sent": net_io.bytes_sent, "bytes_received": net_io.bytes_recv}

@router.get("/disk")
async def get_disk_metrics():
    disk_usage = psutil.disk_usage('/')
    return {"disk_total": disk_usage.total, "disk_used": disk_usage.used, "disk_free": disk_usage.free, "disk_percent": disk_usage.percent}

@router.get("/cpu")
async def get_cpu_metrics():
    cpu_percent = psutil.cpu_percent(interval=1, percpu=True)
    return {"cpu_usage_per_core": cpu_percent}

@router.get("/memory")
async def get_memory_metrics():
    memory_info = psutil.virtual_memory()
    return {"memory_total": memory_info.total, "memory_used": memory_info.used, "memory_free": memory_info.free, "memory_percent": memory_info.percent}
