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

#Função para o atuador (Bomba)
def ativarBomba(client,userdata,msg):
    m = msg.topic.split("/")
    p = msg.payload.decode().split(",")
    print(p)
    print(m)
    client.publish(publish_bomba,p[1])
    if p[1]=='1':
        print(1)
    else:
        print(2)

client = mqtt.Client(client_id)
client.username_pw_set(user,password)
client.connect(server,port)
client.on_message = ativarBomba
client.subscribe(subscribe_bomba)
client.loop_start()

while True:
    print("teste")
    time.sleep(2)

