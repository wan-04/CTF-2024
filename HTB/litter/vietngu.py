from scapy.all import *
from string import printable


def process_packet(packet):
    if packet.haslayer(DNS):
        dns_packet = packet[DNS]
        if dns_packet.qr == 0:
            queried_domain = dns_packet.qd.qname.decode()
            if ".microsofto365.com" in queried_domain:
                filtered_domain = queried_domain.replace(
                    ".microsofto365.com", "").replace('.', '')
                byte_hex = bytes.fromhex(filtered_domain)
                res = ""
                for i in byte_hex:
                    if chr(i) in printable:
                        res += chr(i)

                print(f"DNS Query: {res}")


# Đường dẫn tới file pcap
pcap_file = "suspicious_traffic.pcap"

# Đọc file pcap và gọi hàm xử lý cho từng gói tin
sniff(offline=pcap_file, prn=process_packet, store=0)
