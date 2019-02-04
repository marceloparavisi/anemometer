#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

import string
import time
from serial import Serial

import rospy
from std_msgs.msg import Float32

rospy.init_node('anemoter')
pubWindSpeed = rospy.Publisher('windSpeed', Float32, queue_size=1)
pubWindDirection = rospy.Publisher('windDirection', Float32, queue_size=1)



# Iniciando conexao serial
comport = Serial('/dev/ttyACM0', 9600)
#comport = serial.Serial('/dev/ttyUSB0', 9600, timeout=1) # Setando timeout 1s para a conexao

PARAM_CARACTER='t'
PARAM_ASCII=str(chr(116))       # Equivalente 116 = t

# Time entre a conexao serial e o tempo para escrever (enviar algo)
time.sleep(1.8) # Entre 1.5s a 2s

#comport.write(PARAM_CARACTER)
comport.write(PARAM_ASCII)

while not rospy.is_shutdown():
	lineRead = comport.readline()

	indiceDirecao=string.find(lineRead,'Direcao a :')
	if (indiceDirecao>=0):
		indiceDirecao=indiceDirecao+11
		indiceGraus = string.find(lineRead,' graus')
		textoDirecao = lineRead[indiceDirecao:indiceGraus]
		print "DIRECAO:",textoDirecao
		pubWindDirection.publish(float(textoDirecao))

	indiceWindSpeed=string.find(lineRead,'Wind speed: ')
	if (indiceWindSpeed>=0):
		indiceWindSpeed=indiceWindSpeed+12
		indiceUnidade = string.find(lineRead,' [m/s]')
		textoWindSpeed = lineRead[indiceWindSpeed:indiceUnidade]
		print "SPEED:", textoWindSpeed
		pubWindSpeed.publish(float(textoWindSpeed))

# Fechando conexao serial
comport.close()
