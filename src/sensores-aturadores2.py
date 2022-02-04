#Biblioteca de comunicação
import paho.mqtt.client as mqtt

#Bibliotecas sensor capacitivo
import time
import json
import board
import digitalio
import busio
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn

#Bibliotecas umidade do ar
import RPi.GPIO as GPIO
import paho.mqtt.client as mqtt
import dht11
#import time
import datetime

#Configuração protocolo de comunicação
user = 'db5a8060-3e2b-11ec-8da3-474359af83d7'
password = 'f56e60c61d27ffb784d9a78e776c19e695314deb'
client_id = '8a3d3e70-7a4e-11ec-a681-73c9540e1265'
server = 'mqtt.mydevices.com'
port = 1883

#Configuração para receber e publicar informação da Cayenne
subscribe_bomba = "v1/"+str(user)+"/things/"+str(client_id)+"/cmd/17"
publish_bomba = "v1/"+str(user)+"/things/"+str(client_id)+"/data/17"

subscribe_cooler = "v1/"+str(user)+"/things/"+str(client_id)+"/cmd/23"
publish_cooler = "v1/"+str(user)+"/things/"+str(client_id)+"/data/23"

#Função para os atuadores
def atuadores(client,userdata,msg):
    m = msg.topic.split("/")
    p = msg.payload.decode().split(",")
    if m[-1]=='17': #bomba
        if p[1]=='1':
            client.publish(publish_bomba,1)
            GPIO.output(17, GPIO.LOW)
        else:
            client.publish(publish_bomba,0)
            GPIO.output(17, GPIO.HIGH)
    if m[-1]=='23': #cooler
        if p[1]=='1':
            client.publish(publish_cooler,1)
            GPIO.output(23, GPIO.LOW)
        else:
            client.publish(publish_cooler,0)
            GPIO.output(23, GPIO.HIGH)

client = mqtt.Client(client_id)
client.username_pw_set(user,password)
client.connect(server,port)
client.on_message = atuadores

client.subscribe(subscribe_bomba)
client.subscribe(subscribe_cooler)
client.loop_start()

# Cria spi bus
spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)

# Cria o cs (chip select)
cs = digitalio.DigitalInOut(board.D5)

# Cria o objeto mcp
mcp = MCP.MCP3008(spi, cs)

# Cria uma entrada analógica no pino 0
canal = AnalogIn(mcp, MCP.P0)

# inicializando GPIO
GPIO.setwarnings(True)
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.OUT)
GPIO.setup(23, GPIO.OUT)

# lendo informações do pino GPIO 27
dados = dht11.DHT11(pin = 27)

print('Leitura dos valores do MCP3008, pressione Ctrl-C para sair...')

#Carrega os valores de calibração do sensor
with open("cap_config.json") as json_data_file:
    config_data = json.load(json_data_file)

def percent_translation(raw_val):
    per_val = abs((raw_val- config_data["sem_saturacao"])/(config_data["saturacao"]-config_data["sem_saturacao"]))*100
    return round(per_val, 3)

# Print do título da coluna
if __name__ == '__main__':
    #i=0
    while True:
        ambiente = dados.read()
        try:
            if ambiente.is_valid():
                #i+=1
                #ambiente.temperature += i
                print("Ultima leitura valida: " + str(datetime.datetime.now()))
                print("Temperatura: %-3.1f C" % ambiente.temperature)
                client.publish('v1/db5a8060-3e2b-11ec-8da3-474359af83d7/things/8a3d3e70-7a4e-11ec-a681-73c9540e1265/data/0', ambiente.temperature)
                print("Umidade: %-3.1f %%" % ambiente.humidity)
                client.publish('v1/db5a8060-3e2b-11ec-8da3-474359af83d7/things/8a3d3e70-7a4e-11ec-a681-73c9540e1265/data/1', ambiente.humidity)
                print("----------  {:>5}\t{:>5}".format("Saturacao", "Voltagem"))
                print("Sensor Solo: " + "{:>5}%\t{:>5.3f}\n".format(percent_translation(canal.value), canal.voltage))
                client.publish('v1/db5a8060-3e2b-11ec-8da3-474359af83d7/things/8a3d3e70-7a4e-11ec-a681-73c9540e1265/data/2', percent_translation(canal.value))
        except Exception as error:
            raise error
        except KeyboardInterrupt:
            print('Saindo do script')
            print("Cleanup")
            GPIO.cleanup()
        time.sleep(10)