#!/usr/bin/evn python
import sys
import scapy.all
import scapy as spy


if len(sys.argv)<1:
	sys.exit("python procesar.py archivopcap cantidad_paquetes")

packages = scapy.utils.rdpcap(sys.argv[1], int(sys.argv[2]))

cants = dict()
	

for packet in packages:
	if hasattr(packet,"type"):
		if packet.type==2054:
			if int(sys.argv[3]) == 0:
				print str(packet.psrc) + " -> " + str(packet.pdst) + " - Operation: " + str(packet.op)
			else:
				if packet.psrc in cants:
					if packet.pdst in cants[packet.psrc]:
						cants[packet.psrc][packet.pdst] = cants[packet.psrc][packet.pdst] + 1
					else:
						cants[packet.psrc][packet.pdst] = 1
				else:
					cants[packet.psrc] = dict()
					cants[packet.psrc][packet.pdst] = 1

if int(sys.argv[3])!=0:
	for keysrc in cants.keys():
		for keydst in cants[keysrc].keys():
			print  str(cants[keysrc][keydst]) + "\t| " + str(keysrc) + "\t| " + str(keydst)
