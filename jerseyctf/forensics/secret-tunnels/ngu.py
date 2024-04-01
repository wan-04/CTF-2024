from scapy.all import *


out = b""

packets = rdpcap('final.pcapng')
packets.sort(key=lambda x: x.time) 
ngu = []
for packet in packets:
    if packet.haslayer(TCP):
        tcp_packet = packet.getlayer(TCP)
        ip = packet.getlayer(IP)
        if ip.src == "10.0.2.7":
            print(tcp_packet)
            
            if tcp_packet.haslayer(Raw):
                data = (tcp_packet[Raw].load)[-4:]
                print(data.hex())
                if b'\x01' not in data:
                    ngu.append(data.hex())
ngu.sort()
print(ngu)
for i in ngu:
    print(i[6:], end = ' ')
print(out)