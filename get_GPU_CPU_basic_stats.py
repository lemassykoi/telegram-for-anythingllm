import GPUtil
import psutil
from pynvml import *

## Get GPU Infos
nvmlInit()
h = nvmlDeviceGetHandleByIndex(0)
info = nvmlDeviceGetMemoryInfo(h)
#vram_total = info.total
vram_total = round(info.total / 1024 **3)
vram_free  = round((info.free / 1024 **3), 2)
vram_used  = round((info.used / 1024 **3), 2)

## Get GPU Temperature
gpu = GPUtil.getGPUs()[0]

## Get RAM Infos
def get_ram():
    mem = psutil.virtual_memory()
    free = mem.available / 1024 ** 3
    total = mem.total / 1024 ** 3
    used = round((total - free), 2)
    total = round(total)
    return used, total

used, total = get_ram()
message = []
message.append('Used RAM GPU : ' + str(vram_used) + ' / ' + str(vram_total) + ' Go')
message.append('Temp.    GPU : ' + str(gpu.temperature) + ' °C')
message.append('Used RAM CPU : ' + str(used) + ' / ' + str(total) + ' Go')

## Print values
for line in message:
    print(line)
