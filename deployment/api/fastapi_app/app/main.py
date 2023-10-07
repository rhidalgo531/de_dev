from fastapi import FastAPI, HTTPException
from app.routes.system_metrics import (
    get_battery_metrics,
    get_system_metrics,
    get_network_metrics,
    get_disk_metrics,
    get_cpu_metrics,
    get_memory_metrics
)
from app.config import PostgresSettings 
from .routes import system_metrics

import asyncpg


app = FastAPI()
app.include_router(
    system_metrics.router  
)

@app.get("/")
async def root():
    return {"message": "Hello World"}

# Define a function to insert metrics into the PostgreSQL database
async def insert_metrics(metrics):
    try:
        db_config = PostgresSettings 
        conn = await asyncpg.connect(
            user=db_config.FASTAPI_DB_USER,
            password=db_config.FASTAPI_DB_PASSWORD,
            database=db_config.POSTGRES_DB,
            host=db_config.POSTGRES_HOST,
        )

        # Insert metrics into a "metrics" table
        await conn.execute(
            """
            INSERT INTO system_health (battery_status, battery_percent, uptime_seconds, bytes_sent, bytes_received, 
            disk_total, disk_used, disk_free, disk_percent, cpu_usage, memory_percent)
            VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11)
            """,
            metrics["battery"]["status"],
            metrics["battery"]["percent"],
            metrics["system"]["uptime_seconds"],
            metrics["network"]["bytes_sent"],
            metrics["network"]["bytes_received"],
            metrics["disk"]["disk_total"],
            metrics["disk"]["disk_used"],
            metrics["disk"]["disk_free"],
            metrics["disk"]["disk_percent"],
            metrics["cpu"]["cpu_usage_per_core"],
            metrics["memory"]["memory_percent"],
        )
        await conn.close()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/snapshot")
async def snapshot_metrics():
    try:
        # Collect all metric groups
        battery_metrics = get_battery_metrics()
        system_metrics = get_system_metrics()
        network_metrics = get_network_metrics()
        disk_metrics = get_disk_metrics()
        cpu_metrics = get_cpu_metrics()
        memory_metrics = get_memory_metrics()

        # Create a dictionary to hold all metric groups
        all_metrics = {
            "battery": battery_metrics,
            "system": system_metrics,
            "network": network_metrics,
            "disk": disk_metrics,
            "cpu": cpu_metrics,
            "memory": memory_metrics,
        }

        # Insert metrics into the PostgreSQL database
        await insert_metrics(all_metrics)

        return {"message": "Metrics snapshot successfully inserted into the database."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
