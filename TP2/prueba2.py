from scapy.all import *
import time

res = sr(IP(dst=sys.argv[1],ttl=range(int(sys.argv[2])))/TCP(flags = 2),timeout=1)

print "paquetes recibidos\n"
res[0].display()

print "paquetes sin respuesta\n"
res[1].display()