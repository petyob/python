# Parses TCPDump file to produce some statistics.
# Try using unittest
# Author: Petyo Byankov

import argparse
import time
import re
import unittest

startTime = time.time()

parser = argparse.ArgumentParser(description='Produce some statistics from a TCPDump file')
parser.add_argument(dest='filename', metavar='filename', nargs='*')
parser.add_argument('-v', dest='verbose', help='Verbose mode')
parser.add_argument('-o', dest='op', help='Options')
args = parser.parse_args()
if args.filename:
    tcpdump_file = args.filename[0]
else:
    tcpdump_file = 'tcpdump.log'

# tcpdump line  pathern
_tcpdump_patern = re.compile(
        r'(\d{2}:\d{2}:\d{2}.\d{6}) IP (\d*\.\d*.\d*.\d*).(\d*) > (\d*\.\d*.\d*.\d*).(\d*): UDP, length (\d*)')

# Main data structures
count_small_packets = 0
count_large_packets = 0
clients = dict()  # IP's and traffic(sum of packet's size)
servers = dict()  # IP's and number ot packets


def parse_line(line):
    try:
        # packet_time = _tcpdump_patern.search(line).group(1)
        client_ip = _tcpdump_patern.search(line).group(2)
        # client_port = _tcpdump_patern.search(line).group(3)
        server_ip = _tcpdump_patern.search(line).group(4)
        # server_port = _tcpdump_patern.search(line).group(5)
        packet_size = int(_tcpdump_patern.search(line).group(6))
        return client_ip, server_ip, packet_size
    except:
        return "Error parsing line: ", line


with open(tcpdump_file) as dumpfile:  # Default buffering for text files is line buffering
    for line in dumpfile:
        try:
            client_ip, server_ip, packet_size = parse_line(line)
            if client_ip not in clients:
                clients[client_ip] = 0
            clients[client_ip] += packet_size

            if server_ip not in servers:
                servers[server_ip] = 0
            servers[server_ip] += 1

            if packet_size > 512:
                count_large_packets += 1
            else:
                count_small_packets += 1
        except:
            print("Error parsing line: ", line)


def pick_top_10(hosts):
    hosts_sorted = sorted(hosts, key=lambda x: hosts[x])
#    for x in range(10):
#       yield hosts_sorted.pop()
    return reversed(hosts_sorted[-10:])


def produce_servers_report():
    print("Top 10 servers receiving the most packets.\nShowing the amount of packets received by each:\n")
    for k in pick_top_10(servers):
        print('{0:20} {1:d}'.format(k, servers[k]))


def produce_clients_report():
    print("\nTop 10 clients sending the most bytes.\nShowing the IP address and the number of bytes sent:\n")
    for k in pick_top_10(clients):
        print('{0:20} {1:d}'.format(k,clients[k]))


def small_Packet_report():
    print('\nPercentage of "small" packets: {} % '.format(
            (count_small_packets / (count_small_packets + count_large_packets)) * 100))


def large_pacjet_report():
    print('\nPercentage of "large"  packets: {} % '.format(
            (count_large_packets / (count_small_packets + count_large_packets)) * 100))

# dirty code for case-like choosing.
if args.op == None:
    produce_servers_report()
    produce_clients_report()
    small_Packet_report()
    large_pacjet_report()
elif args.op == "servers":
    produce_servers_report()
elif args.op == "clients":
    produce_clients_report()
elif args.op == "small":
    small_Packet_report()
elif args.op == "large":
    large_pacjet_report()


class Tests(unittest.TestCase):
    def test_parse(self):
        self.assertEqual(
                parse_line("09:59:45.083000 IP 10.0.64.177.8625 > 10.100.0.156.2424: UDP, length 636"),
                ('09:59:45.083000', '10.0.64.177', '10.100.0.156', 636)
        )

    def test_parse_bad_line(self):
        self.assertEqual(
                parse_line("bad line"),
                ("Error parsing line: ", "bad line")
        )

print(time.time()- startTime)

#unittest.main()

