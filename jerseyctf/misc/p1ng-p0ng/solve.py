from scapy.all import *
conf.verb = False
# Định nghĩa nội dung ICMP 
for i in range(0x10, 0x100):
    p_str = i
    payload = b"(GET;"+ bytes.fromhex(hex(i)[2:]) + b";6)"

    # Tạo gói ICMP với nội dung trên
    ping = IP(dst="3.87.129.162")/ICMP()/payload 

    # Gửi request
    reply = sr1(ping)

    # In ra nội dung nhận được
    if reply:
        print(reply.load.decode())
        print(i)
        
'''
Entry #1: USE ICMP FOR COMMS -TL
46
Entry #2: PLS SEND FLAG -TL
46
Entry #3: SENDING NOW -RB
46
Entry #8: THX -TL
82
jctf{1L0V31CMP7UNN3L1N6}
'''
