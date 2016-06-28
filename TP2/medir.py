#!/usr/bin/env python2

import collections
import math
from geoip import geolite2
import sys
import time
import pickle

from scapy.all import *

# Universidades - http://www.webometrics.info/es/Europe

universidades = {'inglaterra' : 'leeds.ac.uk',
				'finlandia' : 'jyu.fi',
				'israel' : 'new.huji.ac.il',
				'italia' : 'www.uniroma1.it',
				'japon' : 'www.u-tokyo.ac.jp',
				'australia' : 'sydney.edu.au',
				'india': 'www.du.ac.in',
				'marruecos': 'www.uca.ma',
				'rusia': 'www.msu.ru',
				'canada': 'www.utoronto.ca',
				'iran': 'www.iust.ac.ir',
				'sudafrica': 'www.unisa.ac.za',
				'mexico': 'www.udem.edu.mx',
				'china': 'en.scut.edu.cn',
				'madagascar': 'www.univ-antananarivo.mg' , # esta esta buena, es una isla pasando africa
				'portugal': 'www.up.pt' ,
				'egipto': 'www.azhar.edu.eg' ,
				'austria': 'www.univie.ac.at' ,
				'suecia': 'www.lunduniversity.lu.se' ,
				'EEUU': 'www.harvard.edu' ,
				'nigeria': 'www.nou.edu.ng' ,
				'espania': 'www.uam.es' ,
				'oxford': 'www.ox.ac.uk' ,
				'islandia': 'english.hi.is' ,
				'indonesia': 'www.ui.ac.id'
				 }

# Constantes

max_ttl = 30

echo_reply = 0
echo_request = 11

repeat_limit = 3
cant_not_replys_limit = 3

class Salto:
	ttl = 0
	packet = None
	rtt = 0.0
	rtti = 0.0
	geoip = None
	cimbala = 0.0

	def __init__(self, **kwds):
		self.__dict__.update(kwds)

class Route:
	def __init__(self):
		self.hops = []

	def trace(self, hostname, name):
		
		self.hops = []

		hasReply = True
		print "Route: " + hostname

		cant_not_replys = 0
		for ttl in range(1,max_ttl+1):

			rtt_total = 0
			rtt_count = 0	
			for i in range(repeat_limit):
			
				packet = IP(dst=hostname, ttl=ttl) / ICMP()
				rtt = time.clock()
				answer = sr1(packet, timeout=1, verbose=0)
				rtt = time.clock() - rtt

				print str(rtt)
				
				answer_ip = ""

				if answer:
					rtt_total += rtt
					rtt_count += 1
					answer_ip = answer.src
					cant_not_replys = 0
				else:
					cant_not_replys += 1


			if rtt_count > 0:
				print str(rtt_total)
				print str(rtt_count)
				print "---------"
				rtt_prom = rtt_total / rtt_count
			else: 
				rtt_prom = 0

			record = None

			if answer:
				match = geolite2.lookup(answer_ip)
				if match is not None:
					record = match.country
				else:
					record = None
			
			self.hops.append(Salto(ttl=ttl, packet_ip=answer_ip, rtt=rtt_prom, geoip=record, cimbala=0.0))

			if answer:
				hop = str(answer.src)
				hop += "\t" + str(rtt_prom)
				if record:
					hop += "\tPosible locacion: " + str(record)
				print hop
			else:
				print "* * *"

			if (answer and answer.type == echo_reply) or cant_not_replys >= cant_not_replys_limit * repeat_limit:
				hasReply = True
				break

		if hasReply:
			with open("new_mediciones/" + str(name) + ".txt", 'wb') as f:
				pickle.dump(self.hops, f)

			print "Listo."
		else:
			print "Error."

def main(argv=sys.argv):
	route = Route()

	route.trace(universidades[argv[1]], argv[1])

if __name__ == '__main__':
	main()