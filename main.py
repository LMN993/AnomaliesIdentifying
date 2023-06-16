import csv
import pyshark
from collections import Counter
import os
import re

str_packet = []
packet_count = []


def parsing():
    uploaded = []
    for root, dirs, files in os.walk('test'):
        for filenam in files:
            path = os.path.join('test', filenam)
            uploaded.append(path)
    # print(uploaded)
    return uploaded


def network_conversation(packet):
    try:

        protocol = packet.transport_layer
        source_address = packet.ip.src
        # source_port = packet[packet.transport_layer].srcport
        destination_address = packet.ip.dst
        destination_port = packet[packet.transport_layer].dstport
        # return (time_p, protocol, source_address, destination_address)
        return (source_address, destination_address, destination_port)
    except AttributeError as e:
        return None


def counting(filename):
    number = int(re.search(r'\d+', filename).group())
    capture = pyshark.FileCapture(filename, keep_packets=False, display_filter='udp.dstport==1200')
    capture.load_packets()
    conversations = []
    for packet in capture:
        results = network_conversation(packet)

        if results != None and (int(results[0].split('.')[-1]) == number+1 or int(results[1].split('.')[-1]) == number+1):
            conversations.append(" ".join(results))

    c = Counter(conversations)
    same_packets = dict(c)
    # same_packets.clear()
    conversations.clear()
    return same_packets


if __name__ == '__main__':
    name = parsing()
    with open("results.csv", "w", newline='', encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile, delimiter=",", quotechar='"', quoting=csv.QUOTE_ALL)
        for i in range(len(name)):
            f = name[i].split('\\', -1)
            print("Counting UDP packets in " + f[-1] + " file")
            new_dict = counting(name[i])
            # словарь с одинаковыми элементами   протокол -> откуда -> куда : сколько
            for key, value in new_dict.items():
                print('"', f[-1], '", "', key, '", "', value, '"', sep="")
                row = [f[-1], key, value]
                writer.writerow(row)
