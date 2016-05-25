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
	lista = listaRepetidos(j,cantidadIteraciones)
	res = sr(IP(dst=paginaWeb,ttl=lista)/ICMP(type=8),timeout=tout)
	tiempoFinal = time.time()
	print 'TTL: ' + str(j)
	for packet in res[0]:
		print packet[1].src
		if packet[1].type==0:
			print 'Servidor Respondio'
	print 'tiempo total:' + str((tiempoFinal-tiempoInicial)*1000) + ' ms'
	j = j+1
