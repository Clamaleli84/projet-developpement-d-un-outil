import psutil
import time
cpu = psutil.cpu_percent(interval=1)
print(f"le CPU est utiliser à : {cpu}")

