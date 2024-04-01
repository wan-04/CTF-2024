from scapy.all import *

pkts = rdpcap('secret-tunnels.pcapng')
dns_pkts = [p for p in pkts if p.haslayer(DNS)]
lst = ""
for p in dns_pkts:
    if p[DNS].qd.qtype == 1 and '.jerseyctf.com' in p[DNS].qd.qname.decode():
        s = p[DNS].qd.qname.decode()
        if (s.split('.')[0]) not in lst:
            lst += s.split('.')[0]
print(lst)
