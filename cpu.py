import psutil
import time
while (True){
  cpu = psutil.cpu_percent (interval=1)

  print(f"le CPU est utiliser à : {cpu}")

  time.sleep(30)
}
