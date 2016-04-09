from scapy.all import *
def monitor_callback(pkt):
	print pkt.show()

if __name__ == '__main__' :
	sniff(prn=monitor_callback , store = 0)
