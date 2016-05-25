from scapy.all import *
import time
import atexit, sys

def listaRepetidos (numero,cantidad):
	lista = []
	i = int(0)
	while i<cantidad:
		lista.append(numero)
		i = i+1
if len(sys.argv) < 6:
	print '<pagina web> <ttlInicial> <ttlFinal> <cantidadIteraciones> <timeOut>'
	quit()

paginaWeb = sys.argv[1]
ttlInicial = int(sys.argv[2])
ttlFinal = int(sys.argv[3])
cantidadIteraciones = int(sys.argv[4])
tout = int(sys.argv[5])

j = ttlInicial
while j <= ttlFinal:
	tiempoInicial = time.time()
	res = sr(IP(dst=paginaWeb,ttl=listaRepetidos(numero=j,cantidad=cantidadIteraciones))/ICMP(type=8),timeout=tout)
	tiempoFinal = time.time()
	print 'TTL: ' + str(j)
	for packet in res[0]:
		print packet[1].src
		if packet.type==0:
			print 'Servidor Respondio'
	print 'tiempo total:' + str((tiempoFinal-tiempoInicial)*1000) + ' ms'
	j = j+1
