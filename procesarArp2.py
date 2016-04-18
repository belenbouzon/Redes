#!/usr/bin/evn python
import sys
import scapy.all
import scapy as spy
import math


if len(sys.argv)<1:
	sys.exit("python procesar.py archivopcap cantidad_paquetes")

packages = scapy.utils.rdpcap(sys.argv[1], int(sys.argv[2]))

cantsSrc = dict()
cantsDst = dict()
cantsSrcReply = dict()
cantsDstReply = dict()

total = 0
tercerParametro = int(sys.argv[3])

for packet in packages:
	if hasattr(packet,"type"):
		if packet.type==2054:
			if tercerParametro == 0:
				print str(packet.psrc) + " -> " + str(packet.pdst) + " - Operation: " + str(packet.op)
			else:
				total = total + 1
				if packet.psrc in cantsSrc:
					cantsSrc[packet.psrc] = cantsSrc[packet.psrc] + 1
				else:
					cantsSrc[packet.psrc] = 1
					cantsSrcReply[packet.psrc] = 0
				if packet.pdst in cantsDst:
					cantsDst[packet.pdst] = cantsDst[packet.pdst] + 1
				else:
					cantsDst[packet.pdst] = 1
					cantsDstReply[packet.pdst] = 0

				if packet.op==2:
					cantsSrcReply[packet.psrc] = cantsSrcReply[packet.psrc] + 1
					cantsDstReply[packet.pdst] = cantsDstReply[packet.pdst] + 1

if tercerParametro!=0 and tercerParametro!=10:
	print "SRC:"
	for keysrc in cantsSrc.keys():
		print  str(cantsSrc[keysrc]) + "\t| " + str(keysrc)
	print "DST:"
	for keydst in cantsDst.keys():
		print  str(cantsDst[keydst]) + "\t| " + str(keydst)
	print "INFO SRC:"
	entropy = 0
	for keysrc in cantsSrc.keys():
		frecuency = float((cantsSrc[keysrc]))/float(total)
		if frecuency != 0:
			info = -1 * math.log(frecuency)
			print str(keysrc) + "\t| " + " - Info del evento: " + str(info)
			entropy += info*frecuency
	print "ENTROPY SRC: " + str(entropy)
	print "INFO DST:"
	entropy = 0
	for keydst in cantsDst.keys():
		frecuency = float((cantsDst[keydst]))/float(total)
		if frecuency != 0:
			info = -1 * math.log(frecuency)
			print str(keydst) + "\t| " + " - Info del evento: " + str(info)
			entropy += info*frecuency
	print "ENTROPY DST: " + str(entropy)
if tercerParametro==10:
	print "Request:\n"
	print "SRC:\n"
	for keysrc in cantsSrc.keys():
		print str(cantsSrc[keysrc]-cantsSrcReply[keysrc]) + "\t| " + str(keysrc)
	print "DST:\n"
	for keydst in cantsDst.keys():
		print  str(cantsDst[keydst]-cantsDstReply[keydst]) + "\t| " + str(keydst)
	print "Reply:\n"
	print "SRC:\n"
	for keysrc in cantsSrc.keys():
		if cantsSrcReply[keysrc]!=0:
			print "Reply" + str(cantsSrcReply[keysrc]) + "\t| " + str(keysrc)
	print "DST:\n"
	for keydst in cantsDst.keys():
		if cantsDstReply[keydst]!=0:
			print  "Reply" + str(cantsDstReply[keydst]) + "\t| " + str(keydst)
	print "INFO SRC:"
	entropy = 0
	for keysrc in cantsSrc.keys():
		frecuency = float((cantsSrc[keysrc])-cantsSrcReply[keysrc])/float(total)
		if frecuency != 0:
			info = -1 * math.log(frecuency)
			print "Request " + str(keysrc) + "\t| " + " - Info del evento: " + str(info)
			entropy += info*frecuency
			frecuency = float(cantsSrcReply[keysrc])/float(total)
			if frecuency != 0:
				info = -1 * math.log(frecuency)
				print "Request " + str(keysrc) + "\t| " + " - Info del evento: " + str(info)
				entropy += info*frecuency
	print "ENTROPY SRC: " + str(entropy)
	print "INFO DST:"
	entropy = 0
	for keydst in cantsDst.keys():
		frecuency = float((cantsDst[keydst])-cantsDstReply[keydsr])/float(total)
		if frecuency != 0:
			info = -1 * math.log(frecuency)
			print "Request " + str(keydst) + "\t| " + " - Info del evento: " + str(info)
			entropy += info*frecuency
			frecuency = float(cantsDstReply[keydst])/float(total)
			if frecuency != 0:
				info = -1 * math.log(frecuency)
				print "Request " + str(keydst) + "\t| " + " - Info del evento: " + str(info)
				entropy += info*frecuency
	print "ENTROPY DST: " + str(entropy)
