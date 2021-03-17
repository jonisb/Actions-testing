import subprocess

KodiCmd = ['kodi.exe', '-p']
proc = subprocess.Popen(KodiCmd)
print(proc.poll())