import time
import json
import board
import digitalio
import busio
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn

# Cria spi bus
spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)

# Cria o cs (chip select)
cs = digitalio.DigitalInOut(board.D5)

# Cria o objeto mcp
mcp = MCP.MCP3008(spi, cs)

# Cria uma entrada analógica no pino 0
canal = AnalogIn(mcp, MCP.P0)

max_val = None
min_val = None

seco_check = input("O sensor capacitivo está fora da água? (Pressione 'y' para continuar): ")
if seco_check == 'y':
    max_val = canal.value
    print("---------{:>5}\t{:>5}".format("puro", "v"))
    for x in range(0, 30):
        if canal.value > max_val:
            max_val = canal.value
        print("CANAL 0: "+"{:>5}\t{:>5.3f}".format(canal.value, canal.voltage))
        time.sleep(1)

print('\n')

molhado_check = input("O sensor capacitivo está dentro da água? (Pressione 'y' para continuar): ")
if molhado_check == 'y':
    min_val = canal.value
    print("---------{:>5}\t{:>5}".format("puro", "v"))
    for x in range(0, 30):
        if canal.value < min_val:
            min_val = canal.value
        print("CANAL 0: "+"{:>5}\t{:>5.3f}".format(canal.value, canal.voltage))
        time.sleep(1)

config_data = dict()
config_data["saturacao"] = min_val
config_data["sem_saturacao"] = max_val
with open('cap_config.json', 'w') as outfile:
    json.dump(config_data, outfile)
print('\n')
print(config_data)
#    time.sleep(0.5)