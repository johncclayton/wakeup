import os 

def get_sub_settings():
    pub_bind_port = os.getenv("MOTION_PUB_BIND_PORT", 8000)

    return (
        os.getenv("MOTION_SUB_CONNECT_HOST", "localhost"),
        os.getenv("MOTION_SUB_CONNECT_PORT", pub_bind_port),
    )
    
def get_pub_settings():
    pub_sensor_pin = os.getenv("MOTION_PUB_SENSOR_PIN", 4)
    pub_bind_host = os.getenv("MOTION_PUB_BIND_HOST", "*")
    pub_bind_port = os.getenv("MOTION_PUB_BIND_PORT", 8000)
    pub_prom_port = os.getenv("MOTION_PROM_PUB_PORT", 9091)
    pub_time_delay_sec = os.getenv("MOTION_PUB_TIMEDELAY", 1.0)

    return (
        pub_sensor_pin,
        pub_bind_host,
        pub_bind_port,
        pub_prom_port,
        pub_time_delay_sec
    )
