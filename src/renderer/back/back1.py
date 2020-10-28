'''
Date: 2020-10-11 16:37:41
LastEditors: Jecosine
LastEditTime: 2020-10-14 17:26:24
'''
from scapy.all import *
import time
import os
import json
from package import Package as PKG
# import flask



class Sniffer:
    def __init__(self):
        self.devices = None
        self._handler = None
        self.packages = []
        self.sniffer = None

    def init_devices(self):
        devices = dict(ifaces)
        self.devices = {j.data["win_index"]: j.data for _, j in devices.items()}

    def get_device_name(self, win_index):
        if not self.devices:
            self.init_devices()
        return self.devices[win_index]["description"]

    def get_device_data(self, win_index):
        return self.devices[win_index]

    def get_dump_devices(self):
        return json.dumps(self.devices)

    def start_sniffer(self, win_index, filter=None, store=False, count=None):
        if not self._handler:
            print("[ERROR]: handler not specified")
        device_name = self.get_device_name(win_index)
        self.sniffer = AsyncSniffer(
            iface=device_name, filter=filter, store=store, prn=self._handler, count=10)
        self.sniffer.start()
        self.sniffer.join()
        # self.sniffer.stop()

    def set_handler(self, raw_handler):
        try:
            _ = compile(raw_handler, "", "exec")
        except Exception as e:
            return False
        return True

    def handler(self, _handler):
        self._handler = _handler

    def save_pcap(self, pkts, file_name):
        try:
            wrpcap(file_name, pkts)
        except Exception as e:
            return False
        return True


sniffer = Sniffer()


@sniffer.handler
def mhandler(x):
    time.sleep(2)
    # x.show()
    p = PKG(raw(x))
    print("===Ether===")
    print(p.ethernet_header)
    print("===IP===")
    print(p.ipv4 if p.ip_version == 4 else p.ipv6)


sniffer.start_sniffer(22)
# sniff(prn=handler, count=5)
