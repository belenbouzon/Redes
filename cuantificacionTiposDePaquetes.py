import sys
import scapy.all
from utils import *

if len(sys.argv)<1:
	sys.exit("Contabilizando tipos de paquetes \n")

packages = scapy.utils.rdpcap(sys.argv[1], int(sys.argv[2]))

cants = dict()
for packet in packages:
	if packet.type in cants:
		cants[packet.type] = cants[packet.type] + 1
	else:
		cants[packet.type] = 1

print "\n\nQUANT\t| TYPE\r"
for key in cants.keys():
	print  str(cants[key]) + "\t| " + str( hex_to_packet( hex(key) ) ) + "\r"
