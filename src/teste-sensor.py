import RPi.GPIO as GPIO
import paho.mqtt.client as mqtt
import dht11
import time
import datetime

user = 'db5a8060-3e2b-11ec-8da3-474359af83d7'
password = 'f56e60c61d27ffb784d9a78e776c19e695314deb'
client_id = 'c269e860-5ef2-11ec-8da3-474359af83d7'
server = 'mqtt.mydevices.com'
port = 1883

client = mqtt.Client(client_id)
client.username_pw_set(user,password)
client.connect(server,port)

# inicializando GPIO
GPIO.setwarnings(True)
GPIO.setmode(GPIO.BCM)

# lendo informações do pino GPIO 27
dados = dht11.DHT11(pin = 27)

try:
	while True:
		ambiente = dados.read()
		if ambiente.is_valid():
			print("Ultima leitura valida: " + str(datetime.datetime.now()))
			print("Temperatura: %-3.1f C" % ambiente.temperature)
			client.publish('v1/db5a8060-3e2b-11ec-8da3-474359af83d7/things/c269e860-5ef2-11ec-8da3-474359af83d7/data/0', ambiente.temperature)
			print("Umidade: %-3.1f %%" % ambiente.humidity)
			client.publish('v1/db5a8060-3e2b-11ec-8da3-474359af83d7/things/c269e860-5ef2-11ec-8da3-474359af83d7/data/1', ambiente.humidity)
		time.sleep(1)

except KeyboardInterrupt:
    print("Cleanup")
    GPIO.cleanup()