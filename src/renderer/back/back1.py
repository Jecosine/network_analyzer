'''
Date: 2020-10-11 16:37:41
LastEditors: Please set LastEditors
LastEditTime: 2020-12-02 16:54:39
'''
from scapy.all import *
import time
import ipaddress
import os
import json
import websocket as ws
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
    def pause_sniffer(self):
        if self.sniffer != None:
            self.sniffer.stop()
    def start_sniffer(self, win_index, filter=None, store=False, count=None):
        if not self._handler:
            print("[ERROR]: handler not specified")
        if self.sniffer != None:
            self.sniffer.start()
            return
        device_name = self.get_device_name(win_index)
        self.sniffer = AsyncSniffer(
            iface=device_name, filter=filter, store=store, prn=self._handler)
        self.sniffer.start()
        # self.sniffer.join()
    def stop_sniffer(self):
        try:
            self.sniffer.stop()
        except Exception as e:
            print(e)
    def close_sniffer(self):
        try:
            self.sniffer.stop()
            self.sniffer = None
        except Exception as e:
            print(e)
            self.sniffer = None

        
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

