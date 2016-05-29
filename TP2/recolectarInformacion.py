from scapy.all import *
import time
import atexit, sys

#www.u-tokyo.ac.jp

def listaRepetidos (numero,cantidad):
	lista = []
	i = int(0)
	while i<cantidad:
		lista.append(numero)
		i = i+1
	return lista
if len(sys.argv) < 7:
	print '<pagina web> <ttlInicial> <ttlFinal> <cantidadIteraciones> <timeOut> <cantidadIntentos>'
	print 'Agregar --noReintentar si no se quiere que se vuelva a iterar sobre una coneccion que no contesto'
	quit()

paginaWeb = sys.argv[1]
ttlInicial = int(sys.argv[2])
ttlFinal = int(sys.argv[3])
cantidadIteraciones = int(sys.argv[4])
tout = int(sys.argv[5])
cantidadIntentos = int(sys.argv[6])
sinIteracionesDeColgados = False

if len(sys.argv)>=8 and sys.argv[7]=='--noReintentar':
	sinIteracionesDeColgados = True

j = ttlInicial
while j <= ttlFinal:
	tiempo = 0
	contesto = False
	iteracion = 0
	respondieron = 0
	tiempoConIteraciones = 0
	while iteracion<=cantidadIteraciones:
		intentos = 0
		while contesto==False and intentos<=cantidadIntentos:
			tiempoInicial = time.time()
			res = sr(IP(dst=paginaWeb,ttl=j)/ICMP(type=8),timeout=tout)
			tiempoFinal = time.time()
			intentos = intentos + 1
			if len(res[0])!=0:
				contesto = True
				tiempo = tiempoFinal-tiempoInicial
				tiempoConIteraciones = tiempoConIteraciones + tiempo
				respondieron = respondieron + 1
		iteracion = iteracion + 1
		if sinIteracionesDeColgados==True and contesto==False:
			iteracion = cantidadIteraciones + 1
	#print 'TTL: ' + str(j)
	sys.stderr.write('TTL: ' + str(j) + '\n')
	if respondieron > 0:
		contesto = True
		tiempoConIteraciones = tiempoConIteraciones/respondieron
	if contesto==True:
		servidorRespondio = False
		for packet in res[0]:
			#print packet[1].src
			sys.stderr.write(str(packet[1].src) + '\n')
			if packet[1].type==0:
				servidorRespondio = True
		#print 'tiempo total:' + str(tiempoConIteraciones)*1000) + ' ms'
		sys.stderr.write('tiempo total:' + str((tiempoConIteraciones)*1000) + ' ms\n')
		if servidorRespondio==True:
			#print 'Servidor Respondio'
			sys.stderr.write('Servidor Respondio\n')
			sys.exit(0)
	else:
		#print 'NO CONTESTO'
		sys.stderr.write('NO CONTESTO\n')
	j = j+1
