import paho.mqtt.client as mqtt
import time
import json
import board
import digitalio
import busio
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn

user = 'db5a8060-3e2b-11ec-8da3-474359af83d7'
password = 'f56e60c61d27ffb784d9a78e776c19e695314deb'
client_id = 'efbe8170-5ef9-11ec-9f5b-45181495093e'
server = 'mqtt.mydevices.com'
port = 1883

client = mqtt.Client(client_id)
client.username_pw_set(user,password)
client.connect(server,port)

# Cria spi bus
spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)

# Cria o cs (chip select)
cs = digitalio.DigitalInOut(board.D5)

# Cria o objeto mcp
mcp = MCP.MCP3008(spi, cs)

# Cria uma entrada analógica no pino 0
canal = AnalogIn(mcp, MCP.P0)

print('Leitura dos valores do MCP3008, pressione Ctrl-C para sair...')

#Carrega os valores de calibração do sensor
with open("cap_config.json") as json_data_file:
    config_data = json.load(json_data_file)

def percent_translation(raw_val):
    per_val = abs((raw_val- config_data["sem_saturacao"])/(config_data["saturacao"]-config_data["sem_saturacao"]))*100
    return round(per_val, 3)

# Print do título da coluna
if __name__ == '__main__':
    print("----------  {:>5}\t{:>5}".format("Saturacao", "Voltagem\n"))
    while True:
        try:
            print("SENSOR SOLO: " + "{:>5}%\t{:>5.3f}".format(percent_translation(canal.value), canal.voltage))
            client.publish('v1/db5a8060-3e2b-11ec-8da3-474359af83d7/things/efbe8170-5ef9-11ec-9f5b-45181495093e/data/0', percent_translation(canal.value))
        except Exception as error:
            raise error
        except KeyboardInterrupt:
            print('Saindo do script')
        time.sleep(1)