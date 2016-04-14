#!/usr/bin/evn python
import sys
import scapy.all


if len(sys.argv)<1:
	sys.exit("python procesar.py archivopcap cantidad_paquetes")

packages = scapy.utils.rdpcap(sys.argv[1], int(sys.argv[2]))

for packet in packages:
	print str(packet.src) + " -> " + str(packet.dst) + " - Type: " + str(packet.type)