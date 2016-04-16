from __future__ import division
import sys
import scapy.all
import math
from utils import *

if len(sys.argv) < 3:
	sys.exit("Uso: cuantificacionTiposDePaquetes.py {archivolectura.pcap} {cantidad de paquetes / -1 es todos}\n")

packages = scapy.utils.rdpcap(sys.argv[1], int(sys.argv[2]))

cants = dict()
for packet in packages:
	
	# Si no tiene type, lo ignoro...
	if not hasattr(packet, 'type'):
		continue

	if packet.type in cants:
		cants[packet.type] = cants[packet.type] + 1
	else:
		cants[packet.type] = 1

print "\n\nQUANT\t| TYPE\r"
for key in cants.keys():
	print  str(cants[key]) + "\t| " + str( hex_to_packet( hex(key) ) ) + "\r"

print "\n####\n"

total = len(packages)

entropy = 0

for key in cants.keys():
	frecuency = (cants[key])/total
	info = -1 * math.log(frecuency)
	print str( hex_to_packet( hex(key) ) ) + " - Info del evento: " + str(info)

	entropy += info*frecuency
	print "\n"

print "ENTROPY: " + str(entropy)