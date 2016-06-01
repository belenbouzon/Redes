#! /usr/bin/env python
from scapy.all import *
import atexit, sys

# Al cerrar el programa, se corre generar_archivo
def generar_archivo():
    print "Generando archivo pcap (para Wireshark)"
    wrpcap("lectura.pcap", sniffed)
    print "Listo."

atexit.register(generar_archivo)

config.sniff_promisc = True

if __name__ == "__main__":
    global sniffed
    sniffed = sniff()