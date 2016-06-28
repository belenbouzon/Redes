#!/usr/bin/env python2

import collections
import math
from geoip import geolite2
import sys
import time
import pickle

## Modified Thompson de Cimbala
## Uso: thompson[n]. Por ejemplo, thompson[3] retorna 1.1511
thompson = [0, 0, 0, 1.1511, 1.4250, 1.5712, 1.6563, 1.7110, 1.7491, 1.7770, 1.7984, 1.8153, 1.8290, 1.8403, 1.8498, 1.8579, 1.8649, 1.8710, 1.8764, 1.8811, 1.8853, 1.8891, 1.8926, 1.8957, 1.8985, 1.9011, 1.9035, 1.9057, 1.9078, 1.9096, 1.9114, 1.9130, 1.9146]

class Salto:
	ttl = 0
	packet = None
	rtt = 0.0
	rtti = 0.0
	geoip = None
	cimbala = 0.0
	delta = 0.0

	def __init__(self, **kwds):
		self.__dict__.update(kwds)

class Analisis:
	def __init__(self):
		self.hops = []

	def compare(self, x,y):
		if float(x.delta) > float(y.delta):
			return -1
		elif float(x.delta) < float(y.delta):
			return 1
		else:
			return 0

	def get_data(self, list):

		self.hops = list

		self.hops[0].rtti = self.hops[0].rtt
		last_rtt_not_zero = None

		# Primera pasada para calcular el rtti de cada uno
		for i in range(1, len(self.hops)):
			if self.hops[i].packet_ip != "":
				if self.hops[i].rtt <= self.hops[i-1].rtt:
					self.hops[i].rtti = 0.0
				else:
					self.hops[i].rtti = self.hops[i].rtt - self.hops[i-1].rtt

		# Calculo de algunas variables

		average = 0.0
		for hop in self.hops:
			average += hop.rtti

		average = average / float(len(self.hops))

		for hop in self.hops:
			hop.delta = abs(hop.rtti - average)

		self.hops.sort(self.compare)

		candidate = self.hops[0]

		for hop in self.hops:
			print str(hop.ttl) + "\t" + str(hop.rtti) + "\t" + str(hop.delta)

		return True
		variance = 0.0


		variance = variance / float(len(self.hops)-1)
		standard_deviation = math.sqrt(variance)

		print "Average: " + str(average).replace('.', ',')
		print "Variance: " + str(variance).replace('.', ',')
		print "Standard Deviation: " + str(standard_deviation).replace('.', ',')

		print "Average+SD: " + str(average + standard_deviation).replace('.', ',')
		print "Average-SD: " + str(average - standard_deviation).replace('.', ',')

		line = "IP\t"
		line += "\t" + "Pais"
		line += "\t" + "RTTI Intervalo"
		line += "\t" + "Cimbala"
		print line
		print "-" * 80

		for hop in self.hops:
			line = ""

			if hop.packet_ip != "":
				hop.cimbala = 0 # Deberiamos hacer la cuenta

				line += hop.packet_ip

			else:
				line += "***.***.***.***"

			line += "\t" + str(hop.geoip).replace('.', ',')
			line += "\t" + str(hop.rtti).replace('.', ',')
			line += "\t" + str(hop.cimbala).replace('.', ',')
			
			print line

def main(argv=sys.argv):
	analisis = Analisis()


	with open("new_mediciones/inglaterra.txt", 'rb') as f:
	    my_list = pickle.load(f)

	analisis.get_data(my_list)

if __name__ == '__main__':
	main()