from email import message
import socket
import signal
import sys
import datetime
import struct
import psutil
import os

def signal_handler(sig, frame):
    print('\nDone!')
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
print('Press Ctrl+C to exit...')

ip_addr = "127.0.0.1"
tcp_port = 5005

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock.connect((ip_addr, tcp_port))

order=0
while True:
    try:        
        cpu = psutil.cpu_percent(2)
        total_memory, used_memory, free_memory = map(int, os.popen('free -t -m').readlines()[-1].split()[1:])
        mem = round((used_memory/total_memory) * 100, 2)
        version = 1
        order += 1
        size = struct.calcsize('f')
        pkt = struct.pack('BLLff', version, size, order, cpu, mem)
        sock.send(pkt)

    except (socket.timeout, socket.error):
        print('Server error. Done!')
        sys.exit(0)
