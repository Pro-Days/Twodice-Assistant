import psutil


def get_resource_info():
    """Returns CPU, MEM, DISK usage in percentage."""
    return (
        psutil.cpu_percent(interval=1),
        psutil.virtual_memory().percent,
        psutil.disk_usage("/").percent,
    )


if __name__ == "__main__":
    cpu, mem, disk = get_resource_info()

    print(f"CPU: {cpu}%")
    print(f"MEM: {mem}%")
    print(f"DISK: {disk}%")
