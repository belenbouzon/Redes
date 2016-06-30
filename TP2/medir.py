#!/usr/bin/env python2

import collections
import math
from geoip import geolite2
import sys
import time
import pickle
from pprint import pprint

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

cant_not_replys_limit = 3

class Salto:
	ttl = 0
	packet = None
	rtt = 0.0
	geoip = None
	confianza = 0.0

	def __init__(self, **kwds):
		self.__dict__.update(kwds)

class Route:
	def __init__(self):
		self.hops = []

	def trace(self, hostname, name, repeat_limit):
		
		repeat_limit = int(repeat_limit)
		self.hops = []

		hasReply = True
		print "Route: " + hostname

		cant_not_replys = 0
		for ttl in range(1,max_ttl+1):

			rtt_total = 0
			rtt_count = 0	

			ips_hops = []
			ips_count = dict()

			for i in range(repeat_limit):
			
				packet = IP(dst=hostname, ttl=ttl) / ICMP()
				a,u = sr(packet, timeout=1, verbose=0)	

				if len(u) > 0:
					continue
					
				answer = a[0][1]
				rtt = a[0][1].time - a[0][0].sent_time

				if answer:
					ip = answer.src
					if ip in ips_count:
						ips_count[ip] = ips_count[ip]+1
					else:
						ips_count[ip] = 1
					new_answer = {"ip": ip, "rtt": rtt}

					ips_hops.append(new_answer)

			if(len(ips_hops) == 0):
				continue

			ips_sorted = sorted(ips_count, key=ips_count.get,  reverse=True)

			ip_ganadora = ips_sorted[0]

			ips_count = ips_count[ip_ganadora]

			rtt = 0
			for hop in ips_hops:
				if hop['ip'] == ip_ganadora:
					rtt = rtt+ hop['rtt']

			rtt = rtt/ips_count
			confianza = ips_count/repeat_limit



			match = geolite2.lookup(ip_ganadora)
		 	if match is not None:
		 		record = match.country
			else:
		 		record = None

		 	self.hops.append(
		 		Salto(ttl=ttl,
		 			packet_ip=ip_ganadora,
		 			rtt=rtt,
		 			geoip=record,
		 			ips_count=ips_count,
		 			confianza=confianza
		 		)
		 	)

		 	print str(ip_ganadora) + "\t" + str(rtt) + "\t" + str(confianza) + "\t" + str(record)

			if (answer and answer.type == echo_reply):
				hasReply = True
			 	break

		if hasReply:
			with open("new_mediciones/" + str(name) + "-" + str(repeat_limit) + ".txt", 'wb') as f:
				pickle.dump(self.hops, f)

			print "Listo."
		else:
			print "Error."

def main(argv=sys.argv):
	route = Route()

	route.trace(universidades[argv[1]], argv[1], argv[2])

if __name__ == '__main__':
	main()