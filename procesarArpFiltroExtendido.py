#!/usr/bin/evn python
import sys
import scapy.all
import scapy as spy
import math


if len(sys.argv)<1:
	sys.exit("python procesar.py archivopcap cantidad_paquetes")

packages = scapy.utils.rdpcap(sys.argv[1], int(sys.argv[2]))

cants = dict()
cantsReply = dict()
	

total = 0
tercerParametro = int(sys.argv[3])

for packet in packages:
	if hasattr(packet,"type"):
		if packet.type==2054:
			total = total + 1
			if packet.psrc != "0.0.0.0" and packet.pdst!= "0.0.0.0" :
				if packet.psrc in cants:
					if packet.pdst in cants[packet.psrc]:
						cants[packet.psrc][packet.pdst] = cants[packet.psrc][packet.pdst] + 1
					else:
						cants[packet.psrc][packet.pdst] = 1
						cantsReply[packet.psrc][packet.pdst] = 0
				else:
					cants[packet.psrc] = dict()
					cants[packet.psrc][packet.pdst] = 1
					cantsReply[packet.psrc] = dict()
					cantsReply[packet.psrc][packet.pdst] = 0
				if packet.op==2:
					cantsReply[packet.psrc][packet.pdst] = cantsReply[packet.psrc][packet.pdst] + 1

if tercerParametro!=0 and tercerParametro!=10:
	for keysrc in cants.keys():
		for keydst in cants[keysrc].keys():
			print  str(cants[keysrc][keydst]) + "\t| " + str(keysrc) + "\t| " + str(keydst)
	entropy = 0
	for keysrc in cants.keys():
		for keydst in cants[keysrc].keys():
			#print str(keysrc)
			frecuency = float((cants[keysrc][keydst]))/float(total)
			if frecuency != 0:
				info = -1 * math.log(frecuency)
				print str(keysrc) + "\t| " + str(keydst) + "\t| " + " - Info del evento: " + str(info)
				entropy += info*frecuency
	print "ENTROPY: " + str(entropy)

if tercerParametro==10:
	for keysrc in cants.keys():
		for keydst in cants[keysrc].keys():
			print  str(cants[keysrc][keydst]) + "\t| " + str(keysrc) + "\t| " + str(keydst)
	entropy = 0
	for keysrc in cants.keys():
		for keydst in cants[keysrc].keys():
			frecuency = float((cants[keysrc][keydst]-cantsReply[keysrc][keydst]))/float(total)
			if frecuency != 0:
				info = -1 * math.log(frecuency)
				print "Request " + str(keysrc) + "\t| " + str(keydst) + "\t| " + " - Info del evento: " + str(info)
				entropy += info*frecuency
				if cantsReply[keysrc][keydst]!=0:
					frecuency = float((cantsReply[keysrc][keydst]))/float(total)
					info = -1 * math.log(frecuency)
					print "Request " + str(keysrc) + "\t| " + str(keydst) + "\t| " + " - Info del evento: " + str(info)
					entropy += info*frecuency
	print "ENTROPY: " + str(entropy)
