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
	geoip = None
	confianza = 0.0

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
		self.filtered_hopes = []

		self.hops[0].diff_rtt = self.hops[0].rtt
		last_rtt_not_zero = 0

		# Primera pasada para calcular el diff_rtt de cada uno
		for i in range(1, len(self.hops)):
			
			if self.hops[i].packet_ip != "":
				if self.hops[i-1].rtt == 0:
					self.hops[i].diff_rtt = self.hops[i].rtt - last_rtt_not_zero
					last_rtt_not_zero = self.hops[i].diff_rtt
					self.filtered_hopes.append(self.hops[i])
				elif self.hops[i].rtt <= self.hops[i-1].rtt:
					self.hops[i].diff_rtt = 0.0
				else:
					self.hops[i].diff_rtt = self.hops[i].rtt - self.hops[i-1].rtt
					last_rtt_not_zero = self.hops[i].diff_rtt
					self.filtered_hopes.append(self.hops[i])

			print str(self.hops[i].packet_ip) + "\t" + str(self.hops[i].rtt) + "\t" + str(self.hops[i].diff_rtt) + "\t" + str(self.hops[i].geoip)

		# Calculo de algunas variables
		print "=========================="
		outlier = True
		while(outlier):
			average = 0.0
			count = len(self.filtered_hopes)
			for hop in self.filtered_hopes:
				average += hop.diff_rtt

			average = average / count

			variance = 0.0
			for hop in self.hops:
				variance += pow(hop.diff_rtt - average, 2)

			variance = variance / float(count)
			standard_deviation = math.sqrt(variance)

			for hop in self.filtered_hopes:
				hop.delta = abs(hop.diff_rtt - average)

			self.filtered_hopes.sort(self.compare)

			candidate = self.filtered_hopes[0]

			thompson_limit = float(candidate.delta / standard_deviation)

			print candidate.packet_ip
			print thompson_limit
			print thompson[count]

			if thompson_limit > thompson[count]:
				print 'Outlier: ' + str(candidate.packet_ip)
				self.filtered_hopes.pop(0)
			else:
				print 'No mas outliers'
				outlier = False

def main(argv=sys.argv):
	analisis = Analisis()


	with open("new_mediciones/inglaterra-10.txt", 'rb') as f:
	    my_list = pickle.load(f)

	analisis.get_data(my_list)

if __name__ == '__main__':
	main()