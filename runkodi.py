import subprocess
import time

KodiCmd = ['kodi.exe', '-p']
proc = subprocess.Popen(KodiCmd)
time.sleep(5)
print(proc.poll())