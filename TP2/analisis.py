#!/usr/bin/env python2

import collections
import math
from geoip import geolite2
import sys
import time
import pickle

class Salto:
	ttl = 0
	packet = None
	rtt = 0.0
	rtti = 0.0
	geoip = None
	cimbala = 0.0

	def __init__(self, **kwds):
		self.__dict__.update(kwds)

class Analisis:
	def __init__(self):
		self.hops = []

	def compare(self, x,y):
		if float(x.rtt) > float(y.rtt):
			return 1
		elif float(x.rtt) < float(y.rtt):
			return -1
		else:
			return 0

	def get_data(self, list):

		self.hops = list

		self.hops[0].rtti = self.hops[0].rtt
		last_rtt_not_zero = None

		self.hops.sort(self.compare)

		for i in range(1, len(self.hops)):
			print str(self.hops[i].ttl) + "\t" + str(self.hops[i].rtt)

		return True

		average = 0.0

		for hop in self.hops:
			average += hop.rtti

		average = average / float(len(self.hops))

		variance = 0.0

		for hop in self.hops:
			variance += pow(hop.rtti - average, 2)

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