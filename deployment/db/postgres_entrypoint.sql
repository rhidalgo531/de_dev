CREATE DATABASE reporting; 
CREATE TABLE reporting.system_health (
    id SERIAL PRIMARY KEY,
    battery_status VARCHAR(255),
    battery_percent INTEGER,
    uptime_seconds BIGINT,
    bytes_sent BIGINT,
    bytes_received BIGINT,
    disk_total BIGINT,
    disk_used BIGINT,
    disk_free BIGINT,
    disk_percent REAL,
    cpu_usage JSONB,
    memory_percent REAL
);



CREATE USER lightdash WITH PASSWORD 'lightdash_password'; 
CREATE USER fastapi WITH PASSWORD 'fastapi_password';

GRANT SELECT ON SCHEMA reporting TO lightdash;
GRANT INSERT ON TABLE reporting.system_health TO fastapi;




